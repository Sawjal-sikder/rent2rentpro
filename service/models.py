from django.db import models # type: ignore

class ContactCreationFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='contracts/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    