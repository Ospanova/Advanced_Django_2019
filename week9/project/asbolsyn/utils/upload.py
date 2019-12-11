def profile_image_path(instance, filename):
    user_id = instance.user.id
    return f'images/profile/{user_id}/{filename}'
