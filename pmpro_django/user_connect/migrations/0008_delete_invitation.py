# Generated by Django 4.2.3 on 2023-09-01 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_connect', '0007_alter_invitation_property_alter_invitation_tenant_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Invitation',
        ),
    ]
