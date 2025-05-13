from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # To show your new fields in the user admin form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('city', 'state', 'address', 'phone')}),
    )
    # To show your new fields when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('city', 'state', 'address', 'phone')}),
    )


admin.site.register(CustomUser,CustomUserAdmin)