from django import forms
from .models import Job, CNCMachineDescription

class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_name', 'job_notes', 'CNCMachine', 'mm8_notes', 'mm8_quantity', 'mm18_notes', 'mm18_quantity']
        widgets = {
            'job_name': forms.TextInput(attrs={
                'placeholder': 'Enter job name',
                'class': 'form-control'
            }),
            'job_notes': forms.Textarea(attrs={
                'placeholder': 'Add job notes here',
                'class': 'form-control autoresize',
                'rows': '2'
            }),
            'CNCMachine': forms.Select(attrs={
                'class': 'form-control form-control-select'  # Adding the custom class for the dropdown
            }),

            'mm8_notes': forms.Textarea(attrs={
                'placeholder': 'Add 8mm notes here',
                'class': 'form-control autoresize',
                'rows': '2'
            }),

            'mm8_quantity': forms.Textarea(attrs={
                'placeholder': 'Enter quantity here',
                'class': 'form-control autoresize',
                'rows': '1'
            }),

            'mm18_notes': forms.Textarea(attrs={
                'placeholder': 'Add 18mm notes here',
                'class': 'form-control autoresize',
                'rows': '2'
            }),

            'mm18_quantity': forms.Textarea(attrs={
                'placeholder': 'Enter quantity here',
                'class': 'form-control autoresize',
                'rows': '1'
            }),

            # 'CNCMachine' will be automatically rendered as a dropdown
        }

    def __init__(self, *args, **kwargs):
        super(CreateJobForm, self).__init__(*args, **kwargs)
        # Set the queryset for the CNCMachine dropdown to display MachineName
        self.fields['CNCMachine'].queryset = CNCMachineDescription.objects.all()
        self.fields['CNCMachine'].label_from_instance = lambda obj: "%s" % obj.machine_name
        self.fields['CNCMachine'].empty_label = "Select a machine"




