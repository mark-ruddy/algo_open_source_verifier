# Generated by Django 4.0.6 on 2022-08-08 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='verifiedcontract',
            old_name='approval_teal_url',
            new_name='approval_url',
        ),
    ]
