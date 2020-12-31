from django import forms
from django.contrib.auth.forms import (ReadOnlyPasswordHashField,
                                       UserCreationForm, UserChangeForm, )
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdminCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'
        field_classes = {}


class UserAdminChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        field_classes = {}


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'personal_id')
        field_classes = {}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_client = True
        if commit:
            user.save()
        return user
