from asyncio import format_helpers
import base64
import os
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
from secure_file_storage_app import settings
import os
from django.conf import settings
from cryptography.fernet import Fernet
from django.utils.html import format_html

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)
    
    return fernet

class FileStorageAdmin(admin.ModelAdmin):
    exclude = ('filename','encrypted_aeskey','ecc_public_key','created_at','created_by','deleted_at','deleted_by','updated_at','updated_by')
    list_display = ["filename","view_team_list"]
    
    def view_team_list(self, obj):
        return format_html('<a class="btn btn-primary" style="border-radius:5px;background-color:#483D8B;color:white;" href="/admin/file-download/{}/">Download</a>',obj.id)
    view_team_list.short_description = 'Team List'
    
    def save_model(self, request, obj, form, change):
        print("called........../////////////")
        # Call the parent save_model method to save the model instance
        uploaded_file = request.FILES['encrypted_filepath']
        
        # Generate a new AES key
        key = Fernet.generate_key()
        # Encrypt the file and save it to disk
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.read())
        fernet_key = encrypt_file(file_path, key)
        # Save the key and file path to the database
        
        #encrypt aeskey with ECC key of the user request.user.public_key

        obj.encrypted_aeskey = fernet_key
        obj.filename = uploaded_file.name
        obj.encrypted_filepath = file_path
        
        if change:
            obj.updated_by = request.user.id
        else:
            obj.created_by = request.user.id
        # Call the parent save_model method
        super().save_model(request, obj, form, change)
        
    def delete_model(self, request, obj):
        obj.deleted_by = request.user.id
        obj.delete()

# # Register your models here.
admin.site.register(FileStorage, FileStorageAdmin)