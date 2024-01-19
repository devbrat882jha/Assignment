from django.db import models

# Create your models here.

class Upload(models.Model):
    file = models.FileField(upload_to='files')
    
    
    def __str__(self) -> str:
        return str(self.file)
