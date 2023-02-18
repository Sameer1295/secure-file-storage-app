


import os
from django.shortcuts import render

from file_storage.models import FileStorage
from secure_file_storage_app import settings


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
        
        file_path = os.path.join(settings.MEDIA_ROOT, encrypted_path)
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        print('before rrrrrrrrrrrrrr')
        cipher_suite = Fernet(aes_key)
        print('after fffffffffffffffffffffff')
        decrypted_data = aes_key.decrypt(encrypted_data)

        response = HttpResponse(decrypted_data, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file.filename}"'

        return response
