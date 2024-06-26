# Generated by Django 4.0 on 2024-05-16 05:29
from django.contrib.auth.models import Permission, User, Group
from django.contrib.contenttypes.models import ContentType
from django.db import migrations


def add_user_moderator_permission(apps, schema_editor):
    content_type = ContentType.objects.get_for_model(User)
    group, created = Group.objects.get_or_create(name='Модератор')
    existing_permissions = Permission.objects.filter(content_type=content_type, codename='user_moderator')

    if not existing_permissions.exists():
        Permission.objects.create(
            codename='user_moderator',
            name='Модератор',
            content_type=content_type,
        )
    group.permissions.add(*existing_permissions)


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0006_alter_payment_amount'),
    ]

    operations = [
        migrations.RunPython(add_user_moderator_permission)
    ]
