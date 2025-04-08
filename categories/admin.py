from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('parent',)


admin.site.register(Category, CategoryAdmin)
