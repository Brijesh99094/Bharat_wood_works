# Generated by Django 3.0.7 on 2020-11-10 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sales',
            old_name='account',
            new_name='sales_user',
        ),
        migrations.RenameField(
            model_name='salesreturn',
            old_name='account',
            new_name='sales_user',
        ),
    ]
