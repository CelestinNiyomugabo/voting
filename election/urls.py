from django.urls import path
from election import views
from .views import voting_form, send_otp, verify_otp, ConntestCreate, ContestUpdate, ContestView, ContestDelete, ConntestantCreate
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.election_list , name="home"),
    path('about/',views.about , name="about"),
    path('form/<int:contest_id>/', voting_form, name='voting_form'),
    path('submit/', views.submit_vote, name='submit_vote'),
    path('send_otp/', send_otp, name='send_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('add_contest/', ConntestCreate.as_view(), name='add_contest'),
    path('edit_contest/', ContestUpdate.as_view(), name='edit_contest'),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('test_otp/', views.test_otp, name='test_otp'),
    path('contest/<int:pk>/edit/', ContestUpdate.as_view(), name='contest_edit'),
    path('contest/<int:pk>/delete/', ContestDelete.as_view(), name='contest_delete'),
    path('contest/<int:pk>/', ContestView.as_view(), name='contest'),
    path('add_contestant/<int:pk>/', ContestView.as_view(), name='add_contestant'),
    path('add_contestant/', ConntestantCreate.as_view(), name='add_contestant'),
    path('dashboard/', views.dashboard, name='dashboard'),
    

    
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
