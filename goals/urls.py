from django.urls import path
from .views import daily_goals, tasks

app_name = 'goals'

urlpatterns = [

    ####################### urls for 'daily-goals' curd operations #######################
    path('daily/', daily_goals.daily_goals_index, name='daily_goals_list'),
    path('daily/add/', daily_goals.create_daily_goal, name='create_daily_goal'),
    path('daily/<int:pk>/', daily_goals.daily_goal_details, name='daily_goal_details'),
    path('daily/<int:pk>/edit/', daily_goals.edit_daily_goal, name='edit_daily_goal'),
    path('daily/<int:pk>/delete/', daily_goals.delete_daily_goal, name='delete_daily_goal'),

    ####################### urls to download 'daily-goals' using weasyprint #######################
    path('daily/<int:pk>/download/', daily_goals.download_daily_goal, name='download_daily_goal'),
    path('daily/download/', daily_goals.download_daily_goals, name='download_daily_goals'),

    ####################### urls for 'tasks' curd operations using JQuery #######################
    path('daily/<int:daily_pk>/tasks/create/', tasks.create_task, name='create_task'),
    path('daily/<int:daily_pk>/tasks/<int:pk>/update/', tasks.update_task, name='update_task'),
    path('daily/<int:daily_pk>/tasks/<int:pk>/delete/', tasks.delete_task, name='delete_task'),
    path('daily/<int:daily_pk>/tasks/<int:pk>/change-status/', tasks.change_task_status, name='change_task_status'),

]

