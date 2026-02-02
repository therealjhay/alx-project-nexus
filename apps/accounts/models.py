import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    class UserRole(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        EMPLOYER = 'EMPLOYER', _('Employer')
        JOB_SEEKER = 'JOB_SEEKER', _('Job Seeker')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        max_length=20, 
        choices=UserRole.choices, 
        default=UserRole.JOB_SEEKER
    )

    # We use email as the login identifier, not username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email