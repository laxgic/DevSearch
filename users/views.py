from django.shortcuts import render
from django.shortcuts import get_object_or_404

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