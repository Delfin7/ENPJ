from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Questions(models.Model):
    question = models.TextField()
    answer_a = models.TextField()
    answer_b = models.TextField()
    answer_c = models.TextField()
    question_eng = models.TextField()
    answer_a_eng = models.TextField()
    answer_b_eng = models.TextField()
    answer_c_eng = models.TextField()
    question_de = models.TextField()
    answer_a_de = models.TextField()
    answer_b_de = models.TextField()
    answer_c_de = models.TextField()
    answer_correct = models.CharField(max_length=1)
    media = models.CharField(max_length=200)
    type = models.CharField(max_length=15)
    points = models.IntegerField()
    categories = models.CharField(max_length=30)
    module = models.CharField(max_length=4)
    source = models.TextField()
    pjm_question = models.CharField(max_length=200)
    pjm_answer_a = models.CharField(max_length=200)
    pjm_answer_b = models.CharField(max_length=200)
    pjm_answer_c = models.CharField(max_length=200)

    class Meta:
        db_table = "questions"


class Exam(models.Model):
    points = models.IntegerField(blank=True, null=True)
    status = models.CharField(default='ROZPOCZETY', max_length=10)
    category = models.CharField(max_length=2)
    id_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "exam"


class ExamQuestions(models.Model):
    id_exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    id_question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, blank=True, null=True)
    question_number = models.IntegerField()
    time_left = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "exam_questions"


class Options(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(default='PL', max_length=3)
    sign_language = models.BooleanField(default=False)

    class Meta:
        db_table = "options"
