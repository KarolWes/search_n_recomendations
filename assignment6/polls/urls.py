from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_firstpage, name="get_firstpage"),
    path('handle_userid_input', views.handle_userid_input, name="handle_userid_input"),
    path('recommendations', views.get_recommendations, name="get_recommendations")
]
