from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(
            self, first_name, last_name, phone_number,is_staff, active, created_at,updated_at, password=None,
        commit=True):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        if not phone_number:
            raise ValueError(_('Users must have an email address or phone number'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            is_staff=is_staff,
            active=active,
            created_at=created_at,
            updated_at=updated_at,
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

        def create_superuser(self, first_name, last_name, password):
            """
            Creates and saves a superuser with the given email, first name,
            last name and password.
            """
            user = self.create_user(
                password=password,
                first_name=first_name,
                last_name=last_name,
                commit=False,
            )
            user.is_staff = True
            user.is_superuser = True
            user.save(using=self._db)
            return user

