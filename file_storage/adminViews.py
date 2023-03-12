


import base64
import os
from django.shortcuts import render
from customuser.models import CustomUser

from file_storage.models import FileStorage
from secure_file_storage_app import settings

from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

def sport_dashboard(request):
    return render(request, "custom-pages/file_access.html")

from django.views import View
from django.http import HttpResponse
from cryptography.fernet import Fernet

class DownloadView(View):
    def get(self, request, file_storage_id):
        file = FileStorage.objects.get(id=file_storage_id)
        encrypted_path = file.filename
        aes_key = file.encrypted_aeskey
        created_by_user = CustomUser.objects.get(pk=file.created_by)
        # Decrypt the encrypted AES key using the user's RSA private key
        private_key = serialization.load_pem_private_key(
            created_by_user.private_key.encode('utf-8'),
            password=None,
            backend=default_backend(),
        )

        decrypted_key = private_key.decrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        file_path = os.path.join(settings.MEDIA_ROOT, encrypted_path)
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        print('before rrrrrrrrrrrrrr')
        cipher_suite = Fernet(decrypted_key)
        print('after fffffffffffffffffffffff')
        decrypted_data = cipher_suite.decrypt(encrypted_data)

        response = HttpResponse(decrypted_data, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file.filename}"'

        return response
