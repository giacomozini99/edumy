# Generated by Django 4.0.4 on 2022-05-20 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userAuth', '0001_initial'),
        ('courseHandler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('body', models.CharField(max_length=1024)),
                ('rating', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='review_course', to='courseHandler.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='review_user', to='userAuth.usertype')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=1024)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='question_user', to='userAuth.usertype')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='question_video', to='courseHandler.video')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=1024)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='answer_user', to='userAuth.usertype')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='answer_question', to='userInteractions.question')),
            ],
        ),
    ]