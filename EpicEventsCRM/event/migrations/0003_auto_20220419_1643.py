from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import migrations

from client.models import Client
from contract.models import Contract
from event.models import Event


def apply_migration(apps, schema_editor):

    group = apps.get_model('auth', 'Group')
    perm = apps.get_model('auth', 'Permission')
    support = group.objects.get(name='SupportTeam')

    support_perm = perm.objects.get(codename='view_client')
    support_event_perm = Permission.objects.filter(codename__in=('change_event', 'view_event'))
    support.permissions.add(support_perm)
    for p in support_event_perm:
        support.permissions.add(p)

    sales = group.objects.get(name='SalesTeam')
    sales_event_perm = perm.objects.filter(codename__in=(
        'change_event', 'view_event', 'add_event', 'delete_event',
        'add_client', 'view_client', 'change_client', 'delete_client',
        'add_contract', 'view_contract', 'change_contract', 'delete_contract',))
    for p in sales_event_perm:
        sales.permissions.add(p)
    """for model, content_type in ct.items():
        sales_perm = perm.objects.filter(content_type=content_type)
        for p in sales_perm:
            sales.permissions.add(p)"""


def revert_migration(apps, schema_editor):
    group = apps.get_model('auth', 'Group')
    group.objects.filter(
        name__in=[
            u'SalesTeam',
            u'SupportTeam',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20220419_1616'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)

    ]
