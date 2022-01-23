from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from projects.models import Project
from .forms import ProjectForm, ReviewForm


class ProjectIndexView(generic.ListView):
    model = Project
    paginate_by = 6
    template_name = 'projects/index.html'

    def get_queryset(self, *args, **kwargs):
        search_query = self.request.GET.get('search_query')
        if search_query:
            projects = Project.objects.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(owner__name__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
            return projects
        else:
            projects = super().get_queryset(*args, **kwargs)
            return projects

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search_query'] = self.request.GET.get('search_query') or ''
        return context



def project_detail(request, pk):
    project = get_object_or_404(Project, id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_obj = form.save(commit=False)
            review_obj.owner = request.user.profile
            review_obj.project = project
            review_obj.save()
            project.refresh_votes
            messages.success(request, 'Your review successfully added!')
            return redirect('projects:detail', pk=pk)


    context = {
        'project': project,
        'form': form
    }
    return render(request, 'projects/project_detail.html', context)



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