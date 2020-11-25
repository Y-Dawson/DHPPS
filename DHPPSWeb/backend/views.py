from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from backend import filters
from rest_framework.filters import OrderingFilter
from backend import paginations
from django.shortcuts import render, get_object_or_404
from django.views import View
from backend import models
from backend import customSerializers
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from backend.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.utils import timezone
from django.core import serializers, paginator
import hashlib
import logging
import json
from django.db.models.signals import pre_delete
from django.forms.models import model_to_dict
import datetime

# Create your views here.

logger = logging.getLogger("django")

'''
@receiver(pre_delete, sender=models.Personalprofile)
def handle_camera_deleted(instance: models.Personalprofile, **_):
    instance.file.delete(save=False)
'''


def index(request):
    """
    render index page
    :param request: request object
    :return: page
    """
    return render(request, 'index.html')


def hash_pwd(pwd, salt):
    h = hashlib.md5()
    pwd = pwd + salt
    h.update(pwd.encode())
    return h.hexdigest()


class DateEnconding(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime('%Y/%m/%d')


def signin(request):
    if request.session.get('is_login', None):
        return HttpResponse({"data": {"message": "你已经登录", "status": 404}, "content-type": "application/json"})
    elif request.method == "POST":
        phonenum = request.POST.get('phonenum', None)
        password = request.POST.get('password', None)
        message = "填写内容不能为空"
        status = 404
        if phonenum and password:
            phonenum = phonenum.strip()
            try:
                profile = models.Personalprofile.get(phonenumber=phonenum)
                logindata = models.Logindata.get(userid=profile.userid)
                if (logindata.password == hash_pwd(pwd=password, salt=logindata.salt)):
                    request.session['is_login'] = True
                    request.session['user_id'] = profile.userid
                    request.session['user_name'] = profile.phonenumber
                    message = "登录成功"
                    status = 200
                else:
                    message = "密码错误"
                    status = 404
            except Exception as identifier:
                print("捕获异常：", identifier)
                message = "该电话未注册"
                status = 404
        return HttpResponse({"data": {"message": message, "status": status}, "content-type": "application/json"})


def logout(request):
    message = "登出成功"
    status = 200
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        message = "未登录，无法登出"
        status = 404
    request.session.flush()
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return HttpResponse({"data": {"message": message, "status": status}, "content-type": "application/json"})


def signup(request):
    message = "注册成功"
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        message = "登录状态，无法注册"
        status = 404
    elif request.method == "POST":
        username = request.POST.get('username', None)
        phonenum = request.POST.get('phonenum', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        verifyCode = request.POST.get('verifyCode', None)
        message = "请检查填写的内容！"
        status = 404
        if username and phonenum and email and password and password2 and verifyCode:  # 获取数据
            if password != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                status = 404
            else:
                same_name_user = models.Personalprofile.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    status = 404

                same_phone_user = models.Personalprofile.objects.filter(phonenumber=phonenum)
                if same_phone_user:  # 手机号码唯一
                    message = '该手机号码已被注册，请使用别的手机号码！'
                    status = 404
                # 当一切都OK的情况下，创建新用户
                try:
                    newAccountInfo = models.Accountinformation.objects.create(themeno=1,
                                                                              createdate=timezone.now(),)
                    newUser = models.Personalprofile.objects.create(userid=newAccountInfo.userid,
                                                                    username=username,
                                                                    phonenumber=phonenum,
                                                                    email=email)
                    logger.info(serializers.serialize("json", newUser))
                    message = "注册成功"
                    status = 200
                except Exception:
                    message = "注册失败"
                    status = 404
    return HttpResponse({"data": {"message": message, "status": status}, "content-type": "application/json"})


class ImageCodeView(View):
    def get(self, request):
        # 1.接受uuid
        uuid = request.GET.get('uuid')
        # 2.验证uuid
        if not uuid:
            return HttpResponseForbidden('uuid无效')
        # 3.生成图片的文本、数据
        code, image = captcha.generate_captcha()
        try:
            # 4.连接到redis
            redisClient = get_redis_connection('image_code')
            # 5.生成redis管道
            pipeline = redisClient.pipeline()
            # 6.保存图片文本，用于后续与用户输入值对比，设置过期时间
            pipeline.setex(uuid, 180, code)
            # 7.传递指令
            pipeline.execute()
        except Exception:
            pass
        # 8.后台显示验证码信息
        logger.info('verify_text:{}'.format(code))
        # 9.响应：输出图片数据
        return HttpResponse(image, content_type='image/png')

    def post(self, request):
        # 1.接受uuid
        uuid = request.POST.get('uuid')
        inputCode = request.POST.get('code')
        # 2.验证uuid
        if not uuid:
            return HttpResponseForbidden('uuid无效')
        message = "表单值不合法"
        status = 404
        try:
            # 3.连接到redis
            redisClient = get_redis_connection('image_code')
            # 4.生成redis管道
            pipeline = redisClient.pipeline()
            # 5.获得验证码
            code = pipeline.setex.get('uuid')
            # 6.比较验证码
            message
            if inputCode == code:
                message = "验证码正确"
                status = 200
            else:
                message = "验证码错误"
                status = 404
        except Exception:
            message = "没有获取到验证码"
        return HttpResponse({"data": {"message": message, "status": status}, "content-type": "application/json"})


def GetUserInfos(request):
    if request.method == "GET":
        page_size = request.GET.get("page_size")
        page = request.GET.get("page")
        accountInfos = models.Accountinformation.objects.select_related("personalprofile").all()
        accountPaginator = paginator.Paginator(accountInfos, page_size)
        if page == "":
            page = 1
        else:
            page = int(page)
        pageInfos = accountPaginator.page(page)
        jsonList = []
        for accountInfo in pageInfos:
            accountInfoDict = model_to_dict(accountInfo)
            profileDict = model_to_dict(accountInfo.personalprofile)
            jsonList.append({**accountInfoDict, **profileDict})
        jsonRes = json.loads(json.dumps(jsonList, cls=DateEnconding))
        print(jsonRes)
        return JsonResponse(jsonRes, safe=False)


def GetGeneralUserInfos(request):
    if request.method == "GET":
        page_size = request.GET.get("page_size")
        page = request.GET.get("page")
        generalUserInfos = models.Accountinformation.objects.select_related("personalprofile").filter(authority="普通用户")
        accountPaginator = paginator.Paginator(generalUserInfos, page_size)
        if page == "":
            page = 1
        else:
            page = int(page)
        pageInfos = accountPaginator.page(page)
        jsonList = []
        for accountInfo in pageInfos:
            accountInfoDict = model_to_dict(accountInfo)
            profileDict = model_to_dict(accountInfo.personalprofile)
            jsonList.append({**accountInfoDict, **profileDict})
        jsonRes = json.loads(json.dumps(jsonList, cls=DateEnconding))
        print(jsonRes)
        return JsonResponse(jsonRes, safe=False)


def GetAdminInfos(request):
    if request.method == "GET":
        page_size = request.GET.get("page_size")
        page = request.GET.get("page")
        adminUserInfos = models.Accountinformation.objects.select_related("personalprofile").filter(authority="管理员")
        accountPaginator = paginator.Paginator(adminUserInfos, page_size)
        if page == "":
            page = 1
        else:
            page = int(page)
        pageInfos = accountPaginator.page(page)
        jsonList = []
        for accountInfo in pageInfos:
            accountInfoDict = model_to_dict(accountInfo)
            profileDict = model_to_dict(accountInfo.personalprofile)
            jsonList.append({**accountInfoDict, **profileDict})
        jsonRes = json.loads(json.dumps(jsonList, cls=DateEnconding))
        print(jsonRes)
        return JsonResponse(jsonRes, safe=False)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Accountinformation.objects.all()
    serializer_class = customSerializers.AccountinformationSerializer


class CaseViewSet(viewsets.ModelViewSet):
    queryset = models.Casedata.objects.all()
    serializer_class = customSerializers.CasedataSerializer
    pagination_class = paginations.MyFormatResultsSetPagination
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filter_class = filters.CaseFilter
    ordering_fields = ('casename', 'inittotal', 'inittotalinfected', 'citynumber', 'roadnumber',)
    ordering = ('caseid',)


class CityPosViewSet(viewsets.ModelViewSet):
    queryset = models.Cityposition.objects.all()
    serializer_class = customSerializers.CitypositionSerializer


class DailyForeViewSet(viewsets.ModelViewSet):
    queryset = models.Dailyforecastdata.objects.all()
    serializer_class = customSerializers.DailyforecastdataSerializer


class InitCityViewSet(viewsets.ModelViewSet):
    queryset = models.Initcitydata.objects.all()
    serializer_class = customSerializers.InitcitydataSerializer


class InitRoadViewSet(viewsets.ModelViewSet):
    queryset = models.Initroaddata.objects.all()
    serializer_class = customSerializers.InitroaddataSerializer


class LoginViewSet(viewsets.ModelViewSet):
    queryset = models.Logindata.objects.all()
    serializer_class = customSerializers.LogindataSerializer


class ModelViewSet(viewsets.ModelViewSet):
    queryset = models.Modeldata.objects.all()
    serializer_class = customSerializers.ModeldataSerializer


class PersonalProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Personalprofile.objects.all()
    serializer_class = customSerializers.PersonalprofileSerializer


class ThemeViewSet(viewsets.ModelViewSet):
    queryset = models.Theme.objects.all()
    serializer_class = customSerializers.ThemeSerializer
