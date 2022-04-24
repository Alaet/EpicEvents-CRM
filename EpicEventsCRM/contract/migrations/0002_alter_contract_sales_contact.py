# Generated by Django 4.0.3 on 2022-04-23 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contract', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='sales_contact',
            field=models.ForeignKey(limit_choices_to={'team': 'sales'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales_contact_contract', to=settings.AUTH_USER_MODEL),
        ),
    ]