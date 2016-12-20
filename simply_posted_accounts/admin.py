from django.contrib import admin
from simply_posted_accounts.models import UserProfile, UserProfileAdmin

admin.site.register(UserProfile, UserProfileAdmin)
