from django import forms
from .models import Job, CNCMachineDescription

class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_name', 'job_notes', 'CNCMachine']  # Replace 'Workshop' with 'CNCMachine'
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
            # 'CNCMachine' will be automatically rendered as a dropdown
        }

    def __init__(self, *args, **kwargs):
        super(CreateJobForm, self).__init__(*args, **kwargs)
        # Set the queryset for the CNCMachine dropdown to display MachineName
        self.fields['CNCMachine'].queryset = CNCMachineDescription.objects.all()
        self.fields['CNCMachine'].label_from_instance = lambda obj: "%s" % obj.machine_name
        self.fields['CNCMachine'].empty_label = "Select a machine"
