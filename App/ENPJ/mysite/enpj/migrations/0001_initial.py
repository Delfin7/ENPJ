# Generated by Django 4.1 on 2022-12-27 23:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(default='ROZPOCZETY', max_length=10)),
                ('category', models.CharField(max_length=2)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'exam',
            },
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer_a', models.TextField()),
                ('answer_b', models.TextField()),
                ('answer_c', models.TextField()),
                ('question_eng', models.TextField()),
                ('answer_a_eng', models.TextField()),
                ('answer_b_eng', models.TextField()),
                ('answer_c_eng', models.TextField()),
                ('question_de', models.TextField()),
                ('answer_a_de', models.TextField()),
                ('answer_b_de', models.TextField()),
                ('answer_c_de', models.TextField()),
                ('answer_correct', models.CharField(max_length=1)),
                ('media', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=15)),
                ('points', models.IntegerField()),
                ('categories', models.CharField(max_length=30)),
                ('module', models.CharField(max_length=4)),
                ('source', models.TextField()),
                ('pjm_question', models.CharField(max_length=200)),
                ('pjm_answer_a', models.CharField(max_length=200)),
                ('pjm_answer_b', models.CharField(max_length=200)),
                ('pjm_answer_c', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'questions',
            },
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(default='PL', max_length=3)),
                ('sign_language', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'options',
            },
        ),
        migrations.CreateModel(
            name='ExamQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=1, null=True)),
                ('question_number', models.IntegerField()),
                ('time_left', models.IntegerField(blank=True, null=True)),
                ('id_exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enpj.exam')),
                ('id_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enpj.questions')),
            ],
            options={
                'db_table': 'exam_questions',
            },
        ),
    ]