from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.validators import *
from utils.upload import *

class MainUser(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id}: {self.username}'


class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, null=True)
    address = models.CharField(max_length=300, null=True)
    avatar = models.FileField(upload_to=avatar_document_path,
                              validators=[validate_file_size, validate_extension],
                              null=True)

    def __str__(self):
        return self.user.username