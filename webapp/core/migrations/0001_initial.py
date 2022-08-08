# Generated by Django 4.0.6 on 2022-08-08 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VerifiedContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_type', models.CharField(max_length=64)),
                ('approval_teal_url', models.CharField(max_length=65536)),
                ('clear_state_url', models.CharField(max_length=65536)),
                ('app_id', models.CharField(max_length=9)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
