# Generated by Django 3.0.7 on 2020-07-09 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_auto_20200709_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='county',
            field=models.CharField(blank=True, default='', max_length=80, null=True),
        ),
    ]
