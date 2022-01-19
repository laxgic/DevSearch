from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm


def my_paginator(request, query_set):
    requested_page_num = request.GET.get('page')
    paginator_obj = Paginator(query_set, per_page=6)
    try:
        page = paginator_obj.page(requested_page_num)
    except PageNotAnInteger:
        page = paginator_obj.page(number=1)
    except EmptyPage:
        page_num = paginator_obj.num_pages
        page = paginator_obj.page(number=page_num)
    
    start_index = page.number - 2
    if start_index < 1:
        start_index = 1

    end_index = page.number + 2
    if end_index > paginator_obj.num_pages:
        end_index = paginator_obj.num_pages

    page_range = range(start_index, end_index+1)

    return page, page_range


def all_profiles(request):
    search_query = request.GET.get('search_query') or ''

    if search_query:
        profiles = Profile.objects.filter(
            Q(name__icontains=search_query) |
            Q(short_intro__icontains=search_query) |
            Q(skill__name__iexact=search_query)
        ).distinct()

    else:
        profiles = Profile.objects.all()
    
    # pagination the profiles
    profiles, page_range = my_paginator(request, profiles)

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'page_range': page_range
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

    context = {'page': 'login'}
    return render(request, 'users/login_register.html', context)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.error(request, 'User was logged out!')
        return redirect('users:login_user')


def register_user(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, "User account was created!")
            return redirect('users:edit_account')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'page': 'register', 'form': form}
    return render(request, 'users/login_register.html', context)


@login_required(login_url='users:login_user')
def user_account(request):
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'users/account.html', context)


@login_required(login_url='users:login_user')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated Successfuly!")
            return redirect('users:user_account')
        else:
            messages.error(request, 'Your form is not valid!')
    
    context = {'form': form}
    return render(request, 'users/edit_profile.html', context)


@login_required(login_url='users:login_user')
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            profile = request.user.profile
            skill.owner = profile
            skill.save()

            messages.success(request, 'skill added successfuly!')
            return redirect('users:user_account')

        else:
            messages.error(request, 'Your form is not valid!')

    form = SkillForm()
    conetxt = {'form': form}
    return render(request, 'users/skill_form.html', conetxt)


@login_required(login_url='users:login_user')
def update_skill(request, pk):
    profile = request.user.profile
    skill = get_object_or_404(profile.skill_set, id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill Updated successfuly!')
            return redirect('users:user_account')
        else:
            messages.error(request, 'Your form is not valid!')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='users:login_user')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = get_object_or_404(profile.skill_set, id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'the "{}" skill deleted'.format(skill.name))
        return redirect('users:user_account')

    context = {'skill': skill}
    return render(request, 'users/delete_skill.html', context)