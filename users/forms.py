from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

    
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        exclude = ['owner']
