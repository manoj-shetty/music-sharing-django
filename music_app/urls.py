from music_app.views import home
from django.urls import path
from music_app.views import upload_music, my_music
from music_app.views import register, user_login, user_logout
from . import views


urlpatterns = [
   
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('check-email/', views.check_email_exists, name='check_email_exists'),
]
