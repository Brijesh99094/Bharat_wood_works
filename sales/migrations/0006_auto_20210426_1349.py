# Generated by Django 3.0.7 on 2021-04-26 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_auto_20210318_1920'),
        ('sales', '0005_auto_20210312_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='sales_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Customer'),
        ),
    ]
