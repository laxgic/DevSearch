from django.db.models.query import RawQuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

from projects import models
from .forms import ProjectForm


class ProjectIndexView(generic.ListView):
    model = models.Project
    template_name = 'projects/index.html'


class ProjectDetailView(generic.DetailView):
    model = models.Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'


def createproject(requeset):
    form = ProjectForm()

    if requeset.method == "POST":
        form = ProjectForm(requeset.POST)
        if form.is_valid():
            form.save()
            return redirect('projects:index')

    context = {
        'form': form
    }

    return render(requeset, 'projects/project_form.html', context)


def updateproject(request, p_uuid):
    project = get_object_or_404(models.Project, id=p_uuid)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:index')

    context = {
        'form': form
    }
    return render(request, 'projects/project_form.html', context)


def deleteproject(request, p_uuid):
    project = get_object_or_404(models.Project, id=p_uuid)

    if request.method == "POST":
        project.delete()
        return redirect('projects:index')

    context = {
        'project': project
    }
    return render(request, 'projects/delete_project.html', context)