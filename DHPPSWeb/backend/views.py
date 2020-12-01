from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from backend import filters
from rest_framework.filters import OrderingFilter
from backend import paginations
from django.shortcuts import render, get_object_or_404
from django.views import View
from backend import models
from backend import customSerializers
from django.http import HttpResponseForbidden, JsonResponse
from backend.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.utils import timezone
from django.core import serializers, paginator
import hashlib
import logging
import json
from django.db.models.signals import pre_delete
from django.forms.models import model_to_dict
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
import datetime
import secrets
# Create your views here.

logger = logging.getLogger("django")

'''
@receiver(pre_delete, sender=models.Personalprofile)
def handle_camera_deleted(instance: models.Personalprofile, **_):
    instance.file.delete(save=False)
'''


# 返回渲染主页，其后由前端负责跳转逻辑
def index(request):
    """
    render index page
    :param request: request object
    :return: page
    """
    return render(request, 'index.html')


# 对传入的密码和salt进行md5加密，返回得到的加密密码
def hash_pwd(pwd, salt):
    h = hashlib.md5()
    pwd = pwd + salt
    h.update(pwd.encode())
    return h.hexdigest()


# json序列化时对datetime处理的函数
class DateEnconding(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime('%Y/%m/%d')


# 登录检测装饰器
def login_required(view_func):
    # 登录判断装饰器
    def wrapper(request, *view_args, **view_kwargs):
        if request.COOKIES.get("userId", None):
            userId = request.COOKIES.get("userId", None)
            print('get cookie [{}]'.format(userId))
        # 判断用户是否登录,session验证
        if request.session.get("isLogin", None):
            userId = request.session.get("userId", None)
            print('get session userId is [{}]'.format(userId))
            return view_func(request, *view_args, **view_kwargs)
        else:
            # 用户未登录,返回信息
            return JsonResponse({"message": "还未登录", "status": 404})
    return wrapper


# 登录函数视图
# 从参数获取phonenum和password，取出对应salt加密，并判断是否和存储加密密码相同
# 登录成功，返回消息和200状态码
# 登录失败，返回消息和404状态码
def signin(request):
    # 若已经登录，直接进入已登录账号
    if request.session.get('isLogin', None):
        return JsonResponse({"message": "你已经登录", "status": 404})
    elif request.method == "POST":
        # 从参数获取phonenum和password
        phonenum = request.POST.get('phonenum', None)
        password = request.POST.get('password', None)
        if phonenum and password:
            phonenum = phonenum.strip()
            try:
                # 从数据库获取phonenum和对应userid，取出salt
                # 获取失败则捕捉错误
                profile = models.Personalprofile.objects.filter(phonenumber=int(phonenum))
                if not profile.exists():
                    return JsonResponse({"message": "该账号不存在", "status": 404})
                profile = profile.first()
                accountInfo = models.Accountinformation.objects.get(userid=profile.userid.userid)

                # 判断是否和存储加密密码相同
                if (accountInfo.logindata.userpassword == hash_pwd(pwd=password, salt=accountInfo.logindata.salt)):
                    # 若相同，设置登录状态为True，设置登录id为userid，登录权限为对应权限
                    request.session['isLogin'] = True
                    request.session['userId'] = accountInfo.userid
                    request.session['userAuthority'] = accountInfo.authority
                    print(request.session.get('userId', None))
                    response = JsonResponse({"message": "登录成功", "status": 200})
                    response.set_cookie('userId', accountInfo.userid)
                    return response
                else:
                    return JsonResponse({"message": "密码错误", "status": 404})
            except Exception as e:
                print('str(Exception):\t', str(Exception))
                print('str(e):\t\t', str(e))
                print('repr(e):\t', repr(e))
                print('e.message:\t', e.message)
                print('########################################################')
                return JsonResponse({"message": "数据库错误", "status": 404})
        else:
            return JsonResponse({"message": "填写内容不能为空", "status": 404})


# 登出函数视图
# 从缓存获取对应session
# 登出成功，返回消息和200状态码
# 登出失败，返沪消息和404状态码
def logout(request):
    message = "登出成功"
    status = 200
    if not request.session.get('isLogin', None):
        # 如果本来就未登录，也就没有登出一说
        return JsonResponse({"message": "未登录，无法登出", "status": 404})
    else:
        request.session.flush()
        # del request.session['isLogin']
        # del request.session['userid']
        # del request.session['username']
        response = JsonResponse({"message": message, "status": status})
        response.delete_cookie("userId")
        return response


# 注册函数视图
# 从参数获取username，phonenum,email,password,verifyCode
# 登出成功，返回消息和200状态码
# 登出失败，返回消息和404状态码
def signup(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。
        message = "登录状态，无法注册"
        status = 404
    elif request.method == "POST":
        username = request.POST.get('username', None)
        phonenum = request.POST.get('phonenum', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        verifyCode = request.POST.get('verifyCode', None)
        print({
            "username": username,
            'phonenum': phonenum,
            'email': email,
            "password": password,
            'verifyCode': verifyCode
        })
        message = "请检查填写的内容！"
        status = 404
        if username and phonenum and email and password and verifyCode:  # 获取数据
            same_name_user = models.Personalprofile.objects.filter(username=username)
            if same_name_user:  # 用户名唯一
                message = '用户已经存在，请重新输入用户名！'
                status = 404
            else:
                same_phone_user = models.Personalprofile.objects.filter(phonenumber=phonenum)
                if same_phone_user:  # 手机号码唯一
                    message = '该手机号码已被注册，请使用别的手机号码！'
                    status = 404
                else:
                    # 当一切都OK的情况下，创建新用户
                    try:
                        newAccountInfo = models.Accountinformation.objects.create(
                            themeno=models.Theme.objects.filter(themeno=1).first(),
                            createdate=timezone.now()
                        )

                        salt = secrets.token_hex(4)
                        encryPassword = hash_pwd(pwd=password, salt=salt)
                        newLoginData = models.Logindata.objects.create(
                            userid=newAccountInfo,
                            userpassword=encryPassword,
                            salt=salt
                        )
                        newUser = models.Personalprofile.objects.create(
                            userid=newAccountInfo,
                            username=username,
                            phonenumber=phonenum,
                            email=email
                        )
                        logger.info(json.dumps(newLoginData, cls=DateEnconding))
                        logger.info(json.dumps(newUser, cls=DateEnconding))
                        message = "注册成功"
                        status = 200
                    except Exception as e:
                        print('str(Exception):\t', str(Exception))
                        print('str(e):\t\t', str(e))
                        print('repr(e):\t', repr(e))
                        print('e.message:\t', e.message)
                        print('########################################################')
                        message = "注册失败"
                        status = 404
    return JsonResponse({"message": message, "status": status})


# 修改密码函数视图
# 从参数获取原密码和userid
# 根据userid查找对应用户的logindata的密码
# 比对通过后，生成新的salt和密码，存入数据库
# 修改成功，返回消息和200状态码
# 修改失败，返回消息和404状态码
def changePwd(request):
    '''
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录", "status": 404})
    el
    '''
    if request.method == "POST":
        # 从参数获取oldPassword和password
        oldPassword = request.POST.get('oldPassword', None)
        newPassword = request.POST.get('newPassword', None)
        if oldPassword and newPassword:
            userId = request.session.get('userId', None)

            account = models.Accountinformation.objects.filter(userid=userId)
            if not account.exists():
                return JsonResponse({"message": "当前账号与浏览器记录不一致", "status": 404})
            account = account.first()
            # 检测账号原密码是否符合
            if (account.logindata.userpassword == hash_pwd(pwd=oldPassword, salt=account.logindata.salt)):
                newSalt = secrets.token_hex(4)
                encryPassword = hash_pwd(pwd=newPassword, salt=newSalt)
                models.Logindata.objects.filter(userid=userId).update(userpassword=encryPassword, salt=newSalt)
                return JsonResponse({"message": "修改成功", "status": 200})
    else:
        return JsonResponse({"message": "参数传递方式有误", "status": 404})


# 忘记密码函数视图
# 从参数获取电话号码以及验证码，密码
# 验证码比对通过后，生成新的salt和密码，存入数据库
# 修改成功，返回消息和200状态码
# 修改失败，返回消息和404状态码
def forgetPwd(request):
    if request.session.get('isLogin', None):
        return JsonResponse({"message": "你已经登录，忘记密码需先退出", "status": 404})
    elif request.method == "POST":
        # 从参数获取phonenum和password
        phonenum = request.POST.get('phonenum', None)
        verifyCode = request.POST.get('verifyCode', None)
        newPassword = request.POST.get('newPassword', None)
        if phonenum and verifyCode and newPassword:
            # 从数据库获取phonenum和对应userid，取出salt
            # 获取失败则捕捉错误
            profile = models.Personalprofile.objects.filter(phonenumber=int(phonenum))
            if not profile.exists():
                return JsonResponse({"message": "该手机未注册", "status": 404})
            profile = profile.first()
            account = models.Accountinformation.objects.get(userid=profile.userid.userid)

            # 缺少逻辑：检测短信验证码是否正确

            newSalt = secrets.token_hex(4)
            encryPassword = hash_pwd(pwd=newPassword, salt=newSalt)
            models.Logindata.objects.filter(userid=account.userid).update(userpassword=encryPassword, salt=newSalt)
            return JsonResponse({"message": "修改成功", "status": 200})
    else:
        return JsonResponse({"message": "参数传递方式有误", "status": 404})


# 存储前端发回的案例参数视图
# 获取表单数据
# 解析表单数据生成对应models存入
# 保存成功，返回消息和200状态码
# 保存失败，返回消息和404状态码
def saveCase(request):
    '''
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录，保存案例需要先登录", "status": 404})
    el
    '''
    if request.method == "POST":
        userId = request.POST.get('userid', None)
        caseName = request.POST.get('casename', None)
        cityNum = request.POST.get('citynum', None)
        roadNum = request.POST.get('roadnum', None)
        initcitydata = request.POST.get('Initcitydata', None)
        initroaddata = request.POST.get('Initroaddata', None)
        cityposition = request.POST.get('Cityposition', None)
        if not(userId and caseName and cityNum and roadNum and initcitydata and initroaddata and cityposition):
            return JsonResponse({"message": "表单未填写完整", "status": 404})
        # 案例计数：初始人口与初始感染人口
        initTotalNum = 0
        initTotalInfectedNum = 0
        initcitydataList = initcitydata.split(",")
        initroaddataList = initroaddata.split(",")
        citypositionList = cityposition.split(",")

        cityCount = 0
        for cityInfo in initcitydataList:
            value = cityInfo.split(":")
            if cityCount % 3 == 1:
                initpop = int(value)
                initTotalNum += initpop
            elif cityCount % 3 == 2:
                initinfect = int(value)
                initTotalInfectedNum += initinfect
            cityCount += 1
        message = "开始进行案例保存"
        status = 200
        newCaseId = 0
        try:
            # 新增案例
            newCase = models.Casedata.objects.create(
                userid=userId,
                casename=caseName,
                citynumber=int(cityNum),
                roadnumber=int(roadNum),
                inittotal=initTotalNum,
                inittotalinfected=initTotalInfectedNum
            )
            # 新增城市信息
            cityCount = 0
            cityname = ""
            initpop = ""
            initinfect = ""
            x = 0.0
            y = 0.0
            for cityInfo in initcitydataList:
                value = cityInfo.split(":")
                posValue = citypositionList[cityCount].split(":")
                if cityCount % 3 == 0:
                    cityname = value
                elif cityCount % 3 == 1:
                    initpop = int(value)
                    x = float(posValue)
                elif cityCount % 3 == 2:
                    initinfect = int(value)
                    y = float(posValue)
                    newCity = models.Initcitydata.objects.create(
                        caseid=newCase.caseid,
                        cityname=cityname,
                        initpop=initpop,
                        initinfect=initinfect
                    )
                    models.Cityposition.objects.create(
                        cityid=newCity.cityid,
                        x=x,
                        y=y
                    )
                cityCount += 1

            # 新增道路信息
            roadCount = 0
            for roadInfo in initroaddataList:
                value = roadInfo.split(":")
                if roadCount % 3 == 0:
                    departure = value
                elif roadCount % 3 == 1:
                    destination = value
                elif roadCount % 3 == 2:
                    volume = float(value)
                    models.Initroaddata.objects.create(
                        caseid=newCase.caseid,
                        departure=departure,
                        destination=destination,
                        volume=volume
                    )
                roadCount += 1
            message = "保存案例成功"
            status = 200
            newCaseId = newCase.caseid
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            print('e.message:\t', e.message)
            print('########################################################')
            message = "注册失败"
            status = 404
        return JsonResponse({"message": message, "status": status, "caseId": newCaseId})


# 解析前端发回数据并送入模型进行模拟，取得返回数据并输出
def startSimulate(request):
    if request.method == "POST":
        userId = request.POST.get('userid', None)
        caseName = request.POST.get('casename', None)
        initcitydataList = request.POST.get('Initcitydata', None)
        initroaddataList = request.POST.get('Initroaddata', None)
        citypositionList = request.POST.get('Cityposition', None)

        if not(userId and caseName and initcitydataList and initroaddataList and citypositionList):
            return JsonResponse({"message": "表单未填写完整", "status": 404})
        cityNum = len(initcitydataList)
        roadNum = len(initroaddataList)
        # 案例计数：初始人口与初始感染人口
        initTotalNum = 0
        initTotalInfectedNum = 0
        for cityInfo in initcitydataList:
            initTotalNum += cityInfo["initpop"]
            initTotalInfectedNum += cityInfo["initinfect"]
        message = "开始进行案例保存"
        status = 200
        newCaseId = 0


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
        return JsonResponse(image, content_type='image/png')

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
        return JsonResponse({"message": message, "status": status})


def GetUserInfos(request):
    if request.method == "GET":
        pageSize = request.GET.get("pageSize")
        page = request.GET.get("page")
        accountInfos = models.Accountinformation.objects.select_related("personalprofile").all().order_by('userid')
        accountPaginator = paginator.Paginator(accountInfos, pageSize)
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
        return JsonResponse({
            'data': jsonRes,
            'pagination': accountPaginator.count,
            'pageSize': accountPaginator.per_page,
            'page': pageInfos.start_index() // accountPaginator.per_page + 1
        })


def GetGeneralUserInfos(request):
    if request.method == "GET":
        pageSize = request.GET.get("pageSize")
        page = request.GET.get("page")
        generalUserInfos = models.Accountinformation.objects.select_related("personalprofile").filter(authority="普通用户").order_by('userid')
        accountPaginator = paginator.Paginator(generalUserInfos, pageSize)
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
        return JsonResponse({
            'data': jsonRes,
            'pagination': accountPaginator.count,
            'pageSize': accountPaginator.per_page,
            'page': pageInfos.start_index() // accountPaginator.per_page + 1
        })


def GetAdminInfos(request):
    if request.method == "GET":
        pageSize = request.GET.get("pageSize")
        page = request.GET.get("page")
        adminUserInfos = models.Accountinformation.objects.select_related("personalprofile").filter(authority="管理员").order_by('userid')
        accountPaginator = paginator.Paginator(adminUserInfos, pageSize)
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
        return JsonResponse({
            'data': jsonRes,
            'pagination': accountPaginator.count,
            'pageSize': accountPaginator.per_page,
            'page': pageInfos.start_index() // accountPaginator.per_page + 1
        })


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
    authentication_classes = [SessionAuthentication]
    queryset = models.Theme.objects.all()
    serializer_class = customSerializers.ThemeSerializer
