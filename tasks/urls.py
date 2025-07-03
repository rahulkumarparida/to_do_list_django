from django.urls import path
from tasks import views
urlpatterns = [
    path('', views.index , name='index' ),
    path('register/' , views.register , name='register'),
    path('login/' , views.login , name='login'),
    path('logout/' , views.logout , name='logout'),
    path('delete_task/<int:task_id>', views.delete_task, name='delete_task'),
    path('complete_task/<int:task_id>', views.complete_task, name='complete_task'),
    path('update_task/<int:task_id>', views.update_task , name='update_task'),
]