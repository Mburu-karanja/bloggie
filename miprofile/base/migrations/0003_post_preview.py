# Generated by Django 3.1.5 on 2024-08-02 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20240801_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='preview',
            field=models.TextField(blank=True, help_text='Short preview of the post content'),
        ),
    ]
