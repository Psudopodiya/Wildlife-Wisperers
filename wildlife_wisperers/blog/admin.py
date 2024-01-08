from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Comment, CustomUser, Blog
from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Comment)
admin.site.register(Blog)
