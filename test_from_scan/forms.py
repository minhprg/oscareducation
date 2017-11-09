# encoding: utf-8

from django import forms
from examinations.models import TestAnswerFromScan



def validate_copy_extension(value):
    if not value.name.endswith('.png') and not value.name.endswith('.jpg'):
        raise forms.ValidationError("Only PNG and JPG files are accepted")

class ImportCopyForm(forms.Form):
    copy = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                            validators=[validate_copy_extension])


