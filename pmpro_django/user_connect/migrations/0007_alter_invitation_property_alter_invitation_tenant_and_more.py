# Generated by Django 4.2.3 on 2023-08-31 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_base', '0001_initial'),
        ('user_auth', '0004_remove_landlord_user_remove_tenant_property_and_more'),
        ('user_connect', '0006_alter_invitation_property_alter_invitation_tenant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='property',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_base.property'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='tenant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_base.tenant'),
        ),
        migrations.AlterField(
            model_name='message',
            name='property',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_base.property'),
        ),
        migrations.DeleteModel(
            name='Property',
        ),
    ]
