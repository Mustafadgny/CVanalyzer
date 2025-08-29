from django import forms
from .models import UploadedCv

class CvUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedCv
        fields = ['pdf']
