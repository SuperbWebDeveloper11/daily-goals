from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
# import models
from ..models import Task, Dailygoal
from ..forms import TaskCreationForm, TaskEditionForm # we'll use this form to create and update instance


"""
function based views (hardcoded) to perform crud operations for ajax requests
    1- create_task (return create template on get && save new instance on post)
    2- update_task (return update template on get && update instance on post)
    3- delete_task (return delete template on get && delete instance on post)
    4- change_task_status (change task status on get)
"""

def create_task(request, daily_pk):
    """ return create template on get && create new instance on post"""

    error_template = 'goals/tasks/partial_error_msg.html'
    create_template = 'goals/tasks/partial_task_create.html'
    template_list = 'goals/tasks/partial_task_list.html'

    try:
        if not request.user.is_authenticated: # raise an exception 
            raise 

        else:
            if request.method == 'GET': # return create template 
                context = {'form': TaskCreationForm(), 'daily_pk':daily_pk}
                template = render_to_string(create_template, context, request=request)
                return JsonResponse({'modal_temp': template})

            elif request.method == 'POST': # create new instance && return list template 
                form = TaskCreationForm(request.POST, request.FILES)
                if form.is_valid(): 
                    # create new instance 
                    daily_goal = Dailygoal.objects.get(pk=daily_pk)
                    form.instance.created_by = request.user
                    form.instance.daily_goal = daily_goal
                    form.save() 
                    # return list template 
                    context = {'daily_goal': daily_goal}
                    list_temp = render_to_string(template_list, context, request=request)
                    return JsonResponse({'list_temp': list_temp, 'form_is_valid': True})
                else:
                    # return create template with error messages
                    context = {'form': form}
                    template = render_to_string(create_template, context, request=request)
                    return JsonResponse({'modal_temp': template, 'form_is_valid': False})
    except: 
        template = render_to_string(error_template, request=request)
        return JsonResponse({'modal_temp': template})


def update_task(request, daily_pk, pk):
    """ return update template on get && update instance on post"""

    error_template = 'goals/tasks/partial_error_msg.html'
    update_template = 'goals/tasks/partial_task_update.html'
    template_list = 'goals/tasks/partial_task_list.html'

    try:
        if not request.user.is_authenticated: 
            raise
        else:
            task_instance = Task.objects.get(daily_goal=daily_pk, pk=pk)

            if request.user != task_instance.created_by: # the user should be the one who created the tasks 
                raise

            if request.method == 'GET': # return update template 
                context = {'form': TaskEditionForm(instance=task_instance)}
                template = render_to_string(update_template, context, request=request)
                return JsonResponse({'modal_temp': template})

            elif request.method == 'POST': # update instance and return list template 
                form = TaskEditionForm(request.POST, request.FILES, instance=task_instance)
                if form.is_valid(): 
                    # update instance 
                    form.save() 
                    # return list template 
                    context = {'daily_goal': form.instance.daily_goal}
                    list_temp = render_to_string(template_list, context, request=request)
                    return JsonResponse({'list_temp': list_temp, 'form_is_valid': True})
                else:
                    # return update template with error messages
                    context = {'form': form}
                    template = render_to_string(update_template, context, request=request)
                    return JsonResponse({'modal_temp': template, 'form_is_valid': False})
    except: 
        template = render_to_string(error_template, request=request)
        return JsonResponse({'modal_temp': template})


def delete_task(request, daily_pk, pk):
    """ return delete template on get && delete instance on post"""

    error_template = 'goals/tasks/partial_error_msg.html'
    delete_template = 'goals/tasks/partial_task_delete.html'
    template_list = 'goals/tasks/partial_task_list.html'

    try:
        if not request.user.is_authenticated: 
            raise
        else:
            task_instance = Task.objects.get(daily_goal=daily_pk, pk=pk)

            if request.user != task_instance.created_by: # the user should be the one who created the tasks 
                raise

            if request.method == 'GET': # return delete template 
                context = {'daily_pk': daily_pk, 'pk': pk}
                template = render_to_string(delete_template, context, request=request)
                return JsonResponse({'modal_temp': template})

            elif request.method == 'POST': # update instance and return list template 
                task_instance.delete()
                daily_goal = Dailygoal.objects.get(pk=daily_pk)
                context = {'daily_goal': daily_goal}
                template = render_to_string(template_list, context, request=request)
                return JsonResponse({'list_temp': template, 'form_is_valid': True})
    except: 
        template = render_to_string(error_template, request=request)
        return JsonResponse({'modal_temp': template})


def change_task_status(request, daily_pk, pk):
    """ change stauts and return list of instances on get """

    error_template = 'goals/tasks/partial_error_msg.html'
    template_list = 'goals/tasks/partial_task_list.html'

    try:
        if not request.user.is_authenticated: 
            raise
        else:
            task_instance = Task.objects.get(daily_goal=daily_pk, pk=pk)

            if request.user != task_instance.created_by: # the user should be the one who created the tasks 
                raise

            if request.method == 'GET': # return delete template 
                if task_instance.status == 'done':
                    task_instance.status = 'undone'
                    task_instance.save()
                else:
                    task_instance.status = 'done'
                    task_instance.save()

                daily_goal = Dailygoal.objects.get(pk=daily_pk)
                context = {'daily_goal': daily_goal}
                template = render_to_string(template_list, context, request=request)
                return JsonResponse({'list_temp': template})
    except: 
        template = render_to_string(error_template, request=request)
        return JsonResponse({'modal_temp': template})



