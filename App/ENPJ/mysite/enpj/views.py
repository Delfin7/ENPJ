from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.template import loader
from django.db.models import Q
import random
from datetime import datetime, timedelta, date
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Questions, Exam, ExamQuestions, Options


def draw_questions(category, sign_language):
    category_contain = category + ','
    if sign_language and category in ("B", "C"):
        questions_primary_query = (Questions.objects.filter(~Q(pjm_question="")).filter(type="PODSTAWOWY")
            .filter(points=3).filter(Q(categories__endswith=category) | Q(categories__contains=category_contain))
            .order_by("?")[:10].only("id").union(Questions.objects.filter(~Q(pjm_question="")).filter(type="PODSTAWOWY")
            .filter(points=2).filter(Q(categories__endswith=category) | Q(categories__contains=category_contain))
            .order_by("?")[:6].only("id")).union(Questions.objects.filter(~Q(pjm_question="")).filter(type="PODSTAWOWY")
            .filter(points=1).filter(Q(categories__endswith=category) | Q(categories__contains=category_contain))
            .order_by("?")[:4].only("id")))

        questions_spec_query = (Questions.objects.filter(~Q(pjm_question="")).filter(type="SPECJALISTYCZNY")
            .filter(points=3).filter(Q(categories__endswith=category) | Q(categories__contains=category_contain))
            .order_by("?")[:6].only("id")).union(Questions.objects.filter(~Q(pjm_question=""))
            .filter(type="SPECJALISTYCZNY").filter(points=2)
            .filter(Q(categories__endswith=category) | Q(categories__contains=category_contain))
            .order_by("?")[:4].only("id")).union(Questions.objects.filter(~Q(pjm_question=""))
            .filter(type="SPECJALISTYCZNY").filter(points=1)
            .filter(Q(categories__endswith=category) | Q(categories__contains=category_contain))
            .order_by("?")[:2].only("id"))
    elif category == "T":
        questions_primary_query = (Questions.objects.filter(type="PODSTAWOWY").filter(points=3)
        .filter(Q(categories__endswith=",T") | Q(categories__contains=",T,") | Q(categories__startswith="T"))
        .order_by("?")[:10].only("id").union(Questions.objects.filter(type="PODSTAWOWY")
        .filter(points=2)
        .filter(Q(categories__endswith=",T") | Q(categories__contains=",T,") | Q(categories__startswith="T"))
        .order_by("?")[:6].only("id")).union(Questions.objects.filter(type="PODSTAWOWY").filter(points=1)
        .filter(Q(categories__endswith=",T") | Q(categories__contains=",T,") | Q(categories__startswith="T"))
        .order_by("?")[:4].only("id")))

        questions_spec_query = (Questions.objects.filter(type="SPECJALISTYCZNY").filter(points=3)
        .filter(Q(categories__endswith=",T") | Q(categories__contains=",T,") | Q(categories__startswith="T"))
        .order_by("?")[:6].only("id")).union(Questions.objects.filter(type="SPECJALISTYCZNY").filter(points=2)
        .filter(Q(categories__endswith=",T") | Q(categories__contains=",T,") | Q(categories__startswith="T"))
        .order_by("?")[:4].only("id")).union(Questions.objects.filter(type="SPECJALISTYCZNY").filter(points=1)
        .filter(Q(categories__endswith=",T") | Q(categories__contains=",T,") | Q(categories__startswith="T"))
        .order_by("?")[:2].only("id"))
    else:
        questions_primary_query = (Questions.objects.filter(type="PODSTAWOWY").filter(points=3)
            .filter(Q(categories__endswith=category) | Q(categories__contains=category_contain))
            .order_by("?")[:10].only("id").union(Questions.objects.filter(type="PODSTAWOWY")
            .filter(points=2).filter(Q(categories__endswith=category) | Q(categories__contains=category_contain))
            .order_by("?")[:6].only("id")).union(Questions.objects.filter(type="PODSTAWOWY").filter(points=1)
            .filter(Q(categories__endswith=category) | Q(categories__contains=category_contain))
            .order_by("?")[:4].only("id")))

        questions_spec_query = (Questions.objects.filter(type="SPECJALISTYCZNY").filter(points=3)
            .filter(Q(categories__endswith=category) | Q(categories__contains=category_contain)).order_by("?")[:6]
            .only("id")).union(Questions.objects.filter(type="SPECJALISTYCZNY").filter(points=2)
            .filter(Q(categories__endswith=category) | Q(categories__contains=category_contain)).order_by("?")[:4]
            .only("id")).union(Questions.objects.filter(type="SPECJALISTYCZNY").filter(points=1)
            .filter(Q(categories__endswith=category) | Q(categories__contains=category_contain)).order_by("?")[:2]
            .only("id"))

    primary_question_list = [i.id for i in questions_primary_query]
    spec_question_list = [i.id for i in questions_spec_query]

    random.shuffle(primary_question_list)
    random.shuffle(spec_question_list)
    questions_list = primary_question_list + spec_question_list
    return questions_list


def exam_next_question(request):
    if not request.user.is_authenticated:
        return HttpResponse('401 Unauthorized', status=401)
    answer = request.POST.get('answer', None)
    exam_id = request.POST.get('examId', None)
    question_id = request.POST.get('questionId', None)
    question_number = request.POST.get('questionNumber', None)
    exam_finished = request.POST.get('end', False)
    time = request.POST.get('time', None)

    exam_question = ExamQuestions.objects.filter(id=question_id)[0]
    if exam_question.answer is not None:
        return HttpResponseNotFound()
    exam_question.answer = answer
    exam_question.save()

    if question_number == '32' or exam_finished:
        end_exam(exam_id)
    else:
        exam_next_question = ExamQuestions.objects.filter(id=int(question_id) + 1)[0]
        exam_next_question.time_left = time
        exam_next_question.save()
    return HttpResponse()


def generate_questions(exam_id, sign_language):
    draw = draw_questions(exam_id.category, sign_language)
    for i in range(32):
        if i == 0:
            ExamQuestions.objects.create(id_exam=exam_id, question_number=i + 1, id_question_id=draw[i], time_left=1500)
        else:
            ExamQuestions.objects.create(id_exam=exam_id, question_number=i + 1, id_question_id=draw[i])


@login_required(login_url='/login')
def check_active_exams(request):
    check = check_endless_exams(request.user)
    if check:
        return JsonResponse({'info': check})
    else:
        return JsonResponse({'info': False})


@login_required(login_url='/login')
def cancel_exam(request):
    if request.POST.get('cancel', False):
        exam = Exam.objects.filter(status="ROZPOCZETY", id_user=request.user)[0]
        exam.status = "ANULOWANY"
        exam.end_date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
        exam.save()
        return HttpResponse()
    else:
        return HttpResponseNotFound()


@login_required(login_url='/login')
def generate_exam(request):
    category = request.POST.get('category', None)
    exam_instance = Exam.objects.create(points=None, category=category, id_user=request.user)
    config = check_options(request.user)
    generate_questions(exam_instance, config["signLanguage"])
    return HttpResponse()


def next_question(user):
    return ExamQuestions.objects.filter(answer=None).select_related('id_exam').filter(id_exam__status='ROZPOCZETY',
                                                                                      id_exam__id_user=user)


def increment_question_number(question_number):
    if question_number <= 20:
        return [question_number, 0]
    else:
        return [20, question_number - 20]


def check_media(media):
    if media == '':
        return "brak_zdjecia_1024x576.jpg"
    else:
        return media


def check_endless_exams(user):
    exam = Exam.objects.filter(status="ROZPOCZETY", id_user=user)
    if exam:
        return exam[0].id
    else:
        return False


def count_points(exam_id):
    exam_questions = ExamQuestions.objects.filter(id_exam=exam_id).select_related('id_question').values(
        'id_question_id__points', 'id_question_id__answer_correct', 'answer')
    points = 0
    for i in exam_questions:
        if i['id_question_id__answer_correct'] == i['answer']:
            points += i['id_question_id__points']
    return points


def check_correct_answers(exam_id):
    exam_questions = ExamQuestions.objects.filter(id_exam=exam_id).select_related('id_question').values(
        'id_question_id__answer_correct', 'answer', 'question_number')
    return [i['question_number'] for i in exam_questions if i['id_question_id__answer_correct'] == i['answer']]


def end_exam(exam_id):
    exam = Exam.objects.filter(id=exam_id)[0]
    exam.status = "ZAKONCZONY"
    exam.end_date = datetime.now(tz=timezone.utc)
    exam.points = count_points(exam_id)
    exam.save()


def format_time(seconds):
    return str(seconds // 60).zfill(2) + ':' + str(seconds % 60).zfill(2)


def get_graph_data(user, category):
    points, end_time = [], []
    if category == "W":
        exam = Exam.objects.filter(status="ZAKONCZONY", id_user=user).order_by('-end_date')[:20]
    else:
        exam = Exam.objects.filter(status="ZAKONCZONY", id_user=user, category=category).order_by('-end_date')[:20]
    for data in exam:
        points.append(data.points)
        end_time.append(str(data.end_date)[:19])
    return points, end_time


def get_exam_language(user, question):
    config = check_options(user)
    if config["language"] == "ENG":
        question_content = question.question_eng
        answer_a = question.answer_a_eng
        answer_b = question.answer_b_eng
        answer_c = question.answer_c_eng
    elif config["language"] == "DE":
        question_content = question.question_de
        answer_a = question.answer_a_de
        answer_b = question.answer_b_de
        answer_c = question.answer_c_de
    else:
        question_content = question.question
        answer_a = question.answer_a
        answer_b = question.answer_b
        answer_c = question.answer_c

    if config["signLanguage"]:
        sign_language_question = question.pjm_question
        sign_language_answer_a = question.pjm_answer_a
        sign_language_answer_b = question.pjm_answer_b
        sign_language_answer_c = question.pjm_answer_c
    else:
        sign_language_question = sign_language_answer_a = sign_language_answer_b = sign_language_answer_c = ""

    return {"questionContent": question_content, "answerA": answer_a, "answerB": answer_b, "answerC": answer_c,
            "signLanguageQuestion": sign_language_question, "signLanguageAnswerA": sign_language_answer_a,
            "signLanguageAnswerB": sign_language_answer_b, "signLanguageAnswerC": sign_language_answer_c,
            "language": config["language"]}


@login_required(login_url='/login')
def exam(request):
    if check_endless_exams(request.user):
        question = next_question(request.user)[0]
        question_details = Questions.objects.filter(id=question.id_question_id)[0]
        category = question.id_exam.category
        increment_questions = increment_question_number(question.question_number)
        media = check_media(question_details.media)
        timer = format_time(question.time_left)
        question_language = get_exam_language(request.user, question_details)
        template = loader.get_template('enpj/exam.html')
        return HttpResponse(template.render({'points': question_details.points,
                                             'category': category,
                                             'media': media,
                                             'question': question_language["questionContent"],
                                             'question_number': question.question_number,
                                             'primary_number': increment_questions[0],
                                             'spec_number': increment_questions[1],
                                             'answer_a': question_language["answerA"],
                                             'answer_b': question_language["answerB"],
                                             'answer_c': question_language["answerC"],
                                             'id_exam': question.id_exam_id,
                                             'id_question': question.id,
                                             'timer': timer,
                                             'timerSeconds': question.time_left - 1,
                                             "language": question_language["language"],
                                             "signLanguageQuestion": question_language["signLanguageQuestion"],
                                             "signLanguageAnswerA": question_language["signLanguageAnswerA"],
                                             "signLanguageAnswerB": question_language["signLanguageAnswerB"],
                                             "signLanguageAnswerC": question_language["signLanguageAnswerC"]}, request))
    else:
        return HttpResponseNotFound()


def exam_get(request):
    if not request.user.is_authenticated:
        return HttpResponse('401 Unauthorized', status=401)
    question = next_question(request.user)[0]
    question_details = Questions.objects.filter(id=question.id_question_id)[0]
    question_language = get_exam_language(request.user, question_details)
    increment_questions = increment_question_number(question.question_number)
    media = check_media(question_details.media)

    response_data = {
        'points': question_details.points,
        'media': media,
        'question': question_language["questionContent"],
        'question_number': question.question_number,
        'primary_number': increment_questions[0],
        'spec_number': increment_questions[1],
        'answer_a': question_language["answerA"],
        'answer_b': question_language["answerB"],
        'answer_c': question_language["answerC"],
        'id_question': question.id,
    }
    if question_language["signLanguageQuestion"]:
        response_data.update({"signLanguageQuestion": question_language["signLanguageQuestion"],
                              "signLanguageAnswerA": question_language["signLanguageAnswerA"],
                              "signLanguageAnswerB": question_language["signLanguageAnswerB"],
                              "signLanguageAnswerC": question_language["signLanguageAnswerC"]})
    print(response_data)
    return JsonResponse(response_data)


@login_required(login_url='/login')
def exam_result(request):
    if not check_endless_exams(request.user):
        try:
            exam = Exam.objects.filter(id_user=request.user).order_by("-id")[0]
        except IndexError:
            return HttpResponseNotFound()
        if int(exam.points) >= 68:
            result = "POZYTYWNY"
        else:
            result = "NEGATYWNY"
        template = loader.get_template('enpj/exam-result.html')
        return HttpResponse(template.render({'category': exam.category,
                                             'points': exam.points,
                                             "result": result,
                                             "exam": exam.id
                                             }, request))
    else:
        return HttpResponseNotFound()


def check_new_account(user):
    if Exam.objects.filter(id_user=user):
        return False
    else:
        return True


@login_required(login_url='login/')
def prepare_exam(request):
    if check_new_account(request.user):
        exams_status = 'new'
    else:
        exams_status = check_endless_exams(request.user)
    if exams_status:
        communicat = "Kontynuuj rozpoczęty egzamin"
    else:
        communicat = "Sprawdź ostatni egzamin"
    template = loader.get_template('enpj/prepare-exam.html')
    return HttpResponse(template.render({'continue': exams_status,
                                         'communicat': communicat}, request))


@login_required(login_url='/login')
def exam_check_answers(request):
    exam_number = request.GET.get('id', '')
    if not exam_number:
        return HttpResponseNotFound()
    try:
        exam = Exam.objects.filter(id=exam_number, id_user=request.user)[0]
    except IndexError:
        return HttpResponseBadRequest()
    question = ExamQuestions.objects.filter(id_exam=exam, question_number=1)[0]
    question_details = Questions.objects.filter(id=question.id_question_id)[0]

    template = loader.get_template('enpj/exam-check-answers.html')
    return HttpResponse(template.render({'points': question_details.points,
                                         'category': exam.category,
                                         'media': question_details.media,
                                         'question': question_details.question,
                                         'id_exam': exam_number,
                                         'answer': question.answer,
                                         'correct_answer': question_details.answer_correct,
                                         'correct_answer_list': check_correct_answers(exam_number)}, request))


def exam_check_answers_get(request):
    if not request.user.is_authenticated:
        return HttpResponse('401 Unauthorized', status=401)
    exam_number = request.GET.get('id', '')
    question_number = request.GET.get('question', '')
    question = ExamQuestions.objects.filter(id_exam=exam_number, question_number=question_number)[0]
    question_details = Questions.objects.filter(id=question.id_question_id)[0]

    response_data = {
        'points': question_details.points,
        'media': check_media(question_details.media),
        'question': question_details.question,
        'answer_a': question_details.answer_a,
        'answer_b': question_details.answer_b,
        'answer_c': question_details.answer_c,
        'answer': question.answer,
        'correct_answer': question_details.answer_correct
    }
    return JsonResponse(response_data)


@login_required(login_url='/login')
def statistics(request):
    exam_count = Exam.objects.filter(id_user=request.user, status='ZAKONCZONY').count()
    passed = Exam.objects.filter(id_user=request.user, status='ZAKONCZONY', points__gte=68).count()
    failed = Exam.objects.filter(id_user=request.user, status='ZAKONCZONY', points__lte=67).count()
    if passed == 0:
        passed = 'null'
    if failed == 0:
        failed = 'null'

    graph_data = get_graph_data(request.user, 'W')
    template = loader.get_template('enpj/statistics.html')
    return HttpResponse(template.render({'examCount': exam_count,
                                         'passed': passed,
                                         'failed': failed,
                                         'graphPoints': graph_data[0],
                                         'graphDate': graph_data[1]}, request))


def pie_chart(request):
    if not request.user.is_authenticated:
        return HttpResponse('401 Unauthorized', status=401)
    time_choose = request.GET.get('time', '')
    category_choose = request.GET.get('category', '')
    if time_choose == "Dzien":
        date_range = datetime.now(tz=timezone.utc) - timedelta(days=1)
    elif time_choose == "Tydzien":
        date_range = datetime.now(tz=timezone.utc) - timedelta(days=7)
    elif time_choose == "Miesiac":
        date_range = datetime.now(tz=timezone.utc) - timedelta(days=30)
    else:
        date_range = date(2022, 1, 1)
    if category_choose == 'W':
        exam_count = Exam.objects.filter(id_user=request.user, status='ZAKONCZONY', end_date__gte=date_range).count()
        passed = Exam.objects.filter(id_user=request.user, status='ZAKONCZONY', points__gte=68,
                                     end_date__gte=date_range).count()
        failed = Exam.objects.filter(id_user=request.user, status='ZAKONCZONY', points__lte=67,
                                     end_date__gte=date_range).count()
    else:
        exam_count = Exam.objects.filter(id_user=request.user, status='ZAKONCZONY', end_date__gte=date_range,
                                         category=category_choose).count()
        passed = Exam.objects.filter(id_user=request.user, status='ZAKONCZONY', points__gte=68,
                                     end_date__gte=date_range, category=category_choose).count()
        failed = Exam.objects.filter(id_user=request.user, status='ZAKONCZONY', points__lte=67,
                                     end_date__gte=date_range, category=category_choose).count()
    if passed == 0:
        passed = None
    if failed == 0:
        failed = None

    response_data = {'examCount': exam_count,
                     'passed': passed,
                     'failed': failed}
    return JsonResponse(response_data)


def graph_chart(request):
    if not request.user.is_authenticated:
        return HttpResponse('401 Unauthorized', status=401)
    category_choose = request.GET.get('category', '')

    graph_data = get_graph_data(request.user, category_choose)
    response_data = {'graphPoints': graph_data[0], 'graphDate': graph_data[1]}
    return JsonResponse(response_data)


@login_required(login_url='/login')
def prepare_learning(request):
    template = loader.get_template('enpj/prepare-learning.html')
    return HttpResponse(template.render({}, request))


def questions_list(category, module_number):
    question_type = "podst"
    if category == "PT":
        if module_number < 12:
            module = "P" + str(module_number)
        else:
            module = "PD" + str(module_number - 11)
            question_type = "spec"
    else:
        if module_number < 21:
            module = "W" + str(module_number)
        else:
            module = category[0] + str(module_number - 20)
            question_type = "spec"
    category_contain = category + ','
    question_list = []
    module_questions = Questions.objects.filter(module=module).filter(Q(categories__endswith=category) |
                                                                      Q(categories__contains=category_contain))
    if question_type == "spec":
        for question in module_questions:
            question_list.append({"question": question.question, "answerA": question.answer_a,
                                  "answerB": question.answer_b, "answerC": question.answer_c,
                                  "correctAnswer": question.answer_correct, "media": question.media,
                                  "source": question.source})
    else:
        for question in module_questions:
            question_list.append({"question": question.question, "correctAnswer": question.answer_correct,
                                 "media": question.media, "source": question.source})
    return question_list, question_type


@login_required(login_url='/login')
def learning(request):
    category = request.GET.get('category', '')
    module = int(request.GET.get('module', '0'))

    if not (module > 0) and ((category in ("A", "A1", "A2", "AM", "B", "B1", "C", "C1", "D", "D1", "T") and module < 27)
                             or (category == "PT" and module < 20)):
        return HttpResponseNotFound()
    questions_list_type = questions_list(category, module)
    template = loader.get_template('enpj/learning.html')
    return HttpResponse(template.render({'questionsArray': questions_list_type[0],
                                         'type': questions_list_type[1],
                                         'category': category,
                                         'module': module}, request))


def check_options(user):
    options = Options.objects.filter(user=user)
    if not options:
        return {"language": "PL", "signLanguage": False, "exist": False}
    else:
        return {"language": options[0].language, "signLanguage": options[0].sign_language, "exist": True}


@login_required(login_url='/login')
def options(request):
    config = check_options(request.user)
    template = loader.get_template('enpj/options.html')
    return HttpResponse(template.render({"language": config["language"],
                                         "signLanguage": str(config["signLanguage"]).lower()}, request))


def update_options(request):
    if not request.user.is_authenticated:
        return HttpResponse('401 Unauthorized', status=401)
    language = request.POST.get('language', "PL")
    sign_language = request.POST.get('signLanguage', False)
    if sign_language == "false":
        sign_language = False
    elif sign_language == "true":
        sign_language = True

    config = check_options(request.user)
    if not config["exist"]:
        Options.objects.create(user=request.user, language=language, sign_language=sign_language)
    else:
        options = Options.objects.filter(user=request.user)[0]
        options.language = language
        options.sign_language = sign_language
        options.save()
    return HttpResponse()
