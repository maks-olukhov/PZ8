from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'departments/',
        views.department_list,
        name='department_list'
    ),

    path(
        'departments/add/',
        views.department_create,
        name='department_create'
    ),

    path(
        'departments/<int:pk>/edit/',
        views.department_update,
        name='department_update'
    ),

    path(
        'departments/<int:pk>/delete/',
        views.department_delete,
        name='department_delete'
    ),
    path('groups/', views.academic_group_list, name='academic_group_list'),
    path('groups/add/', views.academic_group_create, name='academic_group_create'),
    path('groups/<int:id>/edit/', views.academic_group_update, name='academic_group_update'),
    path('groups/<int:id>/delete/', views.academic_group_delete, name='academic_group_delete'),
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/add/', views.courses_create, name='courses_create'),
    path('courses/<int:id>/edit/', views.courses_update, name='courses_update'),
    path('courses/<int:id>/delete/', views.courses_delete, name='courses_delete'),
]
