from django.test import TestCase
from ..views import draw_questions, exam_next_question, generate_questions, check_active_exams, cancel_exam, \
    generate_exam, next_question, increment_question_number, check_media, check_endless_exams, count_points,\
    check_correct_answers, end_exam, format_time, get_graph_data, get_exam_language, exam as function_exam, exam_get, \
    exam_result, check_new_account, prepare_exam, exam_check_answers, exam_check_answers_get, statistics, pie_chart, \
    graph_chart, prepare_learning, questions_list, learning, check_options, options as function_options, update_options
from . import data_generator
from datetime import datetime, timedelta
from django.utils import timezone
from ..models import Questions, ExamQuestions, Exam, Options


class TestDrawQuestions(TestCase):
    def check_list(self, data: tuple, checklist: list):
        for i in data:
            self.assertTrue(i in checklist)

    def test_1(self):
        data_generator.generate_questions("A", "A1")

        question_list_a = draw_questions("A", False)
        self.check_list((1, 3, 5, 6, 8, 24, 26, 28, 29, 31), question_list_a)
        self.assertEqual(len(question_list_a), 32)

        question_list_a1 = draw_questions("A1", False)
        self.check_list((2, 4, 5, 7, 8, 25, 27, 28, 30, 31), question_list_a1)
        self.assertEqual(len(question_list_a1), 32)

    def test_2(self): #błąd
        data_generator.generate_questions("T", "PT")

        question_list_t = draw_questions("T", False)
        self.check_list((1, 3, 5, 6, 8, 24, 26, 28, 29, 31), question_list_t)
        self.assertEqual(len(question_list_t), 32)

        question_list_pt = draw_questions("PT", False)
        self.check_list((2, 4, 5, 7, 8, 25, 27, 28, 30, 31), question_list_pt)
        self.assertEqual(len(question_list_pt), 32)

    def test_3(self):
        data_generator.generate_pjm_questions()

        question_list_pjm = draw_questions("B", True)
        question_list_pjm.sort()
        self.assertListEqual([i for i in range(1, 33)], question_list_pjm)
        self.assertEqual(len(question_list_pjm), 32)

    def test_4(self):
        data_generator.generate_questions("A", "A1")

        question_list_a = draw_questions("A", True)
        self.check_list((1, 3, 5, 6, 8, 24, 26, 28, 29, 31), question_list_a)
        self.assertEqual(len(question_list_a), 32)

    def test_5(self):
        data_generator.generate_questions("B", "B1")

        question_list = draw_questions("B", False)
        primary_question_max = max(question_list[:20])
        spec_question_min = min(question_list[20:])
        self.assertTrue(primary_question_max < spec_question_min)


class TestExamNextQuestion(TestCase):
    def test_6(self):
        request = data_generator.generate_next_questions()[0]

        request.POST = {'answer': "A", 'questionId': 1, 'time': 4}
        self.assertEqual(exam_next_question(request).status_code, 200)
        exam_question = ExamQuestions.objects.filter(id=1)[0]
        self.assertEqual(exam_question.answer, "A")
        next_exam_question = ExamQuestions.objects.filter(id=2)[0]
        self.assertEqual(next_exam_question.time_left, 4)

    def test_7(self):
        request = data_generator.generate_unauthenticated_request()

        self.assertEqual(exam_next_question(request).status_code, 401)

    def test_8(self):
        request = data_generator.generate_next_questions("A", False)[0]

        request.POST = {'questionId': 1}
        self.assertEqual(exam_next_question(request).status_code, 404)

    def test_9(self):
        request = data_generator.generate_next_questions(next_question=False)[0]

        request.POST = {'answer': "A", 'examId': 1, 'questionId': 1, 'end': True}
        self.assertEqual(exam_next_question(request).status_code, 200)
        exam_question = ExamQuestions.objects.filter(id=1)[0]
        self.assertEqual(exam_question.answer, "A")
        exam = Exam.objects.filter(id=1)[0]
        self.assertEqual(exam.status, "ZAKONCZONY")


class TestGenerateQuestions(TestCase):
    def test_10(self):
        exam = data_generator.generate_exam_and_questions()

        generate_questions(exam, False)
        exam_questions = ExamQuestions.objects.filter(id_exam=1)
        self.assertEqual(len(exam_questions), 32)
        self.assertEqual(exam_questions[0].time_left, 1500)
        for i in range(0, 32):
            self.assertEqual(exam_questions[i].id_exam, exam)
            self.assertEqual(exam_questions[i].question_number, i + 1)
            self.assertTrue(exam_questions[i].id_question_id is not None)


class TestCheckActiveExams(TestCase):
    def test_11(self):
        request = data_generator.generate_exam_and_request()[0]

        self.assertEqual(check_active_exams(request).content, b'{"info": 1}')

    def test_12(self):
        request = data_generator.generate_request()

        self.assertEqual(check_active_exams(request).content, b'{"info": false}')


class TestCancelExam(TestCase):
    def test_13(self):
        request = data_generator.generate_exam_and_request()[0]

        request.POST = {'cancel': True}
        self.assertEqual(cancel_exam(request).status_code, 200)
        exam = Exam.objects.filter(id=1)[0]
        self.assertEqual(exam.status, "ANULOWANY")
        self.assertEqual(str(exam.end_date), str(datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M") + ":00+00:00"))

    def test_14(self):
        request = data_generator.generate_request()

        self.assertEqual(cancel_exam(request).status_code, 404)


class TestGenerateExam(TestCase):
    def test_15(self):
        request = data_generator.generate_request()
        data_generator.generate_questions("A", "A")

        request.POST = {'category': 'A'}
        self.assertEqual(generate_exam(request).status_code, 200)
        exam = Exam.objects.filter()[0]
        exam_questions = ExamQuestions.objects.filter(id_exam=exam.id)
        self.assertEqual(exam.category, "A")
        self.assertEqual(exam.id_user, request.user)
        self.assertFalse(exam.points)
        self.assertEqual(len(exam_questions), 32)


class TestNextQuestion(TestCase):
    def test_16(self):
        request = data_generator.generate_next_questions(next_question=False)[0]

        question = next_question(request.user)[0]
        self.assertFalse(question.answer)
        self.assertEqual(question.id_exam.id, 1)


class TestIncrementQuestionNumber(TestCase):
    def test_17(self):
        self.assertEqual(increment_question_number(20), [20, 0])

    def test_18(self):
        self.assertEqual(increment_question_number(21), [20, 1])


class TestCheckMedia(TestCase):
    def test_19(self):
        self.assertEqual(check_media(""), "brak_zdjecia_1024x576.jpg")

    def test_20(self):
        self.assertEqual(check_media("test.jpg"), "test.jpg")


class TestCheckEndlessExams(TestCase):
    def test_21(self):
        request = data_generator.generate_exam_and_request()[0]

        self.assertTrue(check_endless_exams(request.user))

    def test_22(self):
        request = data_generator.generate_request()

        self.assertFalse(check_endless_exams(request.user))


class TestCountPoints(TestCase):
    def test_23(self):
        exam = data_generator.generate_next_questions("A")[1]

        self.assertEqual(count_points(exam), 1)


class TestCheckCorrectAnswers(TestCase):
    def test_24(self):
        exam = data_generator.generate_next_questions("A")[1]

        self.assertEqual(check_correct_answers(exam), [1])


class TestEndExam(TestCase):
    def test_25(self):
        data_generator.generate_exam_and_request()[1]

        end_exam(1)
        exam = Exam.objects.filter(id=1)[0]
        self.assertEqual(exam.status, "ZAKONCZONY")
        self.assertTrue(str(datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M")) in str(exam.end_date))
        self.assertEqual(exam.points, 0)


class TestFormatTime(TestCase):
    def test_26(self):
        self.assertEqual(format_time(50), "00:50")
        self.assertEqual(format_time(60), "01:00")
        self.assertEqual(format_time(750), "12:30")


class TestGetGraphData(TestCase):
    def setUp(self):
        self.request = data_generator.generate_finished_exams(21)

    def test_27(self):
        points, end_time = get_graph_data(self.request.user, "W")
        self.assertListEqual(points, [72, 60, 72, 60, 72, 60, 72, 60, 72, 60, 72, 60, 72, 60, 72, 60, 72, 60, 72, 60])
        self.assertListEqual(end_time, ["2022-10-" + str(i).zfill(2) + " 00:00:00" for i in range(21, 1, -1)])

    def test_28(self):
        points, end_time = get_graph_data(self.request.user, "A")
        self.assertListEqual(points, [72, 60, 72, 60, 72, 60, 72, 60, 72, 60, 72, 60, 72, 60, 72, 60, 72, 60, 72, 60])
        self.assertListEqual(end_time, ["2022-10-" + str(i).zfill(2) + " 00:00:00" for i in range(21, 1, -1)])


class TestGetExamLanguage(TestCase):
    def setUp(self):
        self.question = Questions.objects.create(question="PL", answer_a="PL", answer_b="PL", answer_c="PL",
                                            question_eng="ENG", answer_a_eng="ENG", answer_b_eng="ENG",
                                            answer_c_eng="ENG", question_de="DE", answer_a_de="DE", answer_b_de="DE",
                                            answer_c_de="DE", pjm_question="PJM", pjm_answer_a="PJM",
                                            pjm_answer_b="PJM", pjm_answer_c="PJM", points=1)

    def test_29(self):
        request = data_generator.generate_options("ENG")

        self.assertEqual(get_exam_language(request.user, self.question), {"questionContent": "ENG", "answerA": "ENG",
            "answerB": "ENG", "answerC": "ENG", "signLanguageQuestion": "", "signLanguageAnswerA": "",
            "signLanguageAnswerB": "", "signLanguageAnswerC": "", "language": "ENG"})

    def test_30(self):
        request = data_generator.generate_options("DE")

        self.assertEqual(get_exam_language(request.user, self.question), {"questionContent": "DE", "answerA": "DE",
            "answerB": "DE", "answerC": "DE", "signLanguageQuestion": "", "signLanguageAnswerA": "",
            "signLanguageAnswerB": "", "signLanguageAnswerC": "", "language": "DE"})

    def test_31(self):
        request = data_generator.generate_options("PL", True)

        self.assertEqual(get_exam_language(request.user, self.question), {"questionContent": "PL", "answerA": "PL",
            "answerB": "PL", "answerC": "PL", "signLanguageQuestion": "PJM", "signLanguageAnswerA": "PJM",
            "signLanguageAnswerB": "PJM", "signLanguageAnswerC": "PJM", "language": "PL"})


class TestExam(TestCase):
    def test_32(self):
        request, exam = data_generator.generate_exam_and_request(category="PT")
        question = Questions.objects.create(id=1, points=2, media="media.jpg", question="question",
                                            type="SPECJALISTYCZNY", categories="PT",
                                            answer_a="answer_a", answer_b="answer_b", answer_c="answer_c")
        ExamQuestions.objects.create(id=999, id_exam=exam, id_question=question, question_number=1,
                                     time_left=888)

        response = function_exam(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="points">2')
        self.assertContains(response, 'class="topTdSpanBox">PT')
        self.assertContains(response, 'var importMedia = "media.jpg"')
        self.assertContains(response, 'id="question">question')
        self.assertContains(response, """onClick="takeAnswer('A')">answer_a""")
        self.assertContains(response, """onClick="takeAnswer('B')">answer_b""")
        self.assertContains(response, """onClick="takeAnswer('C')">answer_c""")
        self.assertContains(response, "var importIdExam = 1")
        self.assertContains(response, "var importQuestionNumber = 1")
        self.assertContains(response, "var importQuestionId = 999")
        self.assertContains(response, 'id="time">14:48')
        self.assertContains(response, "var importTimerSeconds = 887")
        self.assertContains(response, 'var importLanguage = "PL"')
        self.assertContains(response, 'var importSignLanguageQuestion = ""')
        self.assertContains(response, 'var importSignLanguageAnswerA = ""')
        self.assertContains(response, 'var importSignLanguageAnswerB = ""')
        self.assertContains(response, 'var importSignLanguageAnswerC = ""')

    def test_33(self):
        request = data_generator.generate_request()

        self.assertEqual(function_exam(request).status_code, 404)


class TestExamGet(TestCase):
    def test_34(self):
        request, exam = data_generator.generate_exam_and_request()
        question = Questions.objects.create(id=1, points=1, media="media.jpg", question="question", type="SPECJALISTYCZNY",
                                            answer_a="A", answer_b="B", answer_c="C")
        ExamQuestions.objects.create(id=1, id_exam=exam, id_question=question, question_number=32, time_left=10)

        exam = exam_get(request)
        self.assertEqual(exam.status_code, 200)
        self.assertEqual(exam.content, b'{"points": 1, "media": "media.jpg", "question": "question", '
                                       b'"question_number": 32, "primary_number": 20, "spec_number": 12,'
                                       b' "answer_a": "A", "answer_b": "B", "answer_c": "C", "id_question": 1}')

    def test_35(self):
        request, exam = data_generator.generate_exam_and_request()
        question = Questions.objects.create(id=1, points=1, media="media.jpg", question="question", type="SPECJALISTYCZNY",
                                            answer_a="A", answer_b="B", answer_c="C", pjm_question="PJM", pjm_answer_a="PJM",
                                            pjm_answer_b="PJM", pjm_answer_c="PJM")
        ExamQuestions.objects.create(id=1, id_exam=exam, id_question=question, question_number=32, time_left=10)
        Options.objects.create(user=request.user, sign_language=True)

        exam = exam_get(request)
        self.assertEqual(exam.status_code, 200)
        self.assertEqual(exam.content, b'{"points": 1, "media": "media.jpg", "question": "question", '
                                       b'"question_number": 32, "primary_number": 20, "spec_number": 12, "answer_a": '
                                       b'"A", "answer_b": "B", "answer_c": "C", "id_question": 1,'
                                       b' "signLanguageQuestion": "PJM", "signLanguageAnswerA": "PJM", '
                                       b'"signLanguageAnswerB": "PJM", "signLanguageAnswerC": "PJM"}')

    def test_36(self):
        request = data_generator.generate_unauthenticated_request()

        self.assertEqual(exam_get(request).status_code, 401)


class TestExamResult(TestCase):
    def test_37(self):
        request = data_generator.generate_exam_and_request("ZAKONCZONY", 67, "PT")[0]

        response = exam_result(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kategoria PT")
        self.assertContains(response, "zdobywając 67")
        self.assertContains(response, "Uzyskałeś wynik NEGATYWNY")
        self.assertContains(response, "id=1")

    def test_38(self):
        request = data_generator.generate_exam_and_request("ZAKONCZONY", 68, "PT")[0]

        response = exam_result(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kategoria PT")
        self.assertContains(response, "zdobywając 68")
        self.assertContains(response, "Uzyskałeś wynik POZYTYWNY")
        self.assertContains(response, "id=1")

    def test_39(self):
        request = data_generator.generate_exam_and_request()[0]

        self.assertEqual(exam_result(request).status_code, 404)

    def test_40(self):
        request = data_generator.generate_request()

        self.assertEqual(exam_result(request).status_code, 404)


class TestCheckNewAccount(TestCase):
    def test_41(self):
        request = data_generator.generate_request()

        self.assertTrue(check_new_account(request.user))

    def test_42(self):
        request = data_generator.generate_exam_and_request()[0]

        self.assertFalse(check_new_account(request.user))


class TestPrepareExam(TestCase):
    def test_43(self):
        request = data_generator.generate_request()

        response = prepare_exam(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'var importContinueExam = "new"')
        self.assertContains(response, 'onClick="ifContinue()">Kontynuuj rozpoczęty egzamin')

    def test_44(self):
        request = data_generator.generate_exam_and_request()[0]

        response = prepare_exam(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'var importContinueExam = "1"')
        self.assertContains(response, 'onClick="ifContinue()">Kontynuuj rozpoczęty egzamin')

    def test_45(self):
        request = data_generator.generate_exam_and_request("ZAKONCZONY")[0]

        response = prepare_exam(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'var importContinueExam = "False"')
        self.assertContains(response, 'onClick="ifContinue()">Sprawdź ostatni egzamin')


class TestExamCheckAnswers(TestCase):
    def test_46(self):#blad
        request, exam = data_generator.generate_exam_and_request(category="PT")
        question = Questions.objects.create(id=1, points=2, media="media.jpg", question="question",
                                            type="SPECJALISTYCZNY", categories="PT", answer_correct="B")
        ExamQuestions.objects.create(id_exam=exam, id_question=question, question_number=1,
                                     time_left=888, answer="A")

        request.GET = {"id": 1}
        response = exam_check_answers(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="points">2')
        self.assertContains(response, 'class="topTdSpanBox">PT')
        self.assertContains(response, 'var importMedia = "media.jpg"')
        self.assertContains(response, 'id="question">question')
        self.assertContains(response, "var importIdExam = 1")
        self.assertContains(response, 'var importAnswer = "A"')
        self.assertContains(response, 'var importCorrectAnswer = "B"')
        self.assertContains(response, "var importCorrectAnswerList = []")

    def test_47(self):
        request = data_generator.generate_request()

        self.assertEqual(exam_check_answers(request).status_code, 404)

    def test_48(self):
        request = data_generator.generate_request()

        request.GET = {"id": 1}
        self.assertEqual(exam_check_answers(request).status_code, 400)


class TestExamCheckAnswersGet(TestCase):
    def test_49(self):
        request, exam = data_generator.generate_exam_and_request()
        question = Questions.objects.create(id=1, points=2, media="media.jpg", question="question", answer_correct="B",
                                            answer_a="answer_a", answer_b="answer_b", answer_c="answer_c")
        ExamQuestions.objects.create(id_exam=exam, id_question=question, question_number=1, answer="A")

        request.GET = {"id": 1, 'question': 1}
        response = exam_check_answers_get(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"points": 2, "media": "media.jpg", "question": "question",'
                                           b' "answer_a": "answer_a", "answer_b": "answer_b", "answer_c": "answer_c",'
                                           b' "answer": "A", "correct_answer": "B"}')

    def test_50(self):
        request = data_generator.generate_unauthenticated_request()

        self.assertEqual(exam_check_answers_get(request).status_code, 401)


class TestStatistics(TestCase):
    def test_51(self):
        request = data_generator.generate_finished_exams(2)

        response = statistics(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'importPassed = 1')
        self.assertContains(response, 'importFailed = 1')
        self.assertContains(response, 'importExamCount = "2"')
        self.assertContains(response, "importGraphDates = ['2022-10-02 00:00:00', '2022-10-01 00:00:00']")
        self.assertContains(response, 'importGraphPoints = [60, 72]')

    def test_52(self):
        request = data_generator.generate_request()

        response = statistics(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'importPassed = null')
        self.assertContains(response, 'importFailed = null')
        self.assertContains(response, 'importExamCount = "0"')
        self.assertContains(response, "importGraphDates = []")
        self.assertContains(response, 'importGraphPoints = []')


class TestPieChart(TestCase):
    def test_53(self):
        request = data_generator.generate_request()
        Exam.objects.create(id_user=request.user, status="ZAKONCZONY", points=72,
                            category="A", end_date="2022-10-10")
        Exam.objects.create(id_user=request.user, status="ZAKONCZONY", points=72,
                            category="B", end_date="2022-10-10")

        request.GET = {'category': "A"}
        response = pie_chart(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"examCount": 1, "passed": 1, "failed": null}')

    def test_54(self):
        request = data_generator.generate_request()
        Exam.objects.create(id_user=request.user, status="ZAKONCZONY", points=72,
                            category="A", end_date="2022-10-10")
        Exam.objects.create(id_user=request.user, status="ZAKONCZONY", points=72,
                            category="B", end_date="2022-10-10")

        request.GET = {'category': "W"}
        response = pie_chart(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"examCount": 2, "passed": 2, "failed": null}')

    def test_55(self):
        request = data_generator.generate_request()

        request.GET = {'category': "W"}
        response = pie_chart(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"examCount": 0, "passed": null, "failed": null}')

    def test_56(self):
        request = data_generator.generate_request()
        Exam.objects.create(id_user=request.user, status="ZAKONCZONY", points=72,
                            category="A", end_date=datetime.now(tz=timezone.utc))
        Exam.objects.create(id_user=request.user, status="ZAKONCZONY", points=72,
                            category="A", end_date=datetime.now(tz=timezone.utc) - timedelta(days=2))

        request.GET = {'time': "Dzien", 'category': "W"}
        response = pie_chart(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"examCount": 1, "passed": 1, "failed": null}')

    def test_57(self):
        request = data_generator.generate_request()
        Exam.objects.create(id_user=request.user, status="ZAKONCZONY", points=72,
                            category="A", end_date=datetime.now(tz=timezone.utc) - timedelta(days=6))
        Exam.objects.create(id_user=request.user, status="ZAKONCZONY", points=72,
                            category="A", end_date=datetime.now(tz=timezone.utc) - timedelta(days=8))

        request.GET = {'time': "Tydzien", 'category': "W"}
        response = pie_chart(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"examCount": 1, "passed": 1, "failed": null}')

    def test_58(self):
        request = data_generator.generate_request()
        Exam.objects.create(id_user=request.user, status="ZAKONCZONY", points=72,
                            category="A", end_date=datetime.now(tz=timezone.utc) - timedelta(days=29))
        Exam.objects.create(id_user=request.user, status="ZAKONCZONY", points=72,
                            category="A", end_date=datetime.now(tz=timezone.utc) - timedelta(days=31))

        request.GET = {'time': "Miesiac", 'category': "W"}
        response = pie_chart(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"examCount": 1, "passed": 1, "failed": null}')

    def test_59(self):
        request = data_generator.generate_unauthenticated_request()

        self.assertEqual(pie_chart(request).status_code, 401)


class TestGraphChart(TestCase):
    def test_60(self):
        request = data_generator.generate_finished_exams(1)

        request.GET = {'category': "A"}
        response = graph_chart(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"graphPoints": [72], "graphDate": ["2022-10-01 00:00:00"]}')

    def test_61(self):
        request = data_generator.generate_unauthenticated_request()

        self.assertEqual(graph_chart(request).status_code, 401)


class TestPrepareLearning(TestCase):
    def test_62(self):
        request = data_generator.generate_request()

        self.assertEqual(prepare_learning(request).status_code, 200)


class TestQuestionsList(TestCase):
    def setUp(self):
        Questions.objects.create(points=2, module="P11", media="media1.jpg", question="question1",
                                 answer_correct="1", source="source1", categories="PT")
        Questions.objects.create(points=2, module="PD1", media="media2.jpg", question="question2",
                                 answer_correct="2", answer_a="answer_a2", answer_b="answer_b2",
                                 answer_c="answer_c2", source="source2", categories="PT")
        Questions.objects.create(points=2, module="W20", media="media3.jpg", question="question3",
                                 answer_correct="3", source="source3", categories="B")
        Questions.objects.create(points=2, module="B1", media="media4.jpg", question="question4",
                                 answer_correct="4", answer_a="answer_a4", answer_b="answer_b4",
                                 answer_c="answer_c4", source="source4", categories="B")

    def test_63(self):
        response = questions_list("PT", 11)
        self.assertListEqual(response[0], [{"question": "question1", "correctAnswer": "1", "media": "media1.jpg",
                                            "source": "source1"}])
        self.assertEqual(response[1], "podst")

    def test_64(self):
        response = questions_list("PT", 12)
        self.assertListEqual(response[0], [{"question": "question2", "answerA": "answer_a2", "answerB": "answer_b2",
                                            "answerC": "answer_c2", "correctAnswer": "2", "media": "media2.jpg",
                                            "source": "source2"}])
        self.assertEqual(response[1], "spec")

    def test_65(self):
        response = questions_list("B", 20)
        self.assertListEqual(response[0], [{"question": "question3", "correctAnswer": "3", "media": "media3.jpg",
                                            "source": "source3"}])
        self.assertEqual(response[1], "podst")

    def test_66(self):
        response = questions_list("B", 21)
        self.assertListEqual(response[0], [{"question": "question4", "answerA": "answer_a4", "answerB": "answer_b4",
                                            "answerC": "answer_c4", "correctAnswer": "4", "media": "media4.jpg",
                                            "source": "source4"}])
        self.assertEqual(response[1], "spec")


class TestLearning(TestCase):
    def test_67(self):
        request = data_generator.generate_request()
        Questions.objects.create(points=2, module="P11", media="media1.jpg", question="question1",
                                 answer_correct="1", source="source1", categories="PT")

        request.GET = {'category': "PT", 'module': 11}
        response = learning(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "const importQuestionsArray = [{\'question\': \'question1\',"
                                      " \'correctAnswer\': \'1\', \'media\': \'media1.jpg\', \'source\': \'source1\'}]")
        self.assertContains(response, 'var importType = "podst"')
        self.assertContains(response, 'var importType = "podst"')
        self.assertContains(response, 'var importCategory = "PT"')
        self.assertContains(response, 'var importModule = "11"')

    def test_68(self):
        request = data_generator.generate_request()

        request.GET = {'category': "A", 'module': -1}
        self.assertEqual(learning(request).status_code, 404)


class TestCheckOptions(TestCase):
    def test_69(self):
        request = data_generator.generate_request()

        self.assertEqual(check_options(request.user), {"language": "PL", "signLanguage": False, "exist": False})

    def test_70(self):
        request = data_generator.generate_options("ENG", True)

        self.assertEqual(check_options(request.user), {"language": "ENG", "signLanguage": True, "exist": True})


class TestOptions(TestCase):
    def test_71(self):
        request = data_generator.generate_options("ENG", True)

        response = function_options(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'var importActualLanguage = "ENG"')
        self.assertContains(response, 'var importActualSignLanguage = true')


class TestUpdateOptions(TestCase):
    def test_72(self):
        request = data_generator.generate_options("ENG", True)

        request.POST = {'language': "PL", 'signLanguage': 'false'}
        self.assertEqual(update_options(request).status_code, 200)
        options = Options.objects.filter(user=request.user)[0]
        self.assertEqual(options.language, "PL")
        self.assertEqual(options.sign_language, False)

    def test_73(self):
        request = data_generator.generate_request()

        request.POST = {'language': "ENG", 'signLanguage': 'true'}
        self.assertEqual(update_options(request).status_code, 200)
        options = Options.objects.filter(user=request.user)[0]
        self.assertEqual(options.language, "ENG")
        self.assertEqual(options.sign_language, True)

    def test_74(self):
        request = data_generator.generate_unauthenticated_request()

        self.assertEqual(update_options(request).status_code, 401)
