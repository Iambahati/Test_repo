from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import gettext_lazy as _
from .models import PasswordResetToken
from django.core.mail import send_mail

class RegisterForm(forms.ModelForm):
    """
    User registration form with password validation.
    """
    class Meta:
        model = get_user_model()
        fields = ['email', 'full_name', 'password']

    email = forms.EmailField(
        required=True,
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if get_user_model().objects.filter(email=email).exists():
                raise ValidationError('This email address is already in use.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError('Passwords do not match')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    
class LoginForm(forms.Form):
    """
    Login form for handling user login.
    """
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class TherapistProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['specializations', 'bio', 'years_experience', 'availability']
    
class VerifyEmailForm(forms.Form):
    """
    Form for verifying user email address.
    """
    token = forms.CharField()
    
    def clean_token(self):
        token = self.cleaned_data.get('token')
        if len(token) != 6:
            raise ValidationError('Invalid token')
        return token
    
class CustomPasswordResetForm(PasswordResetForm):
    def save(self, **kwargs):
        email = self.cleaned_data["email"]
        model = get_user_model()
        active_users = model.objects.filter(email=email, is_active=True)

        if active_users.exists():
            for user in active_users:
                # Generate token and save to DB
                token = PasswordResetToken.objects.create(user=user)
                
                # Send email with token (customize your email template as needed)
                token_url = f"http://yourdomain.com/reset/{user.id}/{token.token}/"
                send_mail(
                    "Password Reset Request",
                    f"Use this link to reset your password: {token_url}",
                    "no-reply@yourdomain.com",
                    [user.email],
                )