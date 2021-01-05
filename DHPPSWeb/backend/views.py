from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from backend import filters
from rest_framework.filters import OrderingFilter
from backend import paginations
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.db.models import F, Avg, Max, Min, Count, Sum
from backend import models
from backend import customSerializers
from backend.sendSms import SendSms
# from backend.simulate import returnDataSimulator
from backend import returnDataSimulator
from django.http import HttpResponseForbidden, JsonResponse
from django_redis import get_redis_connection
from django.utils import timezone
from django.core import serializers, paginator
import hashlib
import logging
import json
from django.db.models.signals import pre_delete
from django.forms.models import model_to_dict
import datetime
from dateutil.relativedelta import relativedelta
import secrets
from django.utils.decorators import method_decorator
# Create your views here.

logger = logging.getLogger("django")


# 登录验证函数，通过method_decorator作为装饰器装饰给各个视图
def LoginAuthenticate(function):
    def authenticate(request, *args, **kwargs):
        if request.COOKIES.get('sessionid', None):
            if request.session.get("isLogin", None):
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({"message": "您尚未登录，请先登录", "status": 404})
        else:
            return JsonResponse({"message": "无登录信息，请先登录", "status": 404})
    return authenticate


# 管理员验证函数，通过method_decorator作为装饰器装饰给各个视图
def AdminAuthenticate(function):
    def authenticate(request, *args, **kwargs):
        if request.COOKIES.get('sessionid', None):
            authority = request.session.get("userAuthority", None)
            if authority == "管理员" or authority == "超级管理员":
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({"message": "您的权限不足，无法访问此页面", "status": 404})
        else:
            return JsonResponse({"message": "无登录信息，请先登录", "status": 404})
    return authenticate


# 超级管理员验证函数，通过method_decorator作为装饰器装饰给各个视图
def SuperAdminAuthenticate(function):
    def authenticate(request, *args, **kwargs):
        if request.COOKIES.get('sessionid', None):
            authority = request.session.get("userAuthority", None)
            if authority == "超级管理员":
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({"message": "您的权限不足，无法访问此页面", "status": 404})
        else:
            return JsonResponse({"message": "无登录信息，请先登录", "status": 404})
    return authenticate


# 返回渲染主页，其后由前端负责跳转逻辑
def Index(request):
    """
    render Index page
    :param request: request object
    :return: page
    """
    return render(request, './dist/index.html')


def HomePage(request):
    '''
    render homepage page
    :param request: request object
    :return: homepage
    '''
    return render(request, './template/index.html')


def ModelPage(request):
    '''
    render Index page
    :param request: request object
    :return: homepage
    '''
    return render(request, './template/model.html')


# 对传入的密码和salt进行md5加密，返回得到的加密密码
def HashPwd(pwd, salt):
    h = hashlib.md5()
    pwd = pwd + salt
    h.update(pwd.encode())
    return h.hexdigest()


# json序列化时对datetime处理的函数
class DateEnconding(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime('%Y/%m/%d')


# 身份信息获取函数
# 从参数获取phoneNum和password，取出对应salt加密，并判断是否和存储加密密码相同
# 登录成功，返回消息和200状态码
# 登录失败，返回消息和404状态码
def GetIdentity(request):
    if not request.session.get('isLogin', None):
        # 如果本来就未登录，也就没有登出一说
        return JsonResponse({"message": "未登录", "status": 404})
    else:
        if request.method == "POST":
            userId = request.session.get('userId', None)
            authority = request.session.get('userAuthority', None)

            return JsonResponse({
                "userId": userId,
                "authority": authority,
                "message": "返回数据成功",
                "status": 200})
        else:
            return JsonResponse({
                "message": "请求方法无效",
                "status": 404})


# 登录函数视图
# 从参数获取phoneNum和password，取出对应salt加密，并判断是否和存储加密密码相同
# 登录成功，返回消息和200状态码
# 登录失败，返回消息和404状态码
def Signin(request):
    # 若已经登录，直接进入已登录账号
    if request.session.get('isLogin', None):
        return JsonResponse({"message": "你已经登录", "status": 404})
    elif request.method == "POST":
        # 从参数获取phoneNum和password
        phoneNum = request.POST.get('phoneNum', None)
        password = request.POST.get('password', None)
        if phoneNum and password:
            phoneNum = phoneNum.strip()
            try:
                # 从数据库获取phonenum和对应userId，取出salt
                # 获取失败则捕捉错误
                profile = models.PersonalProfile.objects.filter(phoneNumber=int(phoneNum))
                if not profile.exists():
                    return JsonResponse({"message": "该账号不存在", "status": 404})
                profile = profile.first()
                accountInfo = models.AccountInformation.objects.get(userId=profile.userId.userId)

                # 判断是否和存储加密密码相同
                if (accountInfo.logindata.userPassword == HashPwd(pwd=password, salt=accountInfo.logindata.salt)):
                    # 若相同，设置登录状态为True，设置登录id为userId，登录权限为对应权限
                    request.session['isLogin'] = True
                    request.session['userId'] = accountInfo.userId
                    request.session['userAuthority'] = accountInfo.authority
                    print(request.session.get('userId', None))
                    response = JsonResponse({
                        "message": "登录成功",
                        "status": 200,
                        "userId": accountInfo.userId,
                        "userAuthority": accountInfo.authority
                        })
                    # response["Access-Control-Allow-Credentials"] = "true"
                    # response["Access-Control-Allow-Methods"] = 'GET, POST, PATCH, PUT, OPTIONS'
                    # response["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
                    return response
                else:
                    return JsonResponse({"message": "密码错误", "status": 404})
            except Exception as e:
                print('str(Exception):\t', str(Exception))
                print('str(e):\t\t', str(e))
                print('repr(e):\t', repr(e))
                print('########################################################')
                return JsonResponse({"message": "数据库错误", "status": 404})
        else:
            return JsonResponse({"message": "填写内容不能为空", "status": 404})


# 登出函数视图
# 从redis获取对应session并删除
# 登出成功，返回消息和200状态码
# 登出失败，返回消息和404状态码
def Logout(request):
    if not request.session.get('isLogin', None):
        # 如果本来就未登录，也就没有登出一说
        return JsonResponse({"message": "未登录，无法登出", "status": 404})
    else:
        request.session.flush()
        # del request.session['isLogin']
        # del request.session['userId']
        # del request.session['userName']
        response = JsonResponse({"message": "登出成功", "status": 200})
        return response


# 请求短信验证码函数视图
# 通过阿里云短信服务发送验证码，并保存验证码到redis缓存
# 发送成功，返回消息和200状态码
# 发送失败，返回消息和404状态码
def RequestSmsCode(request):
    if request.method == "POST":
        phoneNum = request.POST.get('phoneNum', None)
        requestType = request.POST.get('requestType', None)
        if phoneNum is None:
            return JsonResponse({"message": "电话号码不能为空", "status": 404})
        if requestType is None:
            return JsonResponse({"message": "请求类型不能为空", "status": 404})

        samePhoneUser = models.PersonalProfile.objects.filter(phoneNumber=phoneNum)
        if samePhoneUser:  # 手机号码已存在
            if requestType == "signUp":
                return JsonResponse({"message": "该手机号码已被注册，请使用别的手机号码！", "status": 404})
        else:
            if requestType == "forgetPwd":
                return JsonResponse({"message": "该手机号码尚未注册！", "status": 404})

        redisClient = get_redis_connection('smsCode')
        if (redisClient.get(phoneNum+"Flag") is not None):
            return JsonResponse({"message": "冷却中，请60秒后重新申请", "status": 404})
        code, message, result = SendSms(phoneNum)
        print(phoneNum, "result is", message)
        if str(result) == "OK":
            try:
                # 4.连接到redis
                redisClient = get_redis_connection('smsCode')
                # 5.生成redis管道
                # pipeline = redisClient.pipeline()
                # 6.保存验证码，用于后续与用户输入值对比，设置过期时间
                redisClient.setex(phoneNum, 300, code)
                redisClient.setex(phoneNum+"Flag", 60, 1)
                # 7.传递指令
                # pipeline.execute()
            except Exception:
                return JsonResponse({"message": "保存到redis失败", "status": 404})
        else:
            return JsonResponse({"message": "验证码发送失败", "status": 404})
        return JsonResponse({"message": "验证码已发送", "status": 200})


# 注册函数视图
# 从参数获取userName，phonenum,email,password,verifyCode
# 验证判断其合法性，并创建对应数据存入数据库
# 注册成功，返回消息和200状态码
# 注册失败，返回消息和404状态码
def Signup(request):
    if request.session.get('isLogin', None):
        # 登录状态不允许注册。
        message = "登录状态，无法注册"
        status = 404
    elif request.method == "POST":
        userName = request.POST.get('userName', None)
        phoneNum = request.POST.get('phoneNum', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        verifyCode = request.POST.get('verifyCode', None)
        print({
            "userName": userName,
            'phoneNum': phoneNum,
            'email': email,
            "password": password,
            'verifyCode': verifyCode
        })
        message = "请检查填写的内容！"
        status = 404

        redisClient = get_redis_connection('smsCode')
        verifyCodeInCache = redisClient.get(phoneNum)
        print(verifyCodeInCache)
        if verifyCodeInCache is None:
            return JsonResponse({"message": "尚未申请短信验证码", "status": 404})
        verifyCodeInCache = verifyCodeInCache.decode('ascii')

        if userName and phoneNum and email and password and verifyCode:  # 获取数据
            if verifyCodeInCache != verifyCode:
                return JsonResponse({"message": "短信验证码错误，请检查重试", "status": 404})

            sameNameUser = models.PersonalProfile.objects.filter(userName=userName)
            if sameNameUser:  # 用户名唯一
                return JsonResponse({"message": "用户已经存在，请重新输入用户名！", "status": 404})

            samePhoneUser = models.PersonalProfile.objects.filter(phoneNumber=phoneNum)
            if samePhoneUser:  # 手机号码唯一
                return JsonResponse({"message": "该手机号码已被注册，请使用别的手机号码！", "status": 404})

            # 当一切都OK的情况下，创建新用户
            try:
                newAccountInfo = models.AccountInformation.objects.create(
                    themeNo=models.Theme.objects.filter(themeNo=1).first()
                )

                salt = secrets.token_hex(4)
                encryPassword = HashPwd(pwd=password, salt=salt)
                newLoginData = models.LoginData.objects.create(
                    userId=newAccountInfo,
                    userPassword=encryPassword,
                    salt=salt
                )
                newUser = models.PersonalProfile.objects.create(
                    userId=newAccountInfo,
                    userName=userName,
                    phoneNumber=phoneNum,
                    email=email
                )
                logger.info(json.dumps(newLoginData, cls=DateEnconding))
                logger.info(json.dumps(newUser, cls=DateEnconding))
                redisClient.delete(phoneNum)
                redisClient.delete(phoneNum+"Flag")
                message = "注册成功"
                status = 200
            except Exception as e:
                print('str(Exception):\t', str(Exception))
                print('str(e):\t\t', str(e))
                print('repr(e):\t', repr(e))
                print('########################################################')
                message = "注册失败"
                status = 404
    return JsonResponse({"message": message, "status": status})


# 修改密码函数视图
# 从参数获取原密码和userId
# 根据userId查找对应用户的LoginData的密码
# 比对通过后，生成新的salt和密码，存入数据库
# 修改成功，返回消息和200状态码
# 修改失败，返回消息和404状态码
def ChangePwd(request):
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录", "status": 404})
    elif request.method == "POST":
        # 从参数获取oldPassword和password
        userId = request.session.get("userId", None)
        oldPassword = request.POST.get('oldPassword', None)
        newPassword = request.POST.get('newPassword', None)
        if userId and oldPassword and newPassword:
            account = models.AccountInformation.objects.filter(userId=userId)
            if not account.exists():
                return JsonResponse({"message": "当前账号与浏览器记录不一致", "status": 404})
            account = account.first()
            # 检测账号原密码是否符合
            if (account.logindata.userPassword == HashPwd(pwd=oldPassword, salt=account.logindata.salt)):
                newSalt = secrets.token_hex(4)
                encryPassword = HashPwd(pwd=newPassword, salt=newSalt)
                models.LoginData.objects.filter(userId=userId).update(userPassword=encryPassword, salt=newSalt)
                return JsonResponse({"message": "修改成功", "status": 200})
            else:
                return JsonResponse({"message": "账号原密码错误", "status": 404})
    else:
        return JsonResponse({"message": "参数传递方式有误", "status": 404})


# 忘记密码函数视图
# 从参数获取电话号码以及验证码，密码
# 验证码比对通过后，生成新的salt和密码，存入数据库
# 修改成功，返回消息和200状态码
# 修改失败，返回消息和404状态码
def ForgetPwd(request):
    if request.session.get('isLogin', None):
        return JsonResponse({"message": "你已经登录，忘记密码需先退出", "status": 404})
    elif request.method == "POST":
        # 从参数获取phoneNum和password
        phoneNum = request.POST.get('phoneNum', None)
        verifyCode = request.POST.get('verifyCode', None)
        newPassword = request.POST.get('newPassword', None)

        print({
            'phoneNum': phoneNum,
            "newPassword": newPassword,
            'verifyCode': verifyCode
        })
        redisClient = get_redis_connection('smsCode')
        print(phoneNum)
        verifyCodeInCache = redisClient.get(phoneNum)
        print(verifyCodeInCache)
        if verifyCodeInCache is None:
            return JsonResponse({"message": "尚未申请短信验证码", "status": 404})
        verifyCodeInCache = verifyCodeInCache.decode('ascii')

        if phoneNum and verifyCode and newPassword:
            # 从数据库获取phonenum和对应userId，取出salt
            # 获取失败则捕捉错误
            if verifyCode and verifyCodeInCache != verifyCode:
                return JsonResponse({"message": "短信验证码错误，请检查重试", "status": 404})

            profile = models.PersonalProfile.objects.filter(phoneNumber=int(phoneNum))
            if not profile.exists():
                return JsonResponse({"message": "该手机未注册", "status": 404})
            profile = profile.first()
            account = models.AccountInformation.objects.get(userId=profile.userId.userId)

            # 缺少逻辑：检测短信验证码是否正确
            newSalt = secrets.token_hex(4)
            encryPassword = HashPwd(pwd=newPassword, salt=newSalt)
            models.LoginData.objects.filter(userId=account.userId).update(userPassword=encryPassword, salt=newSalt)
            redisClient.delete(phoneNum)
            redisClient.delete(phoneNum+"Flag")
            return JsonResponse({"message": "修改成功", "status": 200})
    else:
        return JsonResponse({"message": "参数传递方式有误", "status": 404})


# 存储前端发回的案例参数视图
# 获取表单数据
# 解析表单数据生成对应models存入
# 保存成功，返回消息和200状态码
# 保存失败，返回消息和404状态码
def SaveCase(request):
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录，保存案例需要先登录", "status": 404})
    elif request.method == "POST":
        userId = request.POST.get('userId', None)
        caseName = request.POST.get('caseName', None)
        cityNum = request.POST.get('citynum', None)
        roadNum = request.POST.get('roadnum', None)
        caseMode = request.POST.get('caseMode', None)
        InitCityData = request.POST.get('InitCityData', None)
        InitRoadData = request.POST.get('InitRoadData', None)
        # 若获取到InitRoadData为"NULL"，代表无道路
        CityPosition = request.POST.get('CityPosition', None)
        if not(userId and caseName and cityNum and roadNum and InitCityData and InitRoadData and CityPosition):
            return JsonResponse({"message": "表单未填写完整", "status": 404})
        # 案例计数：初始人口与初始感染人口

        if (caseMode == "自定模式"):
            initTotalNum = 0
            initTotalInfectedNum = 0
            initCityDataList = InitCityData.split(",")
            if InitRoadData != "NULL":
                initRoadDataList = InitRoadData.split(",")
            citypositionList = CityPosition.split(",")

            cityCount = 0
            for cityInfo in initCityDataList:
                value = cityInfo.split(":")[1]
                if cityCount % 3 == 1:
                    initPop = int(value)
                    initTotalNum += initPop
                elif cityCount % 3 == 2:
                    initInfect = int(value)
                    initTotalInfectedNum += initInfect
                cityCount += 1

            try:
                # 新增案例
                if (models.AccountInformation.objects.filter(userId=userId).exists()):
                    newCase = models.CaseData.objects.create(
                        userId=models.AccountInformation.objects.filter(userId=userId).first(),
                        caseName=caseName,
                        caseMode=caseMode,
                        cityNumber=int(cityNum),
                        roadNumber=int(roadNum),
                        initTotal=initTotalNum,
                        initTotalInfected=initTotalInfectedNum
                    )
                else:
                    return JsonResponse({"message": "目标用户不存在", "status": 404})
                # 新增城市信息
                cityCount = 0
                cityName = ""
                initPop = ""
                initInfect = ""
                x = 0.0
                y = 0.0
                for cityInfo in initCityDataList:
                    value = cityInfo.split(":")[1]
                    posValue = citypositionList[cityCount].split(":")[1]
                    if cityCount % 3 == 0:
                        cityName = value
                    elif cityCount % 3 == 1:
                        initPop = int(value)
                        x = float(posValue)
                    elif cityCount % 3 == 2:
                        initInfect = int(value)
                        y = float(posValue)
                        newCity = models.InitCityData.objects.create(
                            caseId=newCase,
                            cityName=cityName,
                            initPop=initPop,
                            initInfect=initInfect
                        )
                        models.CityPosition.objects.create(
                            cityId=newCity,
                            x=x,
                            y=y
                        )
                    cityCount += 1

                # 新增道路信息
                if InitRoadData != "NULL":
                    roadCount = 0
                    for roadInfo in initRoadDataList:
                        value = roadInfo.split(":")[1]
                        if roadCount % 3 == 0:
                            departure = value
                        elif roadCount % 3 == 1:
                            destination = value
                        elif roadCount % 3 == 2:
                            volume = float(value)
                            models.InitRoadData.objects.create(
                                caseId=newCase,
                                departure=departure,
                                destination=destination,
                                volume=volume
                            )
                        roadCount += 1
                if (newCase):
                    models.AccountInformation.objects.filter(userId=userId).update(caseNumber=F("caseNumber") + 1)
                return JsonResponse({"message": "保存案例成功", "status": 200, "caseId": newCase.caseId})
            except Exception as e:
                print('str(Exception):\t', str(Exception))
                print('str(e):\t\t', str(e))
                print('repr(e):\t', repr(e))
                # print('e.message:\t', e.message)
                print('########################################################')
                return JsonResponse({"message": "保存案例失败", "status": 404})
        elif (caseMode == "地图模式"):
            initTotalNum = 0
            initTotalInfectedNum = 0
            initCityDataList = InitCityData.split(",")
            if InitRoadData != "NULL":
                initRoadDataList = InitRoadData.split(",")

            cityCount = 0
            for cityInfo in initCityDataList:
                value = cityInfo.split(":")[1]
                if cityCount % 3 == 1:
                    initPop = int(value)
                    initTotalNum += initPop
                elif cityCount % 3 == 2:
                    initInfect = int(value)
                    initTotalInfectedNum += initInfect
                cityCount += 1
            try:
                # 新增案例
                if (models.AccountInformation.objects.filter(userId=userId).exists()):
                    newCase = models.CaseData.objects.create(
                        userId=models.AccountInformation.objects.filter(userId=userId).first(),
                        caseName=caseName,
                        caseMode=caseMode,
                        cityNumber=int(cityNum),
                        roadNumber=int(roadNum),
                        initTotal=initTotalNum,
                        initTotalInfected=initTotalInfectedNum
                    )
                else:
                    return JsonResponse({"message": "目标用户不存在", "status": 404})
                # 新增城市信息
                cityCount = 0
                cityName = ""
                initPop = ""
                initInfect = ""
                x = 0.0
                y = 0.0
                for cityInfo in initCityDataList:
                    value = cityInfo.split(":")[1]
                    if cityCount % 3 == 0:
                        cityName = value
                    elif cityCount % 3 == 1:
                        initPop = int(value)
                    elif cityCount % 3 == 2:
                        initInfect = int(value)
                        newCity = models.InitCityData.objects.create(
                            caseId=newCase,
                            cityName=cityName,
                            initPop=initPop,
                            initInfect=initInfect
                        )
                    cityCount += 1

                # 新增道路信息
                if InitRoadData != "NULL":
                    roadCount = 0
                    for roadInfo in initRoadDataList:
                        value = roadInfo.split(":")[1]
                        if roadCount % 3 == 0:
                            departure = value
                        elif roadCount % 3 == 1:
                            destination = value
                        elif roadCount % 3 == 2:
                            volume = float(value)
                            models.InitRoadData.objects.create(
                                caseId=newCase,
                                departure=departure,
                                destination=destination,
                                volume=volume
                            )
                        roadCount += 1
                if (newCase):
                    models.AccountInformation.objects.filter(userId=userId).update(caseNumber=F("caseNumber") + 1)
                return JsonResponse({"message": "保存案例成功", "status": 200, "caseId": newCase.caseId})
            except Exception as e:
                print('str(Exception):\t', str(Exception))
                print('str(e):\t\t', str(e))
                print('repr(e):\t', repr(e))
                # print('e.message:\t', e.message)
                print('########################################################')
                return JsonResponse({"message": "保存案例失败", "status": 404})
        else:
            return JsonResponse({"message": "检测到未知的地图模式", "status": 404})
    else:
        return JsonResponse({"message": "该接口不支持此方法", "status": 404})


# 解析前端发回数据并送入模型进行模拟，取得返回数据并输出
def StartSimulate(request):
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录，保存案例需要先登录", "status": 404})
    elif request.method == "POST":
        # 获取post提交数据
        userId = request.POST.get('userId', None)
        caseName = request.POST.get('caseName', None)
        cityNum = request.POST.get('citynum', None)
        roadNum = request.POST.get('roadnum', None)
        caseMode = request.POST.get('caseMode', None)
        InitCityData = request.POST.get('InitCityData', None)
        InitRoadData = request.POST.get('InitRoadData', None)
        # 若获取到InitRoadData为"NULL"，代表无道路
        CityPosition = request.POST.get('CityPosition', None)
        dayNum = request.POST.get('daynum', None)
        if not(userId and caseName and cityNum and roadNum and InitCityData and InitRoadData and CityPosition and dayNum):
            return JsonResponse({"message": "表单未填写完整", "status": 404})

        if (caseMode == "自定模式"):
            # 案例计数：初始人口与初始感染人口
            initTotalNum = 0
            initTotalInfectedNum = 0
            initCityDataList = InitCityData.split(",")
            if InitRoadData != "NULL":
                initRoadDataList = InitRoadData.split(",")
            citypositionList = CityPosition.split(",")
            cityCount = 0
            for cityInfo in initCityDataList:
                value = cityInfo.split(":")[1]
                if cityCount % 3 == 1:
                    initPop = int(value)
                    initTotalNum += initPop
                elif cityCount % 3 == 2:
                    initInfect = int(value)
                    initTotalInfectedNum += initInfect
                cityCount += 1
            # 案例解析：从获取数据分别解析
            # 各城市人数 = 一维List
            # 各城市道路流通指数 = 实对称矩阵
            # 各城市感染人数 = 一维List
            # 各城市位置 = List，每个元素为一个数对，表示城市x,y坐标
            cityNum = int(cityNum)
            roadNum = int(roadNum)
            dayNum = int(dayNum)
            cityNameList = []
            initPopList = []
            initRoadList = [[0] * cityNum for row in range(cityNum)]
            initInfectedList = []
            cityPosList = []
            try:
                # 新增城市信息
                cityCount = 0
                initPop = ""
                initInfect = ""
                x = 0.0
                y = 0.0
                for cityInfo in initCityDataList:
                    value = cityInfo.split(":")[1]
                    posValue = citypositionList[cityCount].split(":")[1]
                    if cityCount % 3 == 0:
                        # 存入城市名称
                        cityNameList.append(value)
                    elif cityCount % 3 == 1:
                        # 存入城市初始人口
                        initPopList.append(int(value))
                        x = float(posValue)
                    elif cityCount % 3 == 2:
                        # 存入城市感染人口和城市坐标
                        initInfectedList.append(int(value))
                        y = float(posValue)
                        posList = []
                        posList.append(x)
                        posList.append(y)
                        cityPosList.append(posList)
                    cityCount += 1

                # 新增道路信息
                if InitRoadData != "NULL":
                    roadCount = 0
                    for roadInfo in initRoadDataList:
                        value = roadInfo.split(":")[1]
                        if roadCount % 3 == 0:
                            # 出发城市下标
                            departure = cityNameList.index(value)
                        elif roadCount % 3 == 1:
                            # 到达城市下标
                            destination = cityNameList.index(value)
                        elif roadCount % 3 == 2:
                            volume = float(value)
                            initRoadList[departure][destination] = volume
                            initRoadList[destination][departure] = volume
                        roadCount += 1
            except Exception as e:
                print('str(Exception):\t', str(Exception))
                print('str(e):\t\t', str(e))
                print('repr(e):\t', repr(e))
                print('########################################################')
                return JsonResponse({"message": "案例保存失败，数据库出错", "status": 404})
            # 调用模型函数，传入参数，获得返回值
            # dailyInfectMatrix = returnDataSimulator.GetPredict(
            #     popuList=initPopList,
            #     transMatrix=initRoadList,
            #     infectedList=initInfectedList
            #     )
            dailyInfectMatrix = returnDataSimulator.model(inputList=initPopList, length=dayNum)

            # 构造发回数据
            DailyForecastData = []
            for dayCount in range(dayNum):
                dayCase = []
                for cityIdx in range(cityNum):
                    cityCase = {}
                    cityCase["cityName"] = cityNameList[cityIdx]
                    cityCase["population"] = initPopList[cityIdx]

                    if (dayCount == 0):
                        cityCase["infected"] = initInfectedList[cityIdx]
                        cityCase["dailyinfected"] = int(dailyInfectMatrix[cityIdx][dayCount])
                    else:
                        cityCase["infected"] = int(dailyInfectMatrix[cityIdx][dayCount])+initInfectedList[cityIdx]
                        cityCase["dailyinfected"] = int(dailyInfectMatrix[cityIdx][dayCount]) - int(dailyInfectMatrix[cityIdx][dayCount-1])

                    dayCase.append(cityCase)
                DailyForecastData.append(dayCase)
            return JsonResponse({"DailyForecastData": DailyForecastData, "status": 200})
        elif (caseMode == "地图模式"):
            # 案例计数：初始人口与初始感染人口
            initTotalNum = 0
            initTotalInfectedNum = 0
            initCityDataList = InitCityData.split(",")
            if InitRoadData != "NULL":
                initRoadDataList = InitRoadData.split(",")
            cityCount = 0
            for cityInfo in initCityDataList:
                value = cityInfo.split(":")[1]
                if cityCount % 3 == 1:
                    initPop = int(value)
                    initTotalNum += initPop
                elif cityCount % 3 == 2:
                    initInfect = int(value)
                    initTotalInfectedNum += initInfect
                cityCount += 1
            # 案例解析：从获取数据分别解析
            # 各城市人数 = 一维List
            # 各城市道路流通指数 = 实对称矩阵
            # 各城市感染人数 = 一维List
            # 各城市位置 = List，每个元素为一个数对，表示城市x,y坐标
            cityNum = int(cityNum)
            roadNum = int(roadNum)
            dayNum = int(dayNum)
            cityNameList = []
            initPopList = []
            initRoadList = [[0] * cityNum for row in range(cityNum)]
            initInfectedList = []
            try:
                # 新增城市信息
                cityCount = 0
                initPop = ""
                initInfect = ""
                x = 0.0
                y = 0.0
                for cityInfo in initCityDataList:
                    value = cityInfo.split(":")[1]
                    if cityCount % 3 == 0:
                        # 存入城市名称
                        cityNameList.append(value)
                    elif cityCount % 3 == 1:
                        # 存入城市初始人口
                        initPopList.append(int(value))
                    elif cityCount % 3 == 2:
                        # 存入城市感染人口和城市坐标
                        initInfectedList.append(int(value))
                    cityCount += 1

                # 新增道路信息
                if InitRoadData != "NULL":
                    roadCount = 0
                    for roadInfo in initRoadDataList:
                        value = roadInfo.split(":")[1]
                        if roadCount % 3 == 0:
                            # 出发城市下标
                            departure = cityNameList.index(value)
                        elif roadCount % 3 == 1:
                            # 到达城市下标
                            destination = cityNameList.index(value)
                        elif roadCount % 3 == 2:
                            volume = float(value)
                            initRoadList[departure][destination] = volume
                            initRoadList[destination][departure] = volume
                        roadCount += 1
            except Exception as e:
                print('str(Exception):\t', str(Exception))
                print('str(e):\t\t', str(e))
                print('repr(e):\t', repr(e))
                # print('e.message:\t', e.message)
                print('########################################################')
                return JsonResponse({"message": "案例保存失败，数据库出错", "status": 404})
            # 调用模型函数，传入参数，获得返回值
            # dailyInfectMatrix = returnDataSimulator.GetPredict(
            #     popuList=initPopList,
            #     transMatrix=initRoadList,
            #     infectedList=initInfectedList
            #     )
            dailyInfectMatrix = returnDataSimulator.model(inputList=initPopList, length=dayNum)
            # 构造发回数据
            DailyForecastData = []
            for dayCount in range(dayNum):
                dayCase = []
                for cityIdx in range(cityNum):
                    cityCase = {}
                    cityCase["cityName"] = cityNameList[cityIdx]
                    cityCase["population"] = initPopList[cityIdx]

                    if (dayCount == 0):
                        cityCase["infected"] = initInfectedList[cityIdx]
                        cityCase["dailyinfected"] = int(dailyInfectMatrix[cityIdx][dayCount])
                    else:
                        cityCase["infected"] = int(dailyInfectMatrix[cityIdx][dayCount])+initInfectedList[cityIdx]
                        cityCase["dailyinfected"] = int(dailyInfectMatrix[cityIdx][dayCount]) - int(dailyInfectMatrix[cityIdx][dayCount-1])

                    dayCase.append(cityCase)
                DailyForecastData.append(dayCase)
            return JsonResponse({"DailyForecastData": DailyForecastData, "status": 200})
        else:
            return JsonResponse({"message": "检测到未知的地图模式", "status": 404})
    return JsonResponse({"message": "该接口不支持此方法", "status": 404})


# 返回所有案例信息
# 根据caseId发送对应案例的所有相关信息，包括城市，城市位置，道路信息
# 发送成功，返回消息和200状态码
# 发送失败，返回消息和404状态码
def GetCaseInfos(request):
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录", "status": 404})
    elif request.method == "POST":
        caseId = request.POST.get("caseId", None)
        if caseId:
            try:
                caseInfo = models.CaseData.objects.filter(caseId=caseId).first()
                cityInfos = models.InitCityData.objects.filter(caseId=caseInfo)
                roadInfos = models.InitRoadData.objects.filter(caseId=caseInfo)

                cases = {}
                cases["caseName"] = caseInfo.caseName
                cases["cityNum"] = caseInfo.cityNumber
                cases["roadNum"] = caseInfo.roadNumber
                cases["caseMode"] = caseInfo.caseMode

                cityList = []
                cityPosList = []
                for cityIdx in range(len(cityInfos)):
                    cityCase = {}
                    cityCase["cityName"] = cityInfos[cityIdx].cityName
                    cityCase["initPop"] = cityInfos[cityIdx].initPop
                    cityCase["initInfect"] = cityInfos[cityIdx].initInfect
                    cityList.append(cityCase)

                    if caseInfo.caseMode == "自定模式":
                        cityPosCase = {}
                        cityPosCase["cityName"] = cityInfos[cityIdx].cityName
                        cityPosCase["x"] = cityInfos[cityIdx].cityposition.x
                        cityPosCase["y"] = cityInfos[cityIdx].cityposition.y
                        cityPosList.append(cityPosCase)

                roadList = []
                if (roadInfos.exists()):
                    for roadIdx in range(len(roadInfos)):
                        roadCase = {}
                        roadCase["departure"] = roadInfos[roadIdx].departure
                        roadCase["destination"] = roadInfos[roadIdx].destination
                        roadCase["volume"] = roadInfos[roadIdx].volume
                        roadList.append(roadCase)
                    cases["InitRoadData"] = roadList
                cases["InitCityData"] = cityList
                if caseInfo.caseMode == "自定模式":
                    cases["CityPosition"] = cityPosList

                return JsonResponse({"message": "成功返回数据", "cases": cases, "status": 200})
            except Exception as e:
                print('str(Exception):\t', str(Exception))
                print('str(e):\t\t', str(e))
                print('repr(e):\t', repr(e))
                # print('e.message:\t', e.message)
                print('########################################################')
                return JsonResponse({"message": "数据库出错", "status": 404})
        return JsonResponse({"message": "请求参数未填写", "status": 404})
    else:
        return JsonResponse({"message": "请求方法未注册", "status": 404})


# 返回所有超级管理员信息
# 获取分页信息
# 获取所有超级管理员信息，分页器处理后发出
# 发送成功，返回消息和200状态码
# 发送失败，返回消息和404状态码
def GetUserInfos(request):
    # if not request.session.get('isLogin', None):
    #     return JsonResponse({"message": "你还未登录", "status": 404})
    # el
    if request.method == "GET":
        pageSize = request.GET.get("pageSize")
        page = request.GET.get("page")
        accountInfos = models.AccountInformation.objects\
            .select_related("personalprofile").all()\
            .exclude(authority="超级管理员")\
            .order_by('userId')
        accountPaginator = paginator.Paginator(accountInfos, pageSize)
        if page == "":
            page = 1
        else:
            page = int(page)
        pageInfos = accountPaginator.page(page)
        jsonList = []
        for accountInfo in pageInfos:
            accountInfoDict = model_to_dict(accountInfo)
            # print("rawData", accountInfo.personalprofile.GetAvatarUrl())
            profileDict = model_to_dict(accountInfo.personalprofile)
            profileDict["avatar"] = accountInfo.personalprofile.GetAvatarUrl()
            # print("profileDict", profileDict["avatar"])
            jsonList.append({**accountInfoDict, **profileDict})
        jsonRes = json.loads(json.dumps(jsonList, cls=DateEnconding))
        print(jsonRes)
        return JsonResponse({
            'data': jsonRes,
            'pagination': accountPaginator.count,
            'pageSize': accountPaginator.per_page,
            'page': pageInfos.start_index() // accountPaginator.per_page + 1
        })
    else:
        return JsonResponse({"message": "请求方法未注册", "status": 404})


# 返回所有普通用户信息
# 获取分页信息
# 获取所有普通用户信息，分页器处理后发出
# 发送成功，返回消息和200状态码
# 发送失败，返回消息和404状态码
def GetGeneralUserInfos(request):
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录", "status": 404})
    elif request.method == "GET":
        pageSize = request.GET.get("pageSize")
        page = request.GET.get("page")
        generalUserInfos = models.AccountInformation.objects\
            .select_related("personalprofile")\
            .filter(authority="普通用户")\
            .order_by('userId')
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
            profileDict["avatar"] = accountInfo.personalprofile.GetAvatarUrl()
            jsonList.append({**accountInfoDict, **profileDict})
        jsonRes = json.loads(json.dumps(jsonList, cls=DateEnconding))
        print(jsonRes)
        return JsonResponse({
            'data': jsonRes,
            'pagination': accountPaginator.count,
            'pageSize': accountPaginator.per_page,
            'page': pageInfos.start_index() // accountPaginator.per_page + 1
        })
    else:
        return JsonResponse({"message": "请求方法未注册", "status": 404})


# 返回所有管理员信息
# 获取分页信息
# 获取所有管理员信息，分页器处理后发出
# 发送成功，返回消息和200状态码
# 发送失败，返回消息和404状态码
def GetAdminInfos(request):
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录", "status": 404})
    elif request.method == "GET":
        pageSize = request.GET.get("pageSize")
        page = request.GET.get("page")
        adminUserInfos = models.AccountInformation.objects\
            .select_related("personalprofile")\
            .filter(authority="管理员")\
            .order_by('userId')
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
            profileDict["avatar"] = accountInfo.personalprofile.GetAvatarUrl()
            jsonList.append({**accountInfoDict, **profileDict})
        jsonRes = json.loads(json.dumps(jsonList, cls=DateEnconding))
        print(jsonRes)
        return JsonResponse({
            'data': jsonRes,
            'pagination': accountPaginator.count,
            'pageSize': accountPaginator.per_page,
            'page': pageInfos.start_index() // accountPaginator.per_page + 1
        })
    else:
        return JsonResponse({"message": "请求方法未注册", "status": 404})


# 返回高频城市信息
# 发送成功，返回消息和200状态码
# 发送失败，返回消息和404状态码
def GetTopCityInfos(request):
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录，获取高频城市需要先登录", "status": 404})
    elif request.method == "GET":
        # 该接口无提交数据
        # 获取统计信息
        try:
            cityInfos = models.InitCityData.objects\
                        .filter(caseId__caseMode="地图模式")\
                        .values("cityName")\
                        .annotate(cityCount=Count("cityName"))\
                        .order_by('cityName')

            cityInfos = cityInfos.order_by('-cityCount')[:6]
            jsonList = []
            for cityInfo in cityInfos:
                cityInfoDict = {"cityName": cityInfo["cityName"], "cityCount": cityInfo["cityCount"]}
                jsonList.append({**cityInfoDict})
            jsonRes = json.loads(json.dumps(jsonList, cls=DateEnconding))
            print(jsonRes)
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # print('e.message:\t', e.message)
            print('########################################################')
            return JsonResponse({"message": "案例保存失败，数据库出错", "status": 404})
        return JsonResponse({"TopcityInfos": jsonRes, "status": 200})
    else:
        return JsonResponse({"message": "请求方法未注册", "status": 404})


# 返回各性别人数
# 发送成功，返回消息和200状态码
# 发送失败，返回消息和404状态码
def GetSexNum(request):
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录，获取高频城市需要先登录", "status": 404})
    elif request.method == "GET":
        # 该接口无提交数据
        # 获取统计信息
        try:
            sexInfos = models.PersonalProfile.objects\
                        .values("sex")\
                        .annotate(sexCount=Count("userId__userId"))\
                        .order_by('sex')
            jsonList = []
            for sexInfo in sexInfos:
                sexInfoDict = {"sex": sexInfo["sex"], "sexCount": sexInfo["sexCount"]}
                jsonList.append({**sexInfoDict})
            jsonRes = json.loads(json.dumps(jsonList, cls=DateEnconding))
            print(jsonRes)
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # print('e.message:\t', e.message)
            print('########################################################')
            return JsonResponse({"message": "信息获取失败，数据库出错", "status": 404})
        return JsonResponse({"TopcityInfos": jsonRes, "message": "信息获取成功", "status": 200})
    else:
        return JsonResponse({"message": "请求方法未注册", "status": 404})


# 返回最近五个月每月新增用户数量和案例数量
# 发送成功，返回消息和200状态码
# 发送失败，返回消息和404状态码
def GetUserCaseStat(request):
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录，获取用户案例统计信息需要先登录", "status": 404})
    elif request.method == "GET":
        # 该接口无提交数据
        # 获取统计信息
        try:
            nowDate = timezone.now().date().replace(day=1)
            pastLimitDate = nowDate + relativedelta(months=-5)

            jsonList = []
            for i in range(5):
                accountCountInfo = models.AccountInformation.objects\
                    .filter(createDate__gte=pastLimitDate)\
                    .filter(createDate__lt=pastLimitDate + relativedelta(months=+1))\
                    .aggregate(accountCount=Count("userId"))
                caseCountInfo = models.CaseData.objects\
                    .filter(caseCreateDate__gte=pastLimitDate)\
                    .filter(caseCreateDate__lt=pastLimitDate + relativedelta(months=+1))\
                    .aggregate(caseCount=Count("caseId"))

                statInfoDict = {
                    "date": pastLimitDate.strftime("%Y.%m"),
                    "userCount": accountCountInfo["accountCount"],
                    "caseCount": caseCountInfo["caseCount"]
                    }
                jsonList.append({**statInfoDict})
                pastLimitDate = pastLimitDate + relativedelta(months=+1)
            jsonRes = json.loads(json.dumps(jsonList, cls=DateEnconding))
            print(jsonRes)
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # print('e.message:\t', e.message)
            print('########################################################')
            return JsonResponse({"message": "信息获取失败，数据库出错", "status": 404})
        return JsonResponse({"UserCaseStatInfos": jsonRes, "message": "信息获取成功", "status": 200})
    else:
        return JsonResponse({"message": "请求方法未注册", "status": 404})


# 以下类均为继承ModelViewSet类的视图集类，其中成员变量均为继承而来
@method_decorator(LoginAuthenticate, name='dispatch')
class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.AccountInformation.objects.all()
    serializer_class = customSerializers.AccountInformationSerializer


@method_decorator(LoginAuthenticate, name='dispatch')
class CaseViewSet(viewsets.ModelViewSet):
    queryset = models.CaseData.objects.all()
    serializer_class = customSerializers.CaseDataSerializer
    pagination_class = paginations.MyFormatResultsSetPagination
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filter_class = filters.CaseFilter
    ordering_fields = ('caseName', 'initTotal', 'initTotalInfected', 'cityNumber', 'roadNumber',)
    ordering = ('caseId',)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if (instance):
            models.AccountInformation.objects.filter(userId=instance.userId.userId).update(caseNumber=F("caseNumber") - 1)
        return super(CaseViewSet, self).destroy(request, *args, **kwargs)


@method_decorator(LoginAuthenticate, name='dispatch')
class PersonalProfileViewSet(viewsets.ModelViewSet):
    queryset = models.PersonalProfile.objects.all()
    serializer_class = customSerializers.PersonalProfileSerializer
