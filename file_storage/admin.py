from django.contrib import admin
from django.http import HttpResponse
from django.contrib.auth.models import User
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from io import BytesIO
import uuid
from file_storage.models import FileStorage


class FileStorageAdmin(admin.ModelAdmin):
    exclude = ('filename','encrypted_aeskey','ecc_public_key',)
    
    def upload_file(self, request):
        # Read the uploaded file
        file = request.FILES['file']
        file_data = file.read()

        # Generate a new AES key
        aes_key = Fernet.generate_key()

        # Encrypt the file data with the AES key
        cipher = Fernet(aes_key)
        encrypted_file_data = cipher.encrypt(file_data)

        # Get the public key of the user who uploaded the file
        user = User.objects.get(username=request.user.username)
        public_key = RSA.import_key(user.public_key)

        # Encrypt the AES key with the user's public key
        cipher = RSA.new(public_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256), algorithm=hashes.SHA256, label=None))
        encrypted_aes_key = cipher.encrypt(aes_key)

        # Save the encrypted file data and encrypted AES key to the database
        file_obj = File.objects.create(file_name=file.name, file_data=encrypted_file_data, encrypted_aes_key=encrypted_aes_key)
        file_obj.save()

        # Return a success response
        response = HttpResponse(content_type='text/plain')
        response.write('File uploaded successfully')
        return response
# Register your models here.
admin.site.register(FileStorage, FileStorageAdmin)