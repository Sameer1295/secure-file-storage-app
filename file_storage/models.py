from django.db import models

from customuser.models import CustomUser

# Create your models here.
class FileStorage(models.Model):  
      
    filename = models.CharField(max_length=100)
    encrypted_filepath = models.FileField(max_length=1000)
    encrypted_aeskey = models.BinaryField(max_length=1000)
    ecc_public_key = models.CharField(max_length=1000)
    access_users = models.ManyToManyField(CustomUser, related_name='access_files', blank=True)
    created_at = models.DateTimeField(null=True)
    created_by = models.IntegerField(null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.IntegerField(null=True)
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.IntegerField(null=True)    
    class Meta:  
        db_table = "file_storage_tbl"  