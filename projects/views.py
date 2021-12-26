from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required

from projects import models
from .forms import ProjectForm


class ProjectIndexView(generic.ListView):
    model = models.Project
    template_name = 'projects/index.html'


class ProjectDetailView(generic.DetailView):
    model = models.Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'


@login_required(login_url='users:login_user')
def createproject(requeset):
    form = ProjectForm()

    if requeset.method == "POST":
        form = ProjectForm(requeset.POST, files=requeset.FILES)
        if form.is_valid():
            profile = requeset.user.profile
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('users:user_account')

    context = {
        'form': form
    }

    return render(requeset, 'projects/project_form.html', context)


@login_required(login_url='users:login_user')
def updateproject(request, p_uuid):
    profile = request.user.profile
    project = get_object_or_404(profile.project_set, id=p_uuid)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, files=request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('users:user_account')

    context = {
        'form': form
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='users:login_user')
def deleteproject(request, p_uuid):
    profile = request.user.profile
    project = get_object_or_404(profile.project_set, id=p_uuid)
    if request.method == "POST":
        project.delete()
        return redirect('users:user_account')

    context = {
        'project': project
    }
    return render(request, 'projects/delete_project.html', context)