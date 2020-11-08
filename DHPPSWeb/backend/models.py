# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
# * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Authoritydata(models.Model):
    id = models.ForeignKey('Userinforrmation', models.DO_NOTHING, db_column='ID', blank=True, null=True)  # Field name made lowercase.
    authority = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'authoritydata'


class Casedata(models.Model):
    caseid = models.OneToOneField('Userinforrmation', models.DO_NOTHING, db_column='caseID', primary_key=True)  # Field name made lowercase.
    id = models.CharField(db_column='ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    casename = models.CharField(db_column='caseName', max_length=50)  # Field name made lowercase.
    citynumber = models.CharField(db_column='cityNumber', max_length=50)  # Field name made lowercase.
    road = models.IntegerField()
    inittotal = models.BigIntegerField(db_column='initTotal')  # Field name made lowercase.
    inittotalinfected = models.BigIntegerField(db_column='initTotalInfected')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'casedata'


class Cityposition(models.Model):
    cityid = models.ForeignKey('Initcitydata', models.DO_NOTHING, db_column='cityID', blank=True, null=True)  # Field name made lowercase.
    x = models.FloatField()
    y = models.FloatField()

    class Meta:
        managed = False
        db_table = 'cityposition'


class Dailyforecastdata(models.Model):
    nowdate = models.DateField(db_column='nowDate', primary_key=True)  # Field name made lowercase.
    cityid = models.ForeignKey('Initcitydata', models.DO_NOTHING, db_column='cityID', blank=True, null=True)  # Field name made lowercase.
    population = models.BigIntegerField(db_column='Population')  # Field name made lowercase.
    infected = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'dailyforecastdata'


class Initcitydata(models.Model):
    cityid = models.OneToOneField(Cityposition, models.DO_NOTHING, db_column='cityID', primary_key=True)  # Field name made lowercase.
    caseid = models.ForeignKey(Casedata, models.DO_NOTHING, db_column='caseID', blank=True, null=True)  # Field name made lowercase.
    cityname = models.CharField(db_column='cityName', max_length=50)  # Field name made lowercase.
    initpop = models.BigIntegerField(db_column='initPop')  # Field name made lowercase.
    initinfect = models.BigIntegerField(db_column='initInfect')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'initcitydata'


class Initroaddata(models.Model):
    roadid = models.CharField(db_column='roadID', primary_key=True, max_length=50)  # Field name made lowercase.
    caseid = models.ForeignKey(Casedata, models.DO_NOTHING, db_column='caseID', blank=True, null=True)  # Field name made lowercase.
    departure = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    volume = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'initroaddata'


class Logindata(models.Model):
    id = models.ForeignKey('Userinforrmation', models.DO_NOTHING, db_column='ID', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='passWord', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'logindata'


class Modeldata(models.Model):
    layerid = models.CharField(db_column='layerID', primary_key=True, max_length=20)  # Field name made lowercase.
    layername = models.CharField(db_column='layerName', max_length=20)  # Field name made lowercase.
    layerparm = models.CharField(db_column='layerParm', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'modeldata'


class Userdata(models.Model):
    id = models.ForeignKey('Userinforrmation', models.DO_NOTHING, db_column='ID', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='userName', max_length=50)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=11)  # Field name made lowercase.
    sex = models.IntegerField()
    address = models.CharField(max_length=200)
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    birth = models.DateField()

    class Meta:
        managed = False
        db_table = 'userdata'


class Userinforrmation(models.Model):
    id = models.OneToOneField(Logindata, models.DO_NOTHING, db_column='ID', primary_key=True)  # Field name made lowercase.
    createdate = models.DateField(db_column='createDate')  # Field name made lowercase.
    remark = models.CharField(max_length=200)
    casenumber = models.IntegerField(db_column='caseNumber')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userinforrmation'
