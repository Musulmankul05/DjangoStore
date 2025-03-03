from django.contrib.auth.backends import ModelBackend
from .models import UserModel


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
            else:
                return None
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id: int):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
