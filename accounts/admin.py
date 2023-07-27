from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from.models import Account

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display =('username','email', 'first_name', 'last_name','date_joined', 'is_active', 'last_login' )
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('date_joined', )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering= ('username',)
admin.site.register(Account, AccountAdmin)
