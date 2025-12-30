from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, LogoutView, RegisterPage
from . import views


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('',TaskList.as_view(), name='tasks'),
     path('task/<int:pk>/',TaskDetail.as_view(), name='task'),
     path('task-create/', TaskCreate.as_view(), name='task-create'),
     path('task-delete/<int:pk>/',DeleteView.as_view(), name='task-delete'),
     path('task-update/<int:pk>/', views.update_task, name='task-update'),


    path('', views.TaskList.as_view(), name='task_list'),
   ]  