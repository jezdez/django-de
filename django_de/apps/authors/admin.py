from django.contrib import admin
from django_de.apps.authors.models import Author

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'url')
    search_fields = ('name', 'bio')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Author, AuthorAdmin)
