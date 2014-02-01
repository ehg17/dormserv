from django.contrib import admin
# Import the UserProfile model individually.
from users.models import UserProfile
from django.contrib.auth.models import User

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'user','dorm','room',)


admin.site.register(UserProfile, UserProfileAdmin)

