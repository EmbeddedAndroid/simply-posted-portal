from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Simply Posted User Profiles'
        verbose_name_plural = 'Simply Posted User Profiles'


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'first_name', 'last_name')