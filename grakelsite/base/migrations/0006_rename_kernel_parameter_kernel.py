# Generated by Django 4.1.1 on 2022-09-28 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_kernel_parameter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parameter',
            old_name='Kernel',
            new_name='kernel',
        ),
    ]