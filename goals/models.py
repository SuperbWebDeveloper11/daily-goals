from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now =True)

    class Meta:
        abstract = True
        ordering = ('-created', )


class Dailygoal(TimeStampedModel):
    date = models.DateField()
    tags = TaggableManager(blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='daily_goals', on_delete=models.CASCADE)

    def __str__(self):
        return self.date

    def get_absolute_url(self):
        return reverse('goals:daily_goal', kwargs={'pk', self.pk})


class Task(TimeStampedModel):
    STATUS_CHOICES = ( ("done", "Done"), ("undone", "Undone"),)

    task = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='undone')

    daily_goal = models.ForeignKey(Dailygoal, related_name='tasks', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='daily_goal_tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.task


