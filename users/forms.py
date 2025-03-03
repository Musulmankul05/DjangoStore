from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import UserModel


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    username = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    date_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if '__all__' in self.errors:
            del self.errors['__all__']  # Удаление ошибки
        return cleaned_data

    class Meta:
        model = UserModel
        fields = ("username", "first_name", "last_name", "email", "date_birth", "password1", "password2")


class EditProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={"accept": "image/jpeg, image/png"}), required=False)

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'image',)


class PasswordResetForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())
