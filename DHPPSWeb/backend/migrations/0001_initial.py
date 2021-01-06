# Generated by Django 3.0.6 on 2021-01-06 02:11

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountInformation',
            fields=[
                ('userId', models.AutoField(db_column='userId', primary_key=True, serialize=False)),
                ('createDate', models.DateField(db_column='createDate', default=django.utils.timezone.now)),
                ('remark', models.CharField(default='无备注', max_length=200)),
                ('caseNumber', models.IntegerField(db_column='caseNumber', default=0)),
            ],
            options={
                'db_table': 'AccountInformation',
            },
        ),
        migrations.CreateModel(
            name='Authority',
            fields=[
                ('authorityNo', models.AutoField(db_column='authorityNo', primary_key=True, serialize=False)),
                ('authorityValue', models.CharField(db_column='authorityValue', max_length=20)),
            ],
            options={
                'db_table': 'Authority',
            },
        ),
        migrations.CreateModel(
            name='CaseData',
            fields=[
                ('caseId', models.AutoField(db_column='caseId', primary_key=True, serialize=False)),
                ('caseName', models.CharField(db_column='caseName', default='未命名', max_length=50)),
                ('caseCreateDate', models.DateField(db_column='caseCreateDate', default=django.utils.timezone.now)),
                ('cityNumber', models.IntegerField(db_column='cityNumber')),
                ('roadNumber', models.IntegerField(db_column='roadNumber')),
                ('initTotal', models.BigIntegerField(db_column='initTotal')),
                ('initTotalInfected', models.BigIntegerField(db_column='initTotalInfected')),
            ],
            options={
                'db_table': 'CaseData',
            },
        ),
        migrations.CreateModel(
            name='CaseMode',
            fields=[
                ('modeNo', models.AutoField(db_column='modeNo', primary_key=True, serialize=False)),
                ('modeValue', models.CharField(db_column='modeValue', max_length=20)),
            ],
            options={
                'db_table': 'CaseMode',
            },
        ),
        migrations.CreateModel(
            name='InitCityData',
            fields=[
                ('cityId', models.AutoField(db_column='cityId', primary_key=True, serialize=False)),
                ('cityName', models.CharField(db_column='cityName', max_length=50)),
                ('initPop', models.BigIntegerField(db_column='initPop', default=0)),
                ('initInfect', models.BigIntegerField(db_column='initInfect', default=0)),
                ('caseId', models.ForeignKey(db_column='caseId', on_delete=django.db.models.deletion.CASCADE, to='backend.CaseData')),
            ],
            options={
                'db_table': 'InitCityData',
            },
        ),
        migrations.CreateModel(
            name='CityPosition',
            fields=[
                ('cityId', models.OneToOneField(db_column='cityId', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='backend.InitCityData')),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
            ],
            options={
                'db_table': 'CityPosition',
            },
        ),
        migrations.CreateModel(
            name='LoginData',
            fields=[
                ('userId', models.OneToOneField(db_column='userId', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='backend.AccountInformation')),
                ('userPassword', models.CharField(db_column='userPassword', max_length=32)),
                ('salt', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'LoginData',
            },
        ),
        migrations.CreateModel(
            name='PersonalProfile',
            fields=[
                ('userId', models.OneToOneField(db_column='userId', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='backend.AccountInformation')),
                ('avatar', models.ImageField(default='defaultFiles/defaultAvatar.png', upload_to='avatar', verbose_name='头像')),
                ('userName', models.CharField(db_column='userName', max_length=50)),
                ('phoneNumber', models.CharField(db_column='phoneNumber', max_length=11)),
                ('sex', models.CharField(default='保密', max_length=10)),
                ('address', models.CharField(default='保密', max_length=200)),
                ('email', models.CharField(db_column='Email', default='保密', max_length=50)),
                ('birth', models.DateField(default=datetime.date(1900, 1, 1))),
            ],
            options={
                'db_table': 'PersonalProfile',
            },
        ),
        migrations.CreateModel(
            name='InitRoadData',
            fields=[
                ('roadId', models.AutoField(db_column='roadId', primary_key=True, serialize=False)),
                ('departure', models.CharField(max_length=50)),
                ('destination', models.CharField(max_length=50)),
                ('volume', models.BigIntegerField()),
                ('caseId', models.ForeignKey(db_column='caseId', on_delete=django.db.models.deletion.CASCADE, to='backend.CaseData')),
            ],
            options={
                'db_table': 'InitRoadData',
            },
        ),
        migrations.CreateModel(
            name='DailyForecastData',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
                ('population', models.BigIntegerField()),
                ('infected', models.BigIntegerField()),
                ('cityId', models.ForeignKey(db_column='cityId', on_delete=django.db.models.deletion.CASCADE, to='backend.InitCityData')),
            ],
            options={
                'db_table': 'DailyForecastData',
            },
        ),
        migrations.AddField(
            model_name='casedata',
            name='caseMode',
            field=models.ForeignKey(db_column='caseMode', on_delete=django.db.models.deletion.CASCADE, to='backend.CaseMode'),
        ),
        migrations.AddField(
            model_name='casedata',
            name='userId',
            field=models.ForeignKey(db_column='userId', on_delete=django.db.models.deletion.CASCADE, to='backend.AccountInformation'),
        ),
        migrations.AddField(
            model_name='accountinformation',
            name='authority',
            field=models.ForeignKey(db_column='authority', default='1', on_delete=django.db.models.deletion.CASCADE, to='backend.Authority'),
        ),
    ]