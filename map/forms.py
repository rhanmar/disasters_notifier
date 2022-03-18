from django import forms

from .models import DisasterTypes, Point


class PointForm(forms.ModelForm):
    """Form for Point model."""

    disaster_type = forms.ChoiceField(widget=forms.RadioSelect, choices=DisasterTypes.CHOICES)

    class Meta:
        model = Point
        fields = ["name", "disaster_level", "is_verified", "description"]
        help_texts = {
            "is_verified": None,
        }


class PointAdminForm(forms.ModelForm):
    """Point Form for Admin."""

    disaster_type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=DisasterTypes.CHOICES,
        label="Тип стихийного бедствия"
    )

    class Meta:
        model = Point
        fields = [
            "name",
            "description",
            "disaster_level",
            "is_verified",
        ]
        help_texts = {
            "is_verified": None,
        }


class PointUserOwnerForm(forms.ModelForm):
    """Point Form for User Owner."""
    disaster_type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=DisasterTypes.CHOICES,
        label="Тип стихийного бедствия"
    )

    class Meta:
        model = Point
        fields = [
            "name",
            "description",
            "disaster_level",
        ]
        help_texts = {
            "is_verified": None,
        }
