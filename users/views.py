from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Profile



def all_profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'users/profiles.html', context)


def single_profile(request, pk):
    profile = get_object_or_404(Profile, id=pk)

    top_skills = profile.skill_set.exclude(description='')
    other_skills = profile.skill_set.filter(description='')
    context = {
        'profile': profile,
        'top_skills': top_skills,
        'other_skills': other_skills
    }
    return render(request, 'users/single_profile.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('users:profiles')

    if request.method == 'POST':
        uname = request.POST['username']
        upwd = request.POST['password']
        try:
            User.objects.get(username=uname)
        except User.DoesNotExist:
            messages.error(request, "Username does not exist!")
            return redirect('users:login_user')
        
        user = authenticate(request, username=uname, password=upwd)
        if user:
            login(request, user)
            return redirect('users:profiles')
        else:
            messages.error(request, 'Username or password is incorrect')
            return redirect('users:login_user')
    
    return render(request, 'users/login_register.html')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.error(request, 'User was logged out!')
        return redirect('users:login_user')

