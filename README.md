# Certisure - Certificate Validation and Verification System

**Certisure** is a simulation web application that demonstrates how digital certificates can be validated and verified. For now i have only simulated the validation and verification of Aadhaar Card.

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
5. Note: This is only the simulation system Data are verified against Predefined Dataset.
