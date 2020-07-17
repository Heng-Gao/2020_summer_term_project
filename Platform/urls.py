from django.urls import path
from Platform import views

urlpatterns = [
    path('', views.index),
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('index_user/', views.index_user),
    path('index_restaurant/', views.index_restaurant),
    path('index_administrator/', views.index_administrator),
    path('student_scores/', views.student_scores),
    path('student_timetable/', views.student_timetable),
    path('course_selection/', views.course_selection),
    path('course_delete/', views.course_delete),
    path('logout/', views.logout),
    path('teacher_coursetable/', views.teacher_coursetable),
    path('scores_edit/', views.scores_edit),
    path('scores_submit/', views.scores_submit),
    path('user_edit/', views.user_edit),
    path('user_submit/', views.user_submit),
    path('course_edit/', views.course_edit),
    path('course_submit/', views.course_submit),
    path('term_edit/', views.term_edit),
]
