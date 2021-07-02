import django_filters
from .models import Dailygoal


class DailygoalFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(field_name='tags__name')

    class Meta:
        model = Dailygoal
        fields = {
                'date': ['exact', ],
        }

