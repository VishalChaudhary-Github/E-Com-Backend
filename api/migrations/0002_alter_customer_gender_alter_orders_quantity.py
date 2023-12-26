# Generated by Django 5.0 on 2023-12-22 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], max_length=1),
        ),
        migrations.AlterField(
            model_name='orders',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]