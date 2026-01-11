import random
from django.db import models # type: ignore
from datetime import timedelta
from django.utils import timezone # type: ignore
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin,BaseUserManager) # type: ignore

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, phone_number=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        if not full_name:
            raise ValueError("Full name must be set")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.is_active = True  # allow login by default
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_type_choices = (
        ('individuals', 'individuals'),
        ('company', 'company'),
    )
    email = models.EmailField(unique=True, db_index=True)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True
    )
    user_type = models.CharField(max_length=20, choices=user_type_choices, default='individuals')
    address = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=150, blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    company_vat_number = models.CharField(max_length=50, blank=True, null=True)
    

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.full_name

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name.split()[0]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user_auth_customuser"


class PasswordResetCode(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_auth_passwordresetcode"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"{random.randint(100000, 999999)}"
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.created_at + timedelta(minutes=2) < timezone.now()