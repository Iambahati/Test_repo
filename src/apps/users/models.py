from typing import Any

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator

class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str, **extra_fields: Any) -> 'CustomUser':
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> 'CustomUser':
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 1)
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    class Roles(models.IntegerChoices):
        ADMIN = 1, 'Admin'
        THERAPIST = 2, 'Therapist'
        User = 3, 'User'
    
    username = None
    email = models.EmailField(unique=True)
    # email_is_verified = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255)
    role = models.IntegerField(choices=Roles.choices, default=Roles.User)
    profile_image = models.CharField(max_length=255, null=True, blank=True)
    email_verified_at = models.DateTimeField(null=True)
    specializations = models.TextField(blank=True, null=True, help_text="Comma-separated list of specializations")
    bio = models.TextField(null=True, blank=True)
    years_experience = models.IntegerField(null=True, blank=True)
    availability = models.JSONField(default=dict, blank=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.user.email}"

    def is_expired(self):
        """Check if the token is expired."""
        return timezone.now() > self.expired_at

    def generate_token(self):
        """Generate token using default_token_generator."""
        self.token = default_token_generator.make_token(self.user)

    def save(self, *args, **kwargs):
        """Override save to generate the token before saving and set expiration."""
        if not self.token:  # Only generate the token if it hasn't been set
            self.generate_token()
        if not self.expired_at:
            self.expired_at = timezone.now() + timezone.timedelta(minutes=15)  # Token expires in 15 minutes
        super().save(*args, **kwargs)