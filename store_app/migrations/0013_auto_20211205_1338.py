# Generated by Django 3.2.8 on 2021-12-05 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0012_product_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=256)),
                ('code', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='available_colors',
            field=models.ManyToManyField(to='store_app.CustomColor'),
        ),
    ]
