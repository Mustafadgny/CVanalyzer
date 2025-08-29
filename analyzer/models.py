from django.db import models

class UploadedCv(models.Model):
    pdf = models.FileField(upload_to='cvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pdf)
