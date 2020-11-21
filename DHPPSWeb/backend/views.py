from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from backend import models
from backend import serializers
from django.http import HttpResponse, redirect
from forms import UserForm
import hashlib
# Create your views here.


def hash_pwd(pwd, salt):
    h = hashlib.md5()
    pwd = pwd + salt
    h.update(pwd.encode())
    return h.hexdigest()


def index(request):
    """
    render index page
    :param request: request object
    :return: page
    """
    return render(request, 'index.html')


def signin(request):
    if request.session.get('is_login', None):
        return HttpResponse({"data": {},
                             "status": 302,
                             "statusText": "Temporary Move",
                             "headers": {
                                 "content-length": 0,
                                 "content-type": "application/json"
                                 }
                             })
    elif request.method == "GET":
        userSignInForm = UserForm()
        return HttpResponse({"data": userSignInForm.format(),
                             "status": 200,
                             "statusText": "OK",
                             "headers": {
                                 "content-length": len(str(userSignInForm)),
                                 "content-type": "application/json"
                                 }
                             })

    elif request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            phonenum = login_form.cleaned_data['phonenum']
            password = login_form.cleaned_data['password']
            try:
                profile = models.Personalprofile.get(phonenumber=phonenum)
                logindata = models.Logindata.get(userid=profile.userid)
                if (logindata.password == hash_pwd(pwd=password, salt=logindata.salt)):
                    request.session['is_login'] = True
                    request.session['user_id'] = profile.userid
                    request.session['user_name'] = profile.phonenumber
                    return redirect('/index/')
                else:
                    message = "密码错误"
            except Exception as identifier:
                print("捕获异常：", identifier)
                message = "该电话未注册"
        return HttpResponse({"data": {"message": message},
                             "status": 200,
                             "statusText": "OK",
                             "headers": {
                                 "content-length": len(str(message)),
                                 "content-type": "application/json"
                                 }
                             })
    else:
        login_form = UserForm()
        return HttpResponse({"data": {"login_form": login_form},
                             "status": 200,
                             "statusText": "OK",
                             "headers": {
                                 "content-length": len(str(login_form)),
                                 "content-type": "application/json"
                                 }
                             })


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
