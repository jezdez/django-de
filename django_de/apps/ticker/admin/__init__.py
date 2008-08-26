from django.contrib import admin
from django_de.apps.ticker.models import Entry

class EntryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Entry, EntryAdmin)