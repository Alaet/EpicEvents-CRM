from django.db import migrations


def apply_migration(apps, schema_editor):

    group = apps.get_model('auth', 'Group')
    group.objects.bulk_create([
        group(name=u'SalesTeam'),
        group(name=u'SupportTeam'),
    ])


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
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)

    ]
