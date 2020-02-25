from django.contrib.auth.models import AbstractUser
from django_paranoid.models import ParanoidModel


class User(ParanoidModel, AbstractUser):
    pass
