from django.contrib import admin
from .models import Post, Category
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Category)
