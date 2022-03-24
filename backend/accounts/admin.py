from django.contrib import admin
from django.contrib.auth import get_user_model
from django.forms import TextInput
from django.db import models
from django.contrib.auth.models import Group

User = get_user_model()

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'first_name', 'last_name')
    list_display_links = ('phone_number',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'autocomplete': 'off', 'class': 'vTextField'})},
    }
    fields = (
        ('first_name', 'last_name'),
        'phone_number', 'email', 'password', 'chat_id',
        ('date_joined', 'last_login'),
        'is_active',)
