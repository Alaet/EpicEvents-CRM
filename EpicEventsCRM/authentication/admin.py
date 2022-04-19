from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ("username", "first_name", "last_name", "email", "groups")


class UserAdmin(admin.ModelAdmin):
    form = CustomUserCreationForm
    list_display = ("id", "username", "first_name", "last_name", "email")

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            obj.is_staff = True
            obj.save()


admin.site.register(User, UserAdmin)
