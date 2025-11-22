from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('<int:pk>/profile/', views.Profile.as_view(), name='profile'),
    path('<int:pk>/update_user/', views.UpdateUser.as_view(), name='update_user'),
    path('<int:pk>/delete_user/', views.DeleteUser.as_view(), name='delete_user'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('question/create/', views.QuestionCreateView.as_view(), name='question_form'),

]