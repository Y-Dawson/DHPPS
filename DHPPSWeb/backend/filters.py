import django_filters

from backend.models import Casedata


class CaseFilter(django_filters.rest_framework.FilterSet):
    """
    案例过滤器
    """
    userid = django_filters.NumberFilter(field_name='userid')

    class Meta:
        model = Casedata
        fields = ['userid']
