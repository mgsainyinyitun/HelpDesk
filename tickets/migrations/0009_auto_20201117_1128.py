# Generated by Django 3.1.1 on 2020-11-17 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0008_tickets_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.category'),
        ),
    ]
