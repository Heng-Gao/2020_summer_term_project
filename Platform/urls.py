from django.urls import path
from Platform import views

urlpatterns = [
    path('', views.index),
    path('index/', views.index),
    path('login/', views.login),
    # path('register/', views.register),
    path('index_user/', views.index_user),
    path('index_restaurant/', views.index_restaurant),
    path('index_administrator/', views.index_administrator),
    path('history/', views.history),
    path('reserve/', views.reserve),
    path('current/', views.current),
    path('handle_current/', views.handle_current),
    path('logout/', views.logout),
    path('scores_edit/', views.scores_edit),
    path('scores_submit/', views.scores_submit),
    path('restaurant_history/', views.restaurant_history),
    path('user_edit/', views.user_edit),
    path('user_submit/', views.user_submit),
    path('course_edit/', views.course_edit),
    path('course_submit/', views.course_submit),
    path('term_edit/', views.term_edit),
]
