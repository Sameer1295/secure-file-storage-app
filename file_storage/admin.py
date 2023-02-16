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

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)

# savemodel function works
# need to add code to encrypt file using aes key
    # first need access to file in request
    # then that encrypted_filepath file is read and ecnrpyted file is generated
class FileStorageAdmin(admin.ModelAdmin):
    exclude = ('filename','encrypted_aeskey','ecc_public_key','created_at','created_by','deleted_at','deleted_by','updated_at','updated_by')
    
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
        encrypt_file(file_path, key)
        # Save the key and file path to the database
        obj.encrypted_aeskey = key
        obj.filename = uploaded_file.name
        obj.encrypted_filepath = file_path
        
        if change:
            obj.updated_by = request.user.id
        else:
            obj.created_by = request.user.id
        # Call the parent save_model method
        super().save_model(request, obj, form, change)
        
        # encrypted_file_path = 'sdfsdf1111'+image_path.name
        # key = 'sdfsdfdsffdsgdsgdsgsdg'
        # FileStorage.objects.create(encrypted_filepath=encrypted_file_path, encrypted_aeskey=key)
        # Deleted by 

    def delete_model(self, request, obj):
        obj.deleted_by = request.user.id
        obj.delete()

# # Register your models here.
admin.site.register(FileStorage, FileStorageAdmin)