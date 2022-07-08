# Generated by Django 4.0.4 on 2022-07-08 07:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0002_usertype_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertype',
            name='image',
            field=models.FileField(default='/imgs/default.jpg', upload_to='imgs', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'svg', 'jpeg'])]),
        ),
    ]