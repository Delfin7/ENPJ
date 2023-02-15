import django.http

from ..models import Questions, ExamQuestions, Exam, Options
from django.contrib.auth.models import User


def generate_questions(category1, category2):
    Questions.objects.create(id=1, categories=category1, points=1, type="PODSTAWOWY")
    Questions.objects.create(id=2, categories=category2, points=1, type="PODSTAWOWY")
    Questions.objects.create(id=3, categories="," + category1, points=1, type="PODSTAWOWY")
    Questions.objects.create(id=4, categories="," + category2, points=1, type="PODSTAWOWY")
    Questions.objects.create(id=5, categories=category2 + "," + category1, points=1, type="PODSTAWOWY")
    Questions.objects.create(id=6, categories=category1 + ",", points=1, type="PODSTAWOWY")
    Questions.objects.create(id=7, categories=category2 + ",", points=1, type="PODSTAWOWY")
    for i in range(6):
        Questions.objects.create(id=8 + i, categories=category1 + "," + category2, points=2, type="PODSTAWOWY")
    for i in range(10):
        Questions.objects.create(id=14 + i, categories=category1 + "," + category2, points=3, type="PODSTAWOWY")

    Questions.objects.create(id=24, categories=category1, points=2, type="SPECJALISTYCZNY")
    Questions.objects.create(id=25, categories=category2, points=2, type="SPECJALISTYCZNY")
    Questions.objects.create(id=26, categories="," + category1, points=2, type="SPECJALISTYCZNY")
    Questions.objects.create(id=27, categories="," + category2, points=2, type="SPECJALISTYCZNY")
    Questions.objects.create(id=28, categories=category2 + "," + category1, points=2, type="SPECJALISTYCZNY")
    Questions.objects.create(id=29, categories=category1 + ",", points=2, type="SPECJALISTYCZNY")
    Questions.objects.create(id=30, categories=category2 + ",", points=2, type="SPECJALISTYCZNY")
    for i in range(6):
        Questions.objects.create(id=31 + i, categories=category1 + "," + category2, points=3, type="SPECJALISTYCZNY")
    for i in range(2):
        Questions.objects.create(id=37 + i, categories=category1 + "," + category2, points=1, type="SPECJALISTYCZNY")


def generate_pjm_questions():
    for i in range(10):
        Questions.objects.create(id=i + 1, categories="B", points=3, type="PODSTAWOWY", pjm_question="tak")
        Questions.objects.create(categories="B", points=3, type="PODSTAWOWY")
    for i in range(6):
        Questions.objects.create(id=i + 11, categories="B", points=2, type="PODSTAWOWY", pjm_question="tak")
        Questions.objects.create(categories="B", points=2, type="PODSTAWOWY")
        Questions.objects.create(id=i + 17, categories="B", points=3, type="SPECJALISTYCZNY", pjm_question="tak")
        Questions.objects.create(categories="B", points=3, type="SPECJALISTYCZNY")
    for i in range(4):
        Questions.objects.create(id=i + 23, categories="B", points=1, type="PODSTAWOWY", pjm_question="tak")
        Questions.objects.create(categories="B", points=1, type="PODSTAWOWY")
        Questions.objects.create(id=i + 27, categories="B", points=2, type="SPECJALISTYCZNY", pjm_question="tak")
        Questions.objects.create(categories="B", points=2, type="SPECJALISTYCZNY")
    for i in range(2):
        Questions.objects.create(id=i + 31, categories="B", points=1, type="SPECJALISTYCZNY", pjm_question="tak")
        Questions.objects.create(categories="B", points=1, type="SPECJALISTYCZNY")


def generate_request(name="Test"):
    request = django.http.HttpRequest()
    request.user = User.objects.create_user(name)
    return request


def generate_unauthenticated_request():
    class MockUser:
        is_authenticated = False
    request = django.http.HttpRequest()
    request.user = MockUser()
    return request


def generate_exam_and_request(status="ROZPOCZETY", points=None, category=""):
    request = generate_request()
    exam = Exam.objects.create(id=1, id_user=request.user, status=status, points=points, category=category)
    return request, exam


def generate_next_questions(answer=None, next_question=True):
    request, exam = generate_exam_and_request()
    question = Questions.objects.create(id=1, points=1, answer_correct="A")
    ExamQuestions.objects.create(id=1, id_exam=exam, id_question=question, question_number=1, answer=answer,
                                 time_left=10)
    if next_question:
        ExamQuestions.objects.create(id=2, id_exam=exam, id_question=question, question_number=2)
    return request, exam


def generate_exam_and_questions():
    generate_questions("A", "A1")
    exam = generate_exam_and_request()[1]
    return exam


def generate_finished_exams(exams_count=1, category="A"):
    request = generate_request()
    for i in range(exams_count):
        if i % 2 == 0:
            points = 72
        else:
            points = 60
        Exam.objects.create(id=i + 1, id_user=request.user, status="ZAKONCZONY", points=points,
                                   category=category, end_date="2022-10-" + str(i + 1))
    return request


def generate_options(language="PL", sign_language=False):
    request = generate_request()
    Options.objects.create(user=request.user, language=language, sign_language=sign_language)
    return request
