from django import forms


class PartnershipForm(forms.Form):
    CLASS_CHOICES = [
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('both', 'Both'),
    ]
    
    school_name = forms.CharField(max_length=255)
    school_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    school_phone = forms.CharField(max_length=20)
    school_email = forms.EmailField()
    class_type = forms.ChoiceField(choices=CLASS_CHOICES, widget=forms.RadioSelect)