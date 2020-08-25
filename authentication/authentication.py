from users.models import User
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrPhoneModelBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        try:
             user = User.objects.get(phone_number=username)
             pwd_valid = user.check_password(password)
             if pwd_valid:
                 return user
             return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None