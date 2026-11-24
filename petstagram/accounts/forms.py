from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _

from petstagram.accounts.models import Profile


UserModel = get_user_model()

class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ("email",)


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class AppUserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )  # no need
  

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "date_of_birth", "profile_picture"]
        labels = {
            "first_name": "First Name:",
            "last_name": "Last Name:",
            "date_of_birth": "Date of Birth:",
            "profile_picture": "Profile Picture:",
        }
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}
