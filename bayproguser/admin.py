## Copyright 2021, J. Donald Tillman.  All rights reserved.

from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from bayproguser.models import BayProgUser

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = BayProgUser
        fields = ('email', 'firstname', 'lastname', 'about', 'image')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = BayProgUser
        fields = ('email', 'firstname', 'lastname', 'about', 'image')

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'firstname', 'lastname', 'is_admin', 'image')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ('firstname', 'lastname', 'about', 'image',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'password1', 'password2',)}),
    )
    search_fields = ('email',)
    ordering = ('lastname', 'firstname',)
    filter_horizontal = ()

admin.site.register(BayProgUser, UserAdmin)
admin.site.unregister(Group)


