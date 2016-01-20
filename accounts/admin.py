from django.contrib import admin
from accounts.models import UsageToken
# Register your models here.

class UsageTokenAdmin(admin.ModelAdmin):
    exclude = ('token',)
admin.site.register(UsageToken, UsageTokenAdmin)

