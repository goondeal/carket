from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager
from management.models import City


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    date_of_birth = models.DateField(null=True)
    city = models.ForeignKey(
        City, on_delete=models.PROTECT, related_name='users')

    _GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=2, choices=_GENDER_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'phone', 'city')

    objects = CustomUserManager()

    @property
    def age(self):
        td = datetime.now() - self.data_of_birth
        return td.days

    def __str__(self):
        return f'{self.get_full_name()} ({self.phone})'
