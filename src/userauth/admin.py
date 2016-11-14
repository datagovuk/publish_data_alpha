from django.utils.translation import ugettext as _

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from userauth.models import PublishingUser

class UserAdmin(BaseUserAdmin):
    model = PublishingUser
    fieldsets = (
        (None, {'fields': ('email', 'apikey')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1',
                       'password2')}
         ),
    )


print("Registering user admin")

admin.site.register(PublishingUser, UserAdmin)