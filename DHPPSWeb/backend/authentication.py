# from django.http import JsonResponse
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions


class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        sessionId = request.COOKIES.get("sessionid", None)
        # if not sessionId:
        #     return JsonResponse({"message": "您无权访问接口", "status": 404})
        # else:
        #     if not request.session.get('isLogin', None):
        #         return JsonResponse({"message": "您无权访问接口", "status": 404})

        if not sessionId:
            raise exceptions.AuthenticationFailed('您没有登录')
        else:
            if not request.session.get('isLogin', None):
                raise exceptions.AuthenticationFailed('您没有登录')