from django import forms
from .models import Job

class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_name']
        widgets = {
            'job_name': forms.TextInput(attrs={'placeholder': 'Enter job name'}),
        }
