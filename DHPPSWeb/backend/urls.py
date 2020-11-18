from django.urls import path, include
from rest_framework.routers import DefaultRouter

from backend import views


router = DefaultRouter()
router.register('AccountInfos', views.AccountViewSet)

urlpatterns = [
    # 渲染首页，其后的页面跳转由前端负责
    path('', views.index, name="index"),
    path('accountInfo/', views.AccountViewSet.as_view({'get': 'list'}))
]
