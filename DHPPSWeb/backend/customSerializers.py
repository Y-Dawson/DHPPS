from rest_framework import serializers
from backend.models import AccountInformation, CaseData, CityPosition, DailyForecastData
from backend.models import InitCityData, InitRoadData, LoginData, Authority, PersonalProfile, CaseMode
from rest_framework.serializers import SerializerMethodField

class CaseModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseMode
        fields = '__all__'


class AuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Authority
        fields = '__all__'


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


class PersonalProfileSerializer(serializers.ModelSerializer):
    # 为头像URL生成一个只读字段，返回给前端
    avatarUrl = serializers.SerializerMethodField("GetAvatarUrl")

    # DRF对于只读字段SerializerMethodField的生成函数
    def GetAvatarUrl(self, obj):
        return "http://47.112.227.85" + obj.avatar.url

    class Meta:
        model = PersonalProfile
        fields = '__all__'
