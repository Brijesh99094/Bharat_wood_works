# Generated by Django 3.0.6 on 2021-04-03 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0015_auto_20210329_1658'),
        ('dispatch', '0007_dispatch'),
    ]

    operations = [
        migrations.CreateModel(
            name='DispatchDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(null=True)),
                ('dispatch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dispatch.Dispatch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.Product')),
            ],
        ),
    ]
