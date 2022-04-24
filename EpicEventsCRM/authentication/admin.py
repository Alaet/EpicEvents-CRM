from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission

from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ("username", "first_name", "last_name", "email", "team")


class UserAdmin(admin.ModelAdmin):
    form = CustomUserCreationForm
    list_display = ("id", "username", "first_name", "last_name", "email")

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            obj.is_staff = True
            obj.save()
            if obj.team == 'support':
                support_perm = Permission.objects.get(codename='view_client')
                support_event_perm = Permission.objects.filter(codename__in=('change_event', 'view_event'))
                obj.user_permissions.add(support_perm)
                for p in support_event_perm:
                    obj.user_permissions.add(p)
            if obj.team == 'sales':
                sales_perm = Permission.objects.filter(codename__in=(
                    'change_event', 'view_event', 'add_event', 'delete_event',
                    'add_client', 'view_client', 'change_client', 'delete_client',
                    'add_contract', 'view_contract', 'change_contract', 'delete_contract',))
                for p in sales_perm:
                    obj.user_permissions.add(p)


admin.site.register(User, UserAdmin)
