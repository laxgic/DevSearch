from django import forms
from django.forms import ModelForm
from django import forms
from .models import Project, Review



class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'demo_link', 'source_link', 'tags']

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }