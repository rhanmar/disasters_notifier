from django import forms
from .models import Point


class PointForm(forms.ModelForm):
    """Form for Point model"""

    disaster_type = forms.ChoiceField(widget=forms.RadioSelect, choices=Point.DISASTER_TYPES)

    class Meta:
        model = Point
        fields = ["name", "disaster_level", "verified"]


class PointAdminForm(forms.ModelForm):
    """TODO"""

    disaster_type = forms.ChoiceField(widget=forms.RadioSelect, choices=Point.DISASTER_TYPES)

    class Meta:
        model = Point
        fields = ["name", "disaster_level", "verified"]


class PointUserOwnerForm(forms.ModelForm):
    """TODO"""
    disaster_type = forms.ChoiceField(widget=forms.RadioSelect, choices=Point.DISASTER_TYPES)

    class Meta:
        model = Point
        fields = ["name", "disaster_level"]


# class PointUserNonOwnerForm(forms.ModelForm):
#     pass  TODO REMOVE
