# Generated by Django 3.0.7 on 2021-03-07 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_salesreturn_sales'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesreturn_has_product',
            name='price',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
