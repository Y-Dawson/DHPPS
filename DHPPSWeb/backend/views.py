from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from django.views import View
from backend import models
from backend import serializers
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from meiduo_mall.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
import hashlib
import logging
# Create your views here.

logger = logging.getLogger("django")


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


def signin(request):
    if request.session.get('is_login', None):
        return HttpResponse({"data": {"message": "你已经登录"}, "content-type": "application/json"})
    elif request.method == "POST":
        phonenum = request.POST.get('phonenum', None)
        password = request.POST.get('password', None)
        message = "填写内容不能为空"
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
                else:
                    message = "密码错误"
            except Exception as identifier:
                print("捕获异常：", identifier)
                message = "该电话未注册"
        return HttpResponse({"data": {"message": message}, "content-type": "application/json"})


class ImageCodeView(View):
    def get(self, request):
        # 1.接受uuid
        uuid = request.GET.get('uuid')
        # 2.验证uuid
        if not uuid:
            return HttpResponseForbidden('uuid无效')
        # 3.生成图片的文本、数据
        text, code, image = captcha.generate_captcha()
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
            else:
                message = "验证码错误"
        except Exception:
            message = "没有获取到验证码"
        return HttpResponse({"data": {"message": message}, "content-type": "application/json"})


def GetUserInfos(request):
    if request.method == "GET":
        accountInfos = models.Accountinformation.objects.all()
        profiles = models.Personalprofile.objects.all()
        result = accountInfos.union(profiles)
        resultJson = serializers.serialize("json", result)
        print(resultJson)
        return JsonResponse(resultJson, safe=False)


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
