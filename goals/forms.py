from django import forms
from .models import Dailygoal, Task


# This could be used to display html5 date input
# however it's not neccessary when using widget-tweaks : {% render_field form.date type="date" class="form-control" %}
class DateInput(forms.DateInput):
    input_type = 'date'


class DailygoalForm(forms.ModelForm):
    class Meta:
        model = Dailygoal
        fields = ['date', 'tags']
        widgets = {"date": DateInput}


# I will use this form to create tasks for the first time
class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task']


# I will use this form to edit tasks 
class TaskEditionForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task', 'status']

