import re
from datetime import datetime
import pytesseract
from PIL import Image
from pyzbar.pyzbar import decode

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path):
    """Extract text from an image using pytesseract without preprocessing."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang="eng+tam")
        return text
    except Exception as e:
        return f"OCR Error: {str(e)}"

def extract_qr_code(image_path):
    """Extract QR code data from an image."""
    try:
        image = Image.open(image_path)
        decoded_objects = decode(image)
        if decoded_objects:
            return decoded_objects[0].data.decode("utf-8")
        return "No QR code detected"
    except Exception as e:
        return f"QR Code Error: {str(e)}"

def parse_details_from_text(extracted_text):
    """Parse Aadhaar details from the extracted text."""
    cleaned_text = " ".join(extracted_text.split())

    # Extract Aadhaar Number
    aadhaar_number = re.search(r'\b\d{4}\s?\d{4}\s?\d{4}\b', cleaned_text)
    aadhaar_number = aadhaar_number.group(0).replace(" ", "") if aadhaar_number else None

    # Extract Name
    name_match = re.search(r'(?:Name[:\-]?\s*|)\s*([A-Za-z\s]+)', cleaned_text)
    name = name_match.group(2).strip() if name_match else None

    # Extract Date of Birth
    dob_match = re.search(r'DOB[:\-]?\s*(\d{2}/\d{2}/\d{4})', cleaned_text)
    dob = datetime.strptime(dob_match.group(1), "%d/%m/%Y").date() if dob_match else None

    # Extract Gender
    gender_match = re.search(r'\b(Male|Female|ஆண்|பெண்)\b', cleaned_text, re.IGNORECASE)
    gender = gender_match.group(1).capitalize() if gender_match else None

    return {
        'aadhaar_number': aadhaar_number,
        'name': name,
        'dob': dob,
        'gender': gender,
    }

def validate_aadhaar_pattern(details):
    """Validate Aadhaar card pattern."""
    if not details['aadhaar_number'] or not details['name'] or not details['dob'] or not details['gender']:
        return False, "Invalid Aadhaar Pattern: Missing required fields"
    return True, "Aadhaar Pattern Valid"
