from django import forms
from .models import Point


class PointForm(forms.ModelForm):
    """Form for Point model"""

    class Meta:
        model = Point
        fields = ['name']
