from django.db import models

# Create your models here.
class FileStorage(models.Model):  
      
    filename = models.CharField(max_length=100)
    encrypted_filepath = models.FileField(max_length=1000)
    encrypted_aeskey = models.CharField(max_length=1000)
    ecc_public_key = models.CharField(max_length=1000)
    
    class Meta:  
        db_table = "file_storage_tbl"  