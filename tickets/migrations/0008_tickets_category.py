# Generated by Django 3.1.1 on 2020-11-17 04:56

from django.db import migrations, models
import tickets.models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='category',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name=tickets.models.Category),
        ),
    ]
