from django import forms
from .models import Point, DisasterTypes


class PointForm(forms.ModelForm):
    """Form for Point model"""

    disaster_type = forms.ChoiceField(widget=forms.RadioSelect, choices=DisasterTypes.CHOICES)

    class Meta:
        model = Point
        fields = ["name", "disaster_level", "is_verified"]


class PointAdminForm(forms.ModelForm):
    """TODO"""

    disaster_type = forms.ChoiceField(widget=forms.RadioSelect, choices=DisasterTypes.CHOICES)

    class Meta:
        model = Point
        fields = ["name", "disaster_level", "is_verified"]


class PointUserOwnerForm(forms.ModelForm):
    """TODO"""
    disaster_type = forms.ChoiceField(widget=forms.RadioSelect, choices=DisasterTypes.CHOICES)

    class Meta:
        model = Point
        fields = ["name", "disaster_level"]
