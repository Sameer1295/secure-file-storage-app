from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from customuser.views import generate_ecc_key_pair

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username"]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2',),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        generate_ecc_key_pair(obj)
    
admin.site.register(CustomUser, CustomUserAdmin)