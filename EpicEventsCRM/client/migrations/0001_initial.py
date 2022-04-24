# Generated by Django 4.0.3 on 2022-04-23 18:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25, null=True)),
                ('last_name', models.CharField(max_length=25, null=True)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('mobile', models.CharField(max_length=20, null=True)),
                ('company_name', models.CharField(max_length=250, null=True, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('prospect', models.BooleanField(default=True)),
                ('sales_contact', models.ForeignKey(limit_choices_to={'groups': 'sales'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales_contact', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
