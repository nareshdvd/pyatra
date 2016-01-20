from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from yatra_app.models import Category, VideoTemplate, Steaker

class CategoryAdmin(admin.ModelAdmin):
    pass


class VideoTemplateAdmin(admin.ModelAdmin):
    pass

class SteakerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(VideoTemplate, MPTTModelAdmin)
admin.site.register(Steaker, SteakerAdmin)
