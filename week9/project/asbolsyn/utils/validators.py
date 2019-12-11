import os
from django.core.exceptions import ValidationError
from utils.constants import PROFILE_IMAGE_ALLOWED_EXTS


def profile_image_size(value):
    if value.size > 1024*1024*5:
        raise ValidationError('Invalid file size')


def profile_image_extension(value):
    ext = os.path.splitext(value.name)[1]

    if not ext.lower() in PROFILE_IMAGE_ALLOWED_EXTS:
        raise ValidationError(f'Not allowed extension, allowed ({PROFILE_IMAGE_ALLOWED_EXTS})')
