# Generated by Django 4.1.1 on 2022-09-28 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_rename_dataset_evaluation_dataset_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='normalize',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='rbf',
            field=models.BooleanField(),
        ),
    ]
