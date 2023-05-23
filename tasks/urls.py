
from django.urls import path
from . import views

app_name="tasks"
urlpatterns=[
    path('',views.main_menu,name="main"),
    path('generate',views.generate_screen),
    path('list',views.list_screen,name="list"),
    path('retrieve',views.retrieve_screen),
    path('logout',views.logout_func),
]