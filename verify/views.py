from django.shortcuts import render,redirect
from .models import aadhaarusers,panusers
from .forms import numberfield
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth import logout
from django.contrib import messages,auth
from .forms import SignUpForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
import re
from pyzbar.pyzbar import decode
from PIL import Image
import json
from datetime import datetime
from pytesseract import image_to_string
from PIL import Image
from .models import AadhaarRecord, Certificate
from .forms import CertificateUploadForm
from .forms import CertificateUploadForm
from .models import Certificate, AadhaarRecord
from .utils import extract_text_from_image, extract_qr_code,validate_aadhaar_pattern
import re

from datetime import datetime

import json

import re

from PIL import Image, ImageFilter, ImageEnhance
import pytesseract

from datetime import datetime

import cv2
import numpy as np


def does_template_exist(uploaded_path, template_path, threshold=0.31):
    """
    Check if the template exists as a sub-image within the uploaded Aadhaar card document.
    - uploaded_path: Path to the uploaded document (image).
    - template_path: Path to the template image (sub-image).
    - threshold: Matching threshold (default: 0.8 for high confidence).
    """
    try:
        # Load the images in grayscale
        uploaded_image = cv2.imread(uploaded_path, cv2.IMREAD_GRAYSCALE)
        template_image = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

        # Get the dimensions of the template
        template_height, template_width = template_image.shape

        # Perform template matching
        result = cv2.matchTemplate(uploaded_image, template_image, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        # Check if the match exceeds the threshold
        print(f"Template matching score: {max_val}")  # Log the matching score
        if max_val >= threshold:
            return True  # Template exists
        else:
            return False  # Template does not exist
    except Exception as e:
        print(f"Error during template matching: {e}")
        return False
def normalize_date_format(date_string, input_format="%d/%m/%Y", output_format="%Y-%m-%d"):
    """
    Normalize a date string to a specific format.
    - date_string: The date string to normalize (e.g., '12/02/1966').
    - input_format: The format of the input date string.
    - output_format: The desired output format.
    """
    try:
        date_object = datetime.strptime(date_string, input_format)  # Parse input format
        return date_object.strftime(output_format)  # Convert to output format
    except ValueError:
        return None  # Return None if parsing fails



def preprocess_image(image_path):
    """
    Preprocess the image to enhance OCR accuracy.
    - Convert to grayscale
    - Apply thresholding
    - Enhance sharpness
    """
    try:
        image = Image.open(image_path)
        image = image.convert("L")  # Convert to grayscale
        image = image.filter(ImageFilter.SHARPEN)  # Sharpen the image
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)  # Enhance contrast
        return image
    except Exception as e:
        print(f"Image preprocessing error: {e}")
        return None

def extract_text_from_image(image_path):
    """
    Extract text from an Aadhaar card image using enhanced preprocessing.
    """
    try:
        preprocessed_image = preprocess_image(image_path)
        if not preprocessed_image:
            return ""
        text = pytesseract.image_to_string(preprocessed_image, lang="eng")
        return text or ""
    except Exception as e:
        print(f"OCR extraction error: {e}")
        return ""


def extract_qr_code(file_path):
    """
    Extract QR code data from an image file and return it as a dictionary or string.
    """
    try:
        image = Image.open(file_path)
        decoded_objects = decode(image)
        if not decoded_objects:
            return None  # No QR code found

        # Assume there's only one QR code
        qr_code_data = decoded_objects[0].data.decode('utf-8')
        
        # Try parsing as JSON
        try:
            return json.loads(qr_code_data)
        except json.JSONDecodeError:
            # If not JSON, return as plain string
            return qr_code_data
    except Exception as e:
        print(f"QR code extraction error: {e}")
        return None


def parse_details_from_text_and_qr(extracted_text, qr_data):
    """
    Parse Aadhaar details from both text and QR code data.
    """
    cleaned_text = " ".join(extracted_text.split())  # Clean OCR text

    # Extract Aadhaar Number
    aadhaar_number_match = re.search(r'\b\d{4}\s?\d{4}\s?\d{4}\b', cleaned_text)
    aadhaar_number = aadhaar_number_match.group(0).replace(" ", "") if aadhaar_number_match else None

    # Extract Name (prioritize English names)
    name_match = re.search(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)', cleaned_text)
    name = name_match.group(0).strip() if name_match else None

    # Extract Date of Birth
    dob_match = re.search(r'(?:DOB[:\-]?\s*)?(\d{2}/\d{2}/\d{4})', cleaned_text)
    dob = dob_match.group(1) if dob_match else None

    # Extract Gender
    gender_match = re.search(r'\b(Male|Female)\b', cleaned_text, re.IGNORECASE)
    gender = gender_match.group(1).capitalize() if gender_match else None

    # Fallback to QR data if OCR fails
    if isinstance(qr_data, dict):
        aadhaar_number = aadhaar_number or qr_data.get("uid")
        name = name or qr_data.get("name")
        dob = dob or qr_data.get("dob")
        if not gender:
            gender = "Male" if qr_data.get("gender") == "M" else "Female"

    return {
        'aadhaar_number': aadhaar_number,
        'name': name,
        'dob': dob,
        'gender': gender,
    }

@login_required
def upload_certificate(request):
    """
    Handles the upload of Aadhaar card images, checks if the template exists,
    and proceeds with verification.
    """
    if request.method == 'POST':
        form = CertificateUploadForm(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save()
            uploaded_path = certificate.file.path
            template_path = "C:\\Users\\sudharshan\\Documents\\Designthinking\\certisure\\verify\\aadhaar_templates\\aadhaartext.png"  # Replace with your actual template path

            # Check if the uploaded document contains the template
            if not does_template_exist(uploaded_path, template_path):
                return render(request, 'result.html', {'message': "Validation Failed: Not a valid Aadhaar card."})

            # Proceed with extracting details and validating
            extracted_text = extract_text_from_image(uploaded_path)
            qr_data = extract_qr_code(uploaded_path)

            # Parse details
            details = parse_details_from_text_and_qr(extracted_text, qr_data)

            # Save parsed details to the certificate
            certificate.aadhaar_number = details.get('aadhaar_number')
            certificate.name = details.get('name')
            dob = details.get('dob')
            if dob:
                certificate.dob = datetime.strptime(dob, "%d/%m/%Y").strftime("%Y-%m-%d")
            certificate.gender = details.get('gender')
            certificate.save()

            # Validate with database
            try:
                record = AadhaarRecord.objects.get(aadhaar_number=details['aadhaar_number'])
                if (
                    record.name.lower() == details['name'].lower() and
                    record.dob.strftime("%Y-%m-%d") == certificate.dob and
                    record.gender.lower() == details['gender'].lower()
                ):
                    return render(request, 'result.html', {'message': "Validation Successful", 'details': details})
                else:
                    return render(request, 'result.html', {'message': "Validation Failed: Details do not match", 'details': details})
            except AadhaarRecord.DoesNotExist:
                return render(request, 'result.html', {'message': "Validation Failed: Aadhaar not found in database", 'details': details})
    else:
        form = CertificateUploadForm()
    return render(request, 'upload.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('verify:upload_certificate')  # Redirect authenticated users

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('verify:login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()
    return render(request, 'signin.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect('verify:upload_certificate')  # Redirect authenticated users

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                user=form.get_user()
                auth_login(request,user)
                messages.success(request, f"Welcome, {username}!")
                return redirect('verify:upload_certificate')  # Redirect to desired page
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('verify:login')


def home(request):
    return render(request,'index.html')

def db(request):
    user=aadhaarusers.objects.all()
    return render(request,'test.html',{'user':user})
@login_required
def input_page(request):
    result = None
    error = None

    if request.method == 'POST':
        form = numberfield(request.POST)
        doc=request.POST.get('doc_type')
        if form.is_valid():
            number = form.cleaned_data['number']
            
            if doc == 'aadhaar':
                try:
                    # Query the database for the entered number
                    result = aadhaarusers.objects.filter(aadharnumber=number).first()
                    if not result:
                        error = "No matching record found for the entered number."
                except Exception as e:
                    error = f"An error occurred while querying the database: {str(e)}"
            elif doc=="pan":
                try:
                    # Query the database for the entered number
                    result = panusers.objects.filter(pannumber=number).first()
                    if not result:
                        error = "No matching record found for the entered number."
                except Exception as e:
                    error = f"An error occurred while querying the database: {str(e)}"
    else:
        form = numberfield()

    # Render the same page with form, result, or error
    return render(request, 'testing.html', {'form': form, 'result': result, 'error': error})