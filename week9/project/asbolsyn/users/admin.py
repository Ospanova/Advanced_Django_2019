from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import MainUser, Profile


class MyProfile(admin.StackedInline):
    model = Profile
    verbose_name = 'Profile'
    verbose_name_plural = 'Profiles'
    can_delete = False


@admin.register(MainUser)
class MainUserAdmin(admin.ModelAdmin):
    inlines = [MyProfile, ]
    list_display = ('id', 'phone', 'role', 'is_superuser', 'is_active')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'image_url', )


# from django.contrib import admin
# from users.models import MainUser, Profile
# from django.contrib.auth.admin import UserAdmin
#
#
# class InlineProfile(admin.StackedInline):
#     model = Profile
#     verbose_name = 'Profile'
#     verbose_name_plural = 'Profiles'
#     can_delete = False
#
#
# @admin.register(MainUser)
# class MainUserAdmin(UserAdmin):
#     inlines = [InlineProfile,]
#
#
# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('id', 'bio', 'address', 'user',)