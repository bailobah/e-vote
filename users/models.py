from django.contrib.auth.decorators import login_required
from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class Role(models.Model):
    PRESIDENT = 1
    VICE_PRRESIDENT = 2
    ADMIN_PREFECTORAL = 3
    ADMIN_S_PREFECTORAL = 4
    ADMIN_DISTRICT = 5
    ADMIN_BV = 6

    ROLE_CHOICES = {
        (PRESIDENT, 'PRESIDENT'),
        (VICE_PRRESIDENT, 'VICE PRESIDENT'),
        (ADMIN_PREFECTORAL, 'ADMIN PREFECTORAL'),
        (ADMIN_S_PREFECTORAL, 'ADMIN SOUS PREFECTORAL'),
    }

    id = models.PositiveIntegerField(choices = ROLE_CHOICES, primary_key = True)

    def __str__(self):
        return self.get_id_display()


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=150,  unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )

    roles = models.ManyToManyField(Role)
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.phone_number)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    about = models.TextField(default='', blank=True)
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    code_postal = models.CharField(max_length=100, default='', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

