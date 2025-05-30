# Certisure - Certificate Validation and Verification System

**Certisure** is a simulation web application that demonstrates how digital certificates can be validated and verified. It allows institutions and organizations to generate, upload, and verify certificates using modern web technologies and techniques like QR code extraction and template matching.

## 🚀 Features

- Upload and store digital certificates securely
- Verify authenticity of certificates using QR code decoding
- Match uploaded certificates with predefined templates for validation

## 🛠 Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (can be replaced with PostgreSQL or MySQL)
- **Certificate Processing:** 
  - **QR Code Extraction:** `opencv-python`, `pyzbar`
  - **Template Matching:** `OpenCV`
- **Others:** Pillow (image processing), Django Admin for management

## 📷 Certificate Verification Workflow

1. User uploads a certificate image or PDF.
2. QR code embedded in the certificate is decoded to retrieve essential metadata (e.g., certificate ID).
3. The template structure of the uploaded certificate is compared against a verified template using OpenCV template matching.
4. The system cross-verifies the data with the database to validate authenticity.

## 🧪 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/your-username/certisure.git
cd certisure

# Create a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations and run the server
python manage.py migrate
python manage.py runserver
