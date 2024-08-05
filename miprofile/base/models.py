from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = MarkdownxField()
    preview = models.TextField(blank=True, help_text="Short preview of the post content")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)

    def formatted_markdown(self):
        return markdownify(self.content)

    def save(self, *args, **kwargs):
        # Generate preview if not provided
        if not self.preview:
            self.preview = self.content[:500]  # Example preview length (first 500 characters)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


