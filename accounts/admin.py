from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin, AdminPasswordChangeForm

from .forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


class UserAdminCustom(UserAdmin):
    model = User
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    change_password_form = AdminPasswordChangeForm
    readonly_fields = ['date_joined']
    list_display = ('email', 'full_name', 'date_joined')
    list_filter = (
        'is_active', 'is_connected', 'is_client', 'is_operator', 'is_doctor',
        'is_staff', 'is_superuser', 'groups')
    search_fields = ('id', 'email', 'first_name', 'last_name', 'personal_id')
    ordering = ('email', 'date_joined')
    filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = (
        ('Account', {
            'fields': ('email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'phone')
        }),
        ('Sensitive Data', {
            'fields': ('personal_id',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_connected', 'is_client', 'is_operator',
                       'is_doctor', 'is_staff', 'is_superuser',
                       # the PermissionMixins
                       'groups', 'user_permissions')
        })
    )
    add_fieldsets = (
        (None, {
            'fields': (
                'email', 'password1', 'password2', 'first_name',
                'last_name', 'phone', 'personal_id')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_connected', 'is_client', 'is_operator',
                       'is_doctor', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')
        })
    )


admin.site.register(User, UserAdminCustom)
