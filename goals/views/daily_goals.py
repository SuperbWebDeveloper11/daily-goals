from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.files.storage import FileSystemStorage
import datetime
from ..models import Dailygoal
from ..filters import DailygoalFilter
from ..forms import DailygoalForm


"""
function based views (hardcoded) to perform crud operations for daily goals
    - daily_goals_index(request): return daily goals list
    - daily_goal_details(request, pk): return daily goal detail
    - create_daily_goal(request): create daily goal
    - edit_daily_goal(request, pk): edit daily goal
    - delete_daily_goal(request, pk): delete daily goal
    - download_daily_goals(request): download daily goals list as pdf using weasyprint
    - download_daily_goal(request, pk): download daily goal details as pdf using weasyprint
"""


@login_required
def daily_goals_index(request):
    # retrieve goals of the logged in user
    daily_goals = Dailygoal.objects.filter(created_by=request.user)
    # use django-filter to filter daily goals based on model attributes
    daily_goals_filter = DailygoalFilter(request.GET, queryset=daily_goals)
    context = {'daily_goals_filter': daily_goals_filter}
    return render(request, 'goals/daily_goals/daily_goals_index.html', context)



@login_required
def daily_goal_details(request, pk):
    daily_goal = get_object_or_404(Dailygoal, pk=pk, created_by=request.user)
    context = {'daily_goal': daily_goal}
    return render(request, 'goals/daily_goals/daily_goal_details.html', context)


@login_required
def create_daily_goal(request):
    form = DailygoalForm()

    if request.method == 'POST':
        form = DailygoalForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            messages.success(request, 'your daily goal has been created successfuly')
            return HttpResponseRedirect(reverse('goals:daily_goal_details', args=(form.instance.id,)))
        else:
            messages.error(request, 'error when creating daily goal')

    context = {'form': form}
    return render(request, 'goals/daily_goals/create_daily_goal.html', context)


@login_required
def edit_daily_goal(request, pk):

    daily_goal = get_object_or_404(Dailygoal, pk=pk, created_by=request.user)
    form = DailygoalForm(instance=daily_goal)

    if request.user != daily_goal.created_by:
        return HttpResposen("you don't have permission")

    if request.method == 'POST':
        form = DailygoalForm(data=request.POST, instance=daily_goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'your daily goal has been edited successfuly')
            return HttpResponseRedirect(reverse('goals:daily_goal_details', args=(form.instance.id,)))
        else:
            messages.error(request, 'error when editing daily goal')

    context = {'form': form}
    return render(request, 'goals/daily_goals/edit_daily_goal.html', context)


@login_required
def delete_daily_goal(request, pk):

    daily_goal = get_object_or_404(Dailygoal, pk=pk, created_by=request.user)

    if request.user != daily_goal.created_by:
        return HttpResposen("you don't have permission")

    if request.method == 'POST':
        daily_goal.delete()
        messages.error(request, 'your daily goals has been deleted')
        return redirect("goals:daily_goals_list")

    context = {'daily_goal': daily_goal}
    return render(request, 'goals/daily_goals/delete_daily_goal.html', context)


@login_required
def download_daily_goals(request):

    daily_goals = Dailygoal.objects.filter(created_by=request.user)
    context = {'daily_goals': daily_goals, 'date': datetime.datetime.now()}
    html_string = render_to_string('goals/daily_goals/daily_goals_index_pdf.html', context, request=request)

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
        return response


@login_required
def download_daily_goal(request, pk):

    daily_goal = get_object_or_404(Dailygoal, pk=pk)
    context = {'daily_goal': daily_goal, 'date': datetime.datetime.now()}
    html_string = render_to_string('goals/daily_goals/daily_goal_details_pdf.html', context, request=request)

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
        return response


