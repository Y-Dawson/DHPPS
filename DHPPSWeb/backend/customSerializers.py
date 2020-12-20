from rest_framework import serializers
from backend.models import AccountInformation, CaseData, CityPosition, DailyForecastData
from backend.models import InitCityData, InitRoadData, LoginData, ModelData, PersonalProfile, Theme


class AccountInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountInformation
        fields = '__all__'


class CaseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseData
        fields = '__all__'


class CitypositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityPosition
        fields = '__all__'


class DailyforecastdataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyForecastData
        fields = '__all__'


class InitcitydataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitCityData
        fields = '__all__'


class InitroaddataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitRoadData
        fields = '__all__'


class LogindataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginData
        fields = '__all__'


class ModeldataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelData
        fields = '__all__'


class PersonalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalProfile
        fields = '__all__'


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'
