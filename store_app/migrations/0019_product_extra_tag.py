# Generated by Django 3.2.8 on 2021-12-06 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0018_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='extra_tag',
            field=models.CharField(choices=[('WOMEN', 'WOMEN'), ('MEN', 'MEN'), ('KIDS', 'KIDS')], default='WOMEN', max_length=256),
        ),
    ]
