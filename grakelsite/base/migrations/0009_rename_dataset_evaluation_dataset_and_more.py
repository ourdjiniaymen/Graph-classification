# Generated by Django 4.1.1 on 2022-09-28 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_evaluation_result'),
    ]

    operations = [
        migrations.RenameField(
            model_name='evaluation',
            old_name='Dataset',
            new_name='dataset',
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='normalize',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='rbf',
            field=models.IntegerField(),
        ),
    ]
