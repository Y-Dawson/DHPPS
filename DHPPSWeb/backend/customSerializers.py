from rest_framework import serializers
from backend.models import Accountinformation, Casedata, Cityposition, Dailyforecastdata
from backend.models import Initcitydata, Initroaddata, Logindata, Modeldata, Personalprofile, Theme


class AccountinformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accountinformation
        fields = '__all__'


class CasedataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Casedata
        fields = '__all__'


class CitypositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cityposition
        fields = '__all__'


class DailyforecastdataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dailyforecastdata
        fields = '__all__'


class InitcitydataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Initcitydata
        fields = '__all__'


class InitroaddataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Initroaddata
        fields = '__all__'


class LogindataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logindata
        fields = '__all__'


class ModeldataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modeldata
        fields = '__all__'


class PersonalprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personalprofile
        fields = '__all__'


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'
