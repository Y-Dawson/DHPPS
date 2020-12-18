from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from backend import filters
from rest_framework.filters import OrderingFilter
from backend import paginations
from django.shortcuts import render, get_object_or_404
from django.views import View
from backend import models
from backend import customSerializers
from backend.SendSms import SendSms
from backend.returnDataSimulator import model
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

g_logger = logging.getLogger("django")

'''
@receiver(pre_delete, sender=models.PersonalProfile)
def handle_camera_deleted(instance: models.PersonalProfile, **_):
    instance.file.delete(save=False)
'''


# 返回渲染主页，其后由前端负责跳转逻辑
def Index(request):
    """
    render Index page
    :param request: request object
    :return: page
    """
    return render(request, 'Index.html')


# 对传入的密码和salt进行md5加密，返回得到的加密密码
def HashPwd(pwd, salt):
    h = hashlib.md5()
    pwd = pwd + salt
    h.update(pwd.encode())
    return h.hexdigest()


# json序列化时对datetime处理的函数
class DateEnconding(json.JSONEncoder):
    def Default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime('%Y/%m/%d')


# 登录检测装饰器
def LoginRequired(view_func):
    # 登录判断装饰器
    def Wrapper(request, *view_args, **view_kwargs):
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
    return Wrapper


# 登录函数视图
# 从参数获取phoneNum和password，取出对应salt加密，并判断是否和存储加密密码相同
# 登录成功，返回消息和200状态码
# 登录失败，返回消息和404状态码
def Signin(request):
    '''
    # 若已经登录，直接进入已登录账号
    if request.session.get('isLogin', None):
        return JsonResponse({"message": "你已经登录", "status": 404})
    el
    '''
    if request.method == "POST":
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
                if (accountInfo.LoginData.userPassword == HashPwd(pwd=password, salt=accountInfo.LoginData.salt)):
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
                    response.set_cookie('userId', accountInfo.userId)
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
# 登出失败，返回消息和404状态码
def Logout(request):
    message = "登出成功"
    status = 200
    if not request.session.get('isLogin', None):
        # 如果本来就未登录，也就没有登出一说
        return JsonResponse({"message": "未登录，无法登出", "status": 404})
    else:
        request.session.flush()
        # del request.session['isLogin']
        # del request.session['userId']
        # del request.session['userName']
        response = JsonResponse({"message": message, "status": status})
        response.delete_cookie("userId")
        return response


# 请求短信验证码函数视图
# 通过阿里云短信服务发送验证码，并保存验证码到redis缓存
# 发送成功，返回消息和200状态码
# 发送失败，返回消息和404状态码
def RequestSmsCode(request):
    if request.method == "POST":
        phoneNum = request.POST.get('phonenum', None)
        code, message, result = SendSms(phoneNum)
        try:
            # 4.连接到redis
            redisClient = get_redis_connection('sms_code')
            # 5.生成redis管道
            pipeline = redisClient.pipeline()
            # 6.保存验证码，用于后续与用户输入值对比，设置过期时间
            pipeline.setex(phoneNum, 300, code)
            # 7.传递指令
            pipeline.execute()
        except Exception:
            JsonResponse({"message": "保存到redis失败", "status": 404})
        JsonResponse({"message": "验证码已发送", "status": 200})


# 注册函数视图
# 从参数获取userName，phonenum,email,password,verifyCode
# 登出成功，返回消息和200状态码
# 登出失败，返回消息和404状态码
def Signup(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。
        message = "登录状态，无法注册"
        status = 404
    elif request.method == "POST":
        userName = request.POST.get('userName', None)
        phonenum = request.POST.get('phonenum', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        verifyCode = request.POST.get('verifyCode', None)
        print({
            "userName": userName,
            'phonenum': phonenum,
            'email': email,
            "password": password,
            'verifyCode': verifyCode
        })
        message = "请检查填写的内容！"
        status = 404
        if userName and phonenum and email and password and verifyCode:  # 获取数据
            sameNameUser = models.PersonalProfile.objects.filter(userName=userName)
            if sameNameUser:  # 用户名唯一
                message = '用户已经存在，请重新输入用户名！'
                status = 404
            else:
                samePhoneUser = models.PersonalProfile.objects.filter(phoneNumber=phonenum)
                if samePhoneUser:  # 手机号码唯一
                    message = '该手机号码已被注册，请使用别的手机号码！'
                    status = 404
                else:
                    # 当一切都OK的情况下，创建新用户
                    try:
                        newAccountInfo = models.AccountInformation.objects.create(
                            themeNo=models.Theme.objects.filter(themeNo=1).first(),
                            createDate=timezone.now()
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
                            phoneNumber=phonenum,
                            email=email
                        )
                        g_logger.info(json.dumps(newLoginData, cls=DateEnconding))
                        g_logger.info(json.dumps(newUser, cls=DateEnconding))
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
# 从参数获取原密码和userId
# 根据userId查找对应用户的LoginData的密码
# 比对通过后，生成新的salt和密码，存入数据库
# 修改成功，返回消息和200状态码
# 修改失败，返回消息和404状态码
def ChangePwd(request):
    '''
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录", "status": 404})
    el
    '''
    if request.method == "POST":
        # 从参数获取oldPassword和password
        userId = request.POST.get("userId", None)
        oldPassword = request.POST.get('oldPassword', None)
        newPassword = request.POST.get('newPassword', None)
        if userId and oldPassword and newPassword:
            account = models.AccountInformation.objects.filter(userId=userId)
            if not account.exists():
                return JsonResponse({"message": "当前账号与浏览器记录不一致", "status": 404})
            account = account.first()
            # 检测账号原密码是否符合
            if (account.LoginData.userPassword == HashPwd(pwd=oldPassword, salt=account.LoginData.salt)):
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
    '''
    if request.session.get('isLogin', None):
        return JsonResponse({"message": "你已经登录，忘记密码需先退出", "status": 404})
    el
    '''
    if request.method == "POST":
        # 从参数获取phoneNum和password
        phoneNum = request.POST.get('phonenum', None)
        verifyCode = request.POST.get('verifyCode', None)
        newPassword = request.POST.get('newPassword', None)
        if phoneNum and verifyCode and newPassword:
            # 从数据库获取phonenum和对应userId，取出salt
            # 获取失败则捕捉错误
            profile = models.PersonalProfile.objects.filter(phoneNumber=int(phoneNum))
            if not profile.exists():
                return JsonResponse({"message": "该手机未注册", "status": 404})
            profile = profile.first()
            account = models.AccountInformation.objects.get(userId=profile.userId.userId)

            # 缺少逻辑：检测短信验证码是否正确
            newSalt = secrets.token_hex(4)
            encryPassword = HashPwd(pwd=newPassword, salt=newSalt)
            models.LoginData.objects.filter(userId=account.userId).update(userPassword=encryPassword, salt=newSalt)
            return JsonResponse({"message": "修改成功", "status": 200})
    else:
        return JsonResponse({"message": "参数传递方式有误", "status": 404})


# 存储前端发回的案例参数视图
# 获取表单数据
# 解析表单数据生成对应models存入
# 保存成功，返回消息和200状态码
# 保存失败，返回消息和404状态码
def SaveCase(request):
    '''
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录，保存案例需要先登录", "status": 404})
    el
    '''
    if request.method == "POST":
        userId = request.POST.get('userId', None)
        caseName = request.POST.get('caseName', None)
        cityNum = request.POST.get('citynum', None)
        roadNum = request.POST.get('roadnum', None)
        InitCityData = request.POST.get('InitCityData', None)
        InitRoadData = request.POST.get('InitRoadData', None)
        CityPosition = request.POST.get('CityPosition', None)
        if not(userId and caseName and cityNum and roadNum and InitCityData and InitRoadData and CityPosition):
            return JsonResponse({"message": "表单未填写完整", "status": 404})
        # 案例计数：初始人口与初始感染人口
        initTotalNum = 0
        initTotalInfectedNum = 0
        initcitydataList = InitCityData.split(",")
        initroaddataList = InitRoadData.split(",")
        citypositionList = CityPosition.split(",")

        cityCount = 0
        for cityInfo in initcitydataList:
            value = cityInfo.split(":")[1]
            if cityCount % 3 == 1:
                initPop = int(value)
                initTotalNum += initPop
            elif cityCount % 3 == 2:
                initInfect = int(value)
                initTotalInfectedNum += initInfect
            cityCount += 1
        message = "开始进行案例保存"
        status = 200
        newcaseId = 0
        try:
            # 新增案例
            newCase = models.CaseData.objects.create(
                userId=models.AccountInformation.objects.filter(userId=userId).first(),
                caseName=caseName,
                cityNumber=int(cityNum),
                roadNumber=int(roadNum),
                initTotal=initTotalNum,
                initTotalInfected=initTotalInfectedNum
            )
            # 新增城市信息
            cityCount = 0
            cityName = ""
            initPop = ""
            initInfect = ""
            x = 0.0
            y = 0.0
            for cityInfo in initcitydataList:
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
            roadCount = 0
            for roadInfo in initroaddataList:
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
            message = "保存案例成功"
            status = 200
            newcaseId = newCase.caseId
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # print('e.message:\t', e.message)
            print('########################################################')
            message = "注册失败"
            status = 404
        return JsonResponse({"message": message, "status": status, "caseId": newcaseId})


# 解析前端发回数据并送入模型进行模拟，取得返回数据并输出
def StartSimulate(request):
    '''
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录，保存案例需要先登录", "status": 404})
    el
    '''
    if request.method == "POST":
        # 获取post提交数据
        userId = request.POST.get('userId', None)
        caseName = request.POST.get('caseName', None)
        cityNum = request.POST.get('citynum', None)
        roadNum = request.POST.get('roadnum', None)
        InitCityData = request.POST.get('InitCityData', None)
        InitRoadData = request.POST.get('InitRoadData', None)
        CityPosition = request.POST.get('CityPosition', None)
        dayNum = request.POST.get('daynum', None)
        if not(userId and caseName and cityNum and roadNum and InitCityData and InitRoadData and CityPosition and dayNum):
            return JsonResponse({"message": "表单未填写完整", "status": 404})
        # 案例计数：初始人口与初始感染人口
        initTotalNum = 0
        initTotalInfectedNum = 0
        initcitydataList = InitCityData.split(",")
        initroaddataList = InitRoadData.split(",")
        citypositionList = CityPosition.split(",")
        cityCount = 0
        for cityInfo in initcitydataList:
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
            for cityInfo in initcitydataList:
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
            roadCount = 0
            for roadInfo in initroaddataList:
                value = roadInfo.split(":")[1]
                if roadCount % 3 == 0:
                    # 出发城市下标
                    departure = cityNameList.Index(value)
                elif roadCount % 3 == 1:
                    # 到达城市下标
                    destination = cityNameList.Index(value)
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
        dailyInfectMatrix = model(initPopList, dayNum)
        # 以下为模拟产生返回数据
        # dailyInfectMatrix = []
        # for dayCount in range(dayNum):
        #     dayNewInfect = []
        #     for cityIdx in range(cityNum):
        #         dayNewInfect.append(dayCount*10)
        #     dailyInfectMatrix.append(dayNewInfect)

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
    return JsonResponse({"message": "该接口不支持此方法", "status": 404})


class ImageCodeView(View):
    # 该函数为view中函数重写，函数名不可更改
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
        g_logger.info('verify_text:{}'.format(code))
        # 9.响应：输出图片数据
        return JsonResponse(image, content_type='image/png')

    # 该函数为view中函数重写，函数名不可更改
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


def GetAllCaseInfos(request):
    if request.method == "POST":
        caseId = request.POST.get("caseId", None)
        if caseId:
            try:
                caseInfo = models.CaseData.objects.filter(caseId=caseId).first()
                cityInfos = models.InitCityData.objects.filter(caseId=caseInfo)
                roadInfos = models.InitRoadData.objects.filter(caseId=caseInfo)

                cases = {}
                cases["caseName"] = caseInfo.caseName
                cases["citynum"] = len(cityInfos)
                cases["roadnum"] = len(roadInfos)

                cityList = []
                cityPosList = []
                for cityIdx in range(len(cityInfos)):
                    cityCase = {}
                    cityCase["cityName"] = cityInfos[cityIdx].cityName
                    cityCase["initPop"] = cityInfos[cityIdx].initPop
                    cityCase["initInfect"] = cityInfos[cityIdx].initInfect
                    cityList.append(cityCase)

                    cityPosCase = {}
                    cityPosCase["cityName"] = cityInfos[cityIdx].cityName
                    cityPosCase["x"] = cityInfos[cityIdx].CityPosition.x
                    cityPosCase["y"] = cityInfos[cityIdx].CityPosition.y
                    cityPosList.append(cityPosCase)

                roadList = []
                for roadIdx in range(len(roadInfos)):
                    roadCase = {}
                    roadCase["departure"] = roadInfos[roadIdx].departure
                    roadCase["destination"] = roadInfos[roadIdx].destination
                    roadCase["volume"] = roadInfos[roadIdx].volume
                    roadList.append(roadCase)

                cases["InitCityData"] = cityList
                cases["InitRoadData"] = roadList
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
    return JsonResponse({"message": "请求方法未注册", "status": 404})


def GetUserInfos(request):
    if request.method == "GET":
        pageSize = request.GET.get("pageSize")
        page = request.GET.get("page")
        accountInfos = models.AccountInformation.objects.select_related("PersonalProfile").all().exclude(authority="超级管理员").order_by('userId')
        accountPaginator = paginator.Paginator(accountInfos, pageSize)
        if page == "":
            page = 1
        else:
            page = int(page)
        pageInfos = accountPaginator.page(page)
        jsonList = []
        for accountInfo in pageInfos:
            accountInfoDict = model_to_dict(accountInfo)
            profileDict = model_to_dict(accountInfo.PersonalProfile)
            jsonList.append({**accountInfoDict, **profileDict})
        jsonRes = json.loads(json.dumps(jsonList, cls=DateEnconding))
        print(jsonRes)
        return JsonResponse({
            'data': jsonRes,
            'pagination': accountPaginator.count,
            'pageSize': accountPaginator.per_page,
            'page': pageInfos.start_Index() // accountPaginator.per_page + 1
        })


def GetGeneralUserInfos(request):
    if request.method == "GET":
        pageSize = request.GET.get("pageSize")
        page = request.GET.get("page")
        generalUserInfos = models.AccountInformation.objects.select_related("PersonalProfile").filter(authority="普通用户").order_by('userId')
        accountPaginator = paginator.Paginator(generalUserInfos, pageSize)
        if page == "":
            page = 1
        else:
            page = int(page)
        pageInfos = accountPaginator.page(page)
        jsonList = []
        for accountInfo in pageInfos:
            accountInfoDict = model_to_dict(accountInfo)
            profileDict = model_to_dict(accountInfo.PersonalProfile)
            jsonList.append({**accountInfoDict, **profileDict})
        jsonRes = json.loads(json.dumps(jsonList, cls=DateEnconding))
        print(jsonRes)
        return JsonResponse({
            'data': jsonRes,
            'pagination': accountPaginator.count,
            'pageSize': accountPaginator.per_page,
            'page': pageInfos.start_Index() // accountPaginator.per_page + 1
        })


def GetAdminInfos(request):
    if request.method == "GET":
        pageSize = request.GET.get("pageSize")
        page = request.GET.get("page")
        adminUserInfos = models.AccountInformation.objects.select_related("PersonalProfile").filter(authority="管理员").order_by('userId')
        accountPaginator = paginator.Paginator(adminUserInfos, pageSize)
        if page == "":
            page = 1
        else:
            page = int(page)
        pageInfos = accountPaginator.page(page)
        jsonList = []
        for accountInfo in pageInfos:
            accountInfoDict = model_to_dict(accountInfo)
            profileDict = model_to_dict(accountInfo.PersonalProfile)
            jsonList.append({**accountInfoDict, **profileDict})
        jsonRes = json.loads(json.dumps(jsonList, cls=DateEnconding))
        print(jsonRes)
        return JsonResponse({
            'data': jsonRes,
            'pagination': accountPaginator.count,
            'pageSize': accountPaginator.per_page,
            'page': pageInfos.start_Index() // accountPaginator.per_page + 1
        })


# 以下类均为继承ModelViewSet类的视图集类，其中成员变量均为继承而来
class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.AccountInformation.objects.all()
    serializer_class = customSerializers.AccountInformationSerializer


class CaseViewSet(viewsets.ModelViewSet):
    queryset = models.CaseData.objects.all()
    serializer_class = customSerializers.CaseDataSerializer
    pagination_class = paginations.MyFormatResultsSetPagination
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filter_class = filters.CaseFilter
    ordering_fields = ('caseName', 'initTotal', 'initTotalInfected', 'cityNumber', 'roadNumber',)
    ordering = ('caseId',)


class CityPosViewSet(viewsets.ModelViewSet):
    queryset = models.CityPosition.objects.all()
    serializer_class = customSerializers.CitypositionSerializer


class DailyForeViewSet(viewsets.ModelViewSet):
    queryset = models.DailyForecastData.objects.all()
    serializer_class = customSerializers.DailyforecastdataSerializer


class InitCityViewSet(viewsets.ModelViewSet):
    queryset = models.InitCityData.objects.all()
    serializer_class = customSerializers.InitcitydataSerializer


class InitRoadViewSet(viewsets.ModelViewSet):
    queryset = models.InitRoadData.objects.all()
    serializer_class = customSerializers.InitroaddataSerializer


class LoginViewSet(viewsets.ModelViewSet):
    queryset = models.LoginData.objects.all()
    serializer_class = customSerializers.LogindataSerializer


class ModelViewSet(viewsets.ModelViewSet):
    queryset = models.ModelData.objects.all()
    serializer_class = customSerializers.ModeldataSerializer


class PersonalProfileViewSet(viewsets.ModelViewSet):
    queryset = models.PersonalProfile.objects.all()
    serializer_class = customSerializers.PersonalProfileSerializer


class ThemeViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    queryset = models.Theme.objects.all()
    serializer_class = customSerializers.ThemeSerializer
