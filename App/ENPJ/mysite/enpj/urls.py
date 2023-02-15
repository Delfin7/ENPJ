from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('', views.prepare_exam),
    path('exam', views.exam),
    path('exam-get', views.exam_get),
    path('exam-next-question', views.exam_next_question),
    path('exam-result', views.exam_result),
    path('generate-exam', views.generate_exam),
    path('cancel-exam', views.cancel_exam,),
    path('check-active-exams', views.check_active_exams),
    path('exam-check-answers', views.exam_check_answers),
    path('exam-check-answers-get', views.exam_check_answers_get),
    path('statistics', views.statistics),
    path('pie-chart', views.pie_chart),
    path('graph-chart', views.graph_chart),
    path('prepare-learning', views.prepare_learning),
    path('learning', views.learning),
    path('options', views.options),
    path('update-options', views.update_options),
    re_path('', include('allauth.urls')),
]