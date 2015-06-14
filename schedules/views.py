from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from . import models

def index(request):
    if request.user.is_authenticated():
        return redirect(reverse(home))

    return render(request, "index.html")


def log_in(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect(reverse(home))

    return redirect(reverse(index))

@login_required
def home(request):
    memberships = request.user.membership_set.all()
    projects = [membership.project for membership in memberships]

    projects_own = models.Project.objects.filter(owner=request.user)

    return render(request, 'home.html', {
        'projects': projects,
        'projects_own': projects_own
    })


@login_required
def project(request, project_slug):
    found_project = get_object_or_404(models.Project, slug=project_slug)

    members = found_project.membership_set.all()

    total = len(members)
    block_status = {}

    for member in members:
        blocks = member.occupiedblock_set.all()

        for block in blocks:
            day = block.day
            block_number = block.block

            if day not in block_status:
                block_status[day] = {}

            if block_number not in block_status[day]:
                block_status[day][block_number] = []

            block_status[day][block_number].append(block.membership.user.get_full_name())

    return render(request, 'project.html', {
        'project': found_project,
        'blocks': block_status,
        'block_loops': range(1, 15),
        'day_loops': range(7),
        'total': total,
    })


@login_required
def submit_schedule(request, project_slug):
    found_project = get_object_or_404(models.Project, slug=project_slug)

    return render(request, "submit-schedule.html", {
        'project': found_project,
        'block_loops': range(1, 15),
        'day_loops': range(7),
    })

@login_required
def log_out(request):
    logout(request)

    return redirect(reverse(index))


@login_required
def create_project(request):
    return render(request, "create_project.html", {

    })


@login_required
def submit_project(request):
    if request.method == "GET":
        return redirect(create_project)

    name = request.POST['name']
    users = request.POST['users']
    short_description = request.POST['short_description']

    if name and short_description:
        project = models.Project(name=name, owner=request.user, short_description=short_description)
        project.save()

        user_list = users.split(",")
        user_list.append(request.user)

        for user in user_list:
            if user:
                user_object = models.User.objects.filter(username=user).all()

                if len(user_object) == 1:
                    membership = models.Membership(user=user_object[0], project=project)
                    membership.save()

    return redirect(home)
