from django.urls import path
from Platform import views

urlpatterns = [
    path('', views.index),
    path('index/', views.index),
    path('login/', views.login),
    path('user_register/', views.user_register, name='user_register'),
    path('restaurant_register/', views.restaurant_register, name='restaurant_register'),
    path('index_user/', views.index_user),
    path('index_restaurant/', views.index_restaurant),
    path('index_administrator/', views.index_administrator),
    path('history/', views.history),
    path('recommand/', views.recommand),
    path('reserve/', views.reserve),
    path('current/', views.current),
    path('handle_current/', views.handle_current),
    path('logout/', views.logout),
    path('new_activities/', views.new_activities),
    path('edit_menu/', views.edit_menu),
    path('menu_submit/', views.menu_submit),
    path('restaurant_history/', views.restaurant_history),
    path('audit_restaurant/', views.audit_restaurant),
    path('delete_restaurant/', views.delete_restaurant),
    path('algorithm/',views.aitest)
]
