

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import MusicFile
from django.contrib.auth.decorators import login_required
from .forms import MusicFileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm
from django.db import models
from music_app.models import MusicFile
from music_app.forms import UserRegistrationForm
from django.http import JsonResponse
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        user = request.user
        user_music_files = MusicFile.objects.filter(uploaded_by=user)
        public_music_files = MusicFile.objects.filter(access_type=MusicFile.PUBLIC)
        protected_music_files = MusicFile.objects.filter(allowed_emails__contains=user.email)
    else:
        user_music_files = []
        public_music_files = MusicFile.objects.filter(access_type=MusicFile.PUBLIC)
        protected_music_files = []

    return render(request, 'home.html', {'user_music_files': user_music_files, 'public_music_files': public_music_files, 'protected_music_files': protected_music_files})


@login_required
def upload_music(request):
    if request.method == 'POST':
        form = MusicFileForm(request.POST, request.FILES)
        if form.is_valid():
            music_file = form.save(commit=False)
            music_file.uploaded_by = request.user
            music_file.save()
            return redirect('home')
    else:
        form = MusicFileForm()
    return render(request, 'upload_music.html', {'form': form})


@login_required
def my_music(request):
    music_files = MusicFile.objects.filter(uploaded_by=request.user)
    return render(request, 'my_music.html', {'music_files': music_files})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def check_email_exists(request):
    email = request.GET.get('email', None)
    data = {
        'exists': User.objects.filter(email=email).exists()
    }
    return JsonResponse(data)
