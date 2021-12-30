from django.urls import path, include
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('moderation/', views.moderation, name='moderation'),
    path('add_question/', views.add_question, name='add_question'),
    #path('reclaimaccount/', views.reclaimaccount, name='reclaimaccount'),
]
