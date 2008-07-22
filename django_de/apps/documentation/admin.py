from django.contrib import admin
from django_de.apps.documentation.models import Release

class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("version", "release_date")

admin.site.register(Release, ReleaseAdmin)
