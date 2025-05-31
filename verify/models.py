from django.db import models


class documenttype(models.Model):
    doc_type=models.CharField(max_length=3)
    def __str__(self):
        return "Document Type"
class aadhaarusers(models.Model):
    username=models.CharField(max_length=30)
    aadharnumber=models.IntegerField(max_length=12,unique=True,primary_key=True)
    verification=models.BooleanField()
    mobilenumber=models.IntegerField(max_length=10)
    dob=models.DateField(null=True)
    def __str__(self):
        return self.username
class panusers(models.Model):
    username=models.CharField(max_length=30)
    pannumber=models.CharField(max_length=10,unique=True,primary_key=True)
    verification=models.BooleanField()
    mobilenumber=models.IntegerField(max_length=10)
    dob=models.DateField(null=True)
    def __str__(self):
        return self.username
class Certificate(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='certificates/')
    extracted_text = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    aadhaar_number = models.CharField(max_length=12, blank=True, null=True)
    def __str__(self):
        return f"Certificate {self.id} uploaded at {self.uploaded_at}"
class AadhaarRecord(models.Model):
    aadhaar_number = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    def __str__(self):
        return self.name
