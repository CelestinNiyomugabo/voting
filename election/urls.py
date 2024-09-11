from django.urls import path
from election import views
from .views import voting_form

urlpatterns = [
    path('',views.election_list , name="home"),
    path('about/',views.about , name="about"),
    path('form/<int:contest_id>/', voting_form, name='voting_form'),
    path('submit/', views.submit_vote, name='submit_vote'),
]