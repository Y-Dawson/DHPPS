from django.urls import path
from rest_framework.routers import DefaultRouter

from backend import views


router = DefaultRouter()
router.register('AccountInfos', views.AccountViewSet)

urlpatterns = [
    # 渲染首页，其后的页面跳转由前端负责
    path('', views.index, name="index"),

    # 以下为对任意模型的增删改查列

    # 关于accountInfo的请求：
    # 无参数：get=list all,post=create new
    path('accountInfo/', views.AccountViewSet.as_view({'get': 'list', 'post': 'create'})),
    # 有参数：get=retrieve one,put=update one,delete=delete one
    path('accountInfo/<int:pk>/', views.AccountViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # 关于Casedata的请求
    # 无参数：get=list all,post=create new
    path('case/', views.ThemeViewSet.as_view({'get': 'list', 'post': 'create'})),
    # 有参数：get=retrieve one,put=update one,delete=delete one
    path('case/<int:pk>/', views.ThemeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # 关于Cityposition的请求
    # 无参数：get=list all,post=create new
    path('citypos/', views.CityPosViewSet.as_view({'get': 'list', 'post': 'create'})),
    # 有参数：get=retrieve one,put=update one,delete=delete one
    path('citypos/<int:pk>/', views.CityPosViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # 关于Dailyforecastdata的请求
    # 无参数：get=list all,post=create new
    path('dailyfore/', views.DailyForeViewSet.as_view({'get': 'list', 'post': 'create'})),
    # 有参数：get=retrieve one,put=update one,delete=delete one
    path('dailyfore/<int:pk>/', views.DailyForeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # 关于Initcitydata的请求
    # 无参数：get=list all,post=create new
    path('initcity/', views.InitCityViewSet.as_view({'get': 'list', 'post': 'create'})),
    # 有参数：get=retrieve one,put=update one,delete=delete one
    path('initcity/<int:pk>/', views.InitCityViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # 关于Initroaddata的请求
    # 无参数：get=list all,post=create new
    path('initroad/', views.InitRoadViewSet.as_view({'get': 'list', 'post': 'create'})),
    # 有参数：get=retrieve one,put=update one,delete=delete one
    path('initroad/<int:pk>/', views.InitRoadViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # 关于Logindata的请求
    # 无参数：get=list all,post=create new
    path('logindata/', views.LoginViewSet.as_view({'get': 'list', 'post': 'create'})),
    # 有参数：get=retrieve one,put=update one,delete=delete one
    path('logindata/<int:pk>/', views.LoginViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # 关于Modeldata的请求
    # 无参数：get=list all,post=create new
    path('model/', views.ModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    # 有参数：get=retrieve one,put=update one,delete=delete one
    path('model/<int:pk>/', views.ModelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # 关于Personalprofile的请求
    # 无参数：get=list all,post=create new
    path('profile/', views.PersonalProfileViewSet.as_view({'get': 'list', 'post': 'create'})),
    # 有参数：get=retrieve one,put=update one,delete=delete one
    path('profile/<int:pk>/', views.PersonalProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # 关于theme的请求
    # 无参数：get=list all,post=create new
    path('theme/', views.ThemeViewSet.as_view({'get': 'list', 'post': 'create'})),
    # 有参数：get=retrieve one,put=update one,delete=delete one
    path('theme/<int:pk>/', views.ThemeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

]
