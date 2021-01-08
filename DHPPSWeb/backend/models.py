# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import uuid
import os
from _datetime import date
from django.utils import timezone


class CaseMode(models.Model):
    modeNo = models.AutoField(db_column='modeNo', primary_key=True)  # Field name made lowercase.
    modeValue = models.CharField(db_column='modeValue', max_length=20)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'CaseMode'


class Authority(models.Model):
    authorityNo = models.AutoField(db_column='authorityNo', primary_key=True)  # Field name made lowercase.
    authorityValue = models.CharField(db_column='authorityValue', max_length=20)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'Authority'


class AccountInformation(models.Model):
    userId = models.AutoField(db_column='userId', primary_key=True)  # Field name made lowercase.
    createDate = models.DateField(db_column='createDate', default=timezone.now)  # Field name made lowercase.
    remark = models.CharField(max_length=200, default='无备注')
    caseNumber = models.IntegerField(db_column='caseNumber', default=0)  # Field name made lowercase.
    authority = models.ForeignKey(Authority, models.CASCADE, db_column='authority', default='1')

    class Meta:
        # managed = False
        db_table = 'AccountInformation'


class CaseData(models.Model):
    caseId = models.AutoField(db_column='caseId', primary_key=True)  # Field name made lowercase.
    userId = models.ForeignKey(AccountInformation, models.CASCADE, db_column='userId')  # Field name made lowercase.
    caseName = models.CharField(db_column='caseName', max_length=50, default='未命名')  # Field name made lowercase.
    caseMode = models.ForeignKey(CaseMode, models.CASCADE, db_column='caseMode')
    caseCreateDate = models.DateField(db_column='caseCreateDate', default=timezone.now)  # Field name made lowercase.
    cityNumber = models.IntegerField(db_column='cityNumber')  # Field name made lowercase.
    roadNumber = models.IntegerField(db_column='roadNumber')  # Field name made lowercase.
    initTotal = models.BigIntegerField(db_column='initTotal')  # Field name made lowercase.
    initTotalInfected = models.BigIntegerField(db_column='initTotalInfected')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'CaseData'


class InitCityData(models.Model):
    cityId = models.AutoField(db_column='cityId', primary_key=True)  # Field name made lowercase.
    caseId = models.ForeignKey(CaseData, models.CASCADE, db_column='caseId')  # Field name made lowercase.
    cityName = models.CharField(db_column='cityName', max_length=50)  # Field name made lowercase.
    initPop = models.BigIntegerField(db_column='initPop', default=0)  # Field name made lowercase.
    initInfect = models.BigIntegerField(db_column='initInfect', default=0)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'InitCityData'


class CityPosition(models.Model):
    cityId = models.OneToOneField(InitCityData, models.CASCADE, db_column='cityId', primary_key=True)  # Field name made lowercase.
    x = models.FloatField()
    y = models.FloatField()

    class Meta:
        # managed = False
        db_table = 'CityPosition'


class DailyForecastData(models.Model):
    date = models.DateField(primary_key=True)
    cityId = models.ForeignKey(InitCityData, models.CASCADE, db_column='cityId')  # Field name made lowercase.
    population = models.BigIntegerField()
    infected = models.BigIntegerField()

    class Meta:
        # managed = False
        db_table = 'DailyForecastData'


class InitRoadData(models.Model):
    roadId = models.AutoField(db_column='roadId', primary_key=True)  # Field name made lowercase.
    caseId = models.ForeignKey(CaseData, models.CASCADE, db_column='caseId')  # Field name made lowercase.
    departure = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    volume = models.BigIntegerField()

    class Meta:
        # managed = False
        db_table = 'InitRoadData'


class LoginData(models.Model):
    userId = models.OneToOneField(AccountInformation, models.CASCADE, db_column='userId', primary_key=True)  # Field name made lowercase.
    userPassword = models.CharField(db_column='userPassword', max_length=32)  # Field name made lowercase.
    salt = models.CharField(max_length=20)

    class Meta:
        # managed = False
        db_table = 'LoginData'


def UserDirectoryPath(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # return the whole path to the file
    return os.path.join(instance.userId, "avatar", filename)


class PersonalProfile(models.Model):
    userId = models.OneToOneField(AccountInformation, models.CASCADE, db_column='userId', primary_key=True)  # Field name made lowercase.
    avatar = models.ImageField(upload_to="avatar", verbose_name="头像", default="defaultFiles/defaultAvatar.png")
    userName = models.CharField(db_column='userName', max_length=50)  # Field name made lowercase.
    phoneNumber = models.CharField(db_column='phoneNumber', max_length=11)  # Field name made lowercase.
    sex = models.CharField(max_length=10, default='保密')
    address = models.CharField(max_length=200, default='保密')
    email = models.CharField(db_column='Email', max_length=50, default='保密')  # Field name made lowercase.
    birth = models.DateField(default=timezone.now().date())

    def GetAvatarUrl(self):
        return "http://47.112.227.85/media/" + str(self.avatar)

    class Meta:
        # managed = False
        db_table = 'PersonalProfile'
