from django.contrib import admin
from django_de.apps.jobboard.models import Entry 

class EntryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'job_type',
        'verified',
        'published',
    )

admin.site.register(Entry, EntryAdmin)