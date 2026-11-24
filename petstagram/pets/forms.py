from django import forms

from petstagram.pets.models import Pet


class PetForm(forms.ModelForm):
    field_order = ["name", "date_of_birth"]

    class Meta:
        model = Pet
        exclude = ["slug", "user"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Pet name"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "personal_photo": forms.URLInput(attrs={"placeholder": "Link to image"})
        }
        labels = {
            "name": "Pet Name",
            "date_of_birth": "Date of Birth",
            "personal_photo": "Link to Image"
        }


class PetDeleteForm(PetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
            field.widget.attrs["readonly"] = True
            # field.widget.attrs["disabled"] = "disabled"
            # field.widget.attrs["readonly"] = "readonly"

# Uni version: with Mixin
