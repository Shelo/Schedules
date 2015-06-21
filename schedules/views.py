import copy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from schedules import util


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

    # find if the submitter is already a member.
    user = request.user

    # check if the membership exists.
    if not models.Membership.objects.filter(user=user, project=found_project).exists():
        return redirect(reverse(home))

    # retrieve block status.
    members = found_project.membership_set.all()

    member_names = set([member.user.get_full_name() for member in members])

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
                block_status[day][block_number] = copy.deepcopy(member_names)

            block_status[day][block_number].discard(block.membership.user.get_full_name())

    # check if the user is the owner.
    is_owner = request.user.id == found_project.owner.id

    return render(request, 'project.html', {
        'project': found_project,
        'blocks': block_status,
        'block_loops': range(1, 15),
        'day_loops': range(7),
        'total': total,
        'all_members': member_names,
        'is_owner': is_owner
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
    if request.method == "GET":
        return redirect(home)

    name = request.POST['name']
    short_description = request.POST['short_description']

    if name and short_description:
        project = models.Project(name=name, owner=request.user, short_description=short_description)
        project.save()

        # create a membership for the owner.
        membership = models.Membership(user=request.user, project=project)
        membership.save()

    return redirect(home)


@login_required
def add_member(request, project_slug):
    project = get_object_or_404(models.Project, slug=project_slug)

    # find if the submitter is already a member.
    if not util.user_is_member(request, project, models.Membership):
        return HttpResponse()

    # then continue, everything is alright.
    username = request.POST['username']

    if not username:
        return HttpResponse("false")

    user = models.User.objects.filter(username=username).get()

    # check if the membership exists.
    if models.Membership.objects.filter(user=user, project=project).exists():
        return HttpResponse("")

    # if not, add it.
    membership = models.Membership(user=user, project=project)
    membership.save()

    return HttpResponse("true")


@login_required
def query_users(request):
    term = request.GET['term']

    query = Q(username__contains=term) | Q(first_name__contains=term) | Q(email__contains=term)
    matches = models.User.objects.filter(query)[:10]

    users = []
    for match in matches:
        users.append(match.username)

    return JsonResponse(users, safe=False)


@login_required
def query_project_members(request, project_slug):
    project = get_object_or_404(models.Project, slug=project_slug)

    # find if the submitter is already a member.
    if not util.user_is_member(request, project, models.Membership):
        return HttpResponse()

    owner = project.owner.username;

    users = []
    for membership in project.membership_set.all():
        if membership.user.username == owner:
            continue

        users.append({
            'username': membership.user.username,
            'fullname': membership.user.get_full_name()
        })

    return JsonResponse(users, safe=False)


@login_required
def query_remove_member(request, project_slug):
    project = get_object_or_404(models.Project, slug=project_slug)

    # find if the submitter is the owner.
    if project.owner_id != request.user.id:
        return JsonResponse(False, safe=False)

    if 'username' not in request.POST:
        return JsonResponse(False, safe=False)

    username = request.POST['username']

    # find membership.
    membership_filter = project.membership_set.filter(username=username)
    if not membership_filter.exists():
        return JsonResponse(False, safe=False)

    membership = membership_filter.get()
    membership.delete()

    return JsonResponse(True, safe=False)

