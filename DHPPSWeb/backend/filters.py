import django_filters

from backend.models import Casedata, Accountinformation


class CaseFilter(django_filters.rest_framework.FilterSet):
    """
    案例过滤器
    """
    userid = django_filters.NumberFilter(field_name='userid')

    class Meta:
        model = Casedata
        fields = ['userid']


class AccountInfoFilter(django_filters.rest_framework.FilterSet):
    """
    个人信息过滤器
    """
    authority = django_filters.CharFilter(field_name='authority')

    class Meta:
        model = Accountinformation
        fields = ['authority']
