from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from backend import models
from backend import serializers
# Create your views here.


def index(request):
    """
    render index page
    :param request: request object
    :return: page
    """
    return render(request, 'index.html')


class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Accountinformation.objects.all()
    serializer_class = serializers.AccountinformationSerializer


class CaseViewSet(viewsets.ModelViewSet):
    queryset = models.Casedata.objects.all()
    serializer_class = serializers.CasedataSerializer


class CityPosViewSet(viewsets.ModelViewSet):
    queryset = models.Cityposition.objects.all()
    serializer_class = serializers.CitypositionSerializer


class DailyForeViewSet(viewsets.ModelViewSet):
    queryset = models.Dailyforecastdata.objects.all()
    serializer_class = serializers.DailyforecastdataSerializer


class InitCityViewSet(viewsets.ModelViewSet):
    queryset = models.Initcitydata.objects.all()
    serializer_class = serializers.InitcitydataSerializer


class InitRoadViewSet(viewsets.ModelViewSet):
    queryset = models.Initroaddata.objects.all()
    serializer_class = serializers.InitroaddataSerializer


class LoginViewSet(viewsets.ModelViewSet):
    queryset = models.Logindata.objects.all()
    serializer_class = serializers.LogindataSerializer


class ModelViewSet(viewsets.ModelViewSet):
    queryset = models.Modeldata.objects.all()
    serializer_class = serializers.ModeldataSerializer


class PersonalProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Personalprofile.objects.all()
    serializer_class = serializers.PersonalprofileSerializer


class ThemeViewSet(viewsets.ModelViewSet):
    queryset = models.Theme.objects.all()
    serializer_class = serializers.ThemeSerializer
