# Generated by Django 3.0.6 on 2020-10-20 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20201020_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Area'),
        ),
    ]