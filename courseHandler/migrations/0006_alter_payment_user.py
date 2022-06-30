# Generated by Django 4.0.4 on 2022-06-13 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0001_initial'),
        ('courseHandler', '0005_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payment_user', to='userAuth.usertype'),
        ),
    ]