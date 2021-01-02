from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        # Return `True` if permission is granted, `False` otherwise.
        # 超级用户可以访问，除了超级用户以外，都不能访问
        if not request.session.get('isLogin', None):
            return False
        else:
            authority = request.session.get('userAuthority', None)
            if authority and authority == "普通用户":
                return True
            else:
                return False


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        # Return `True` if permission is granted, `False` otherwise.
        # 超级用户可以访问，除了超级用户以外，都不能访问
        if not request.session.get('isLogin', None):
            return False
        else:
            authority = request.session.get('userAuthority', None)
            if authority and authority == "管理员":
                return True
            else:
                return False


class SuperAdminPermission(BasePermission):
    def has_permission(self, request, view):
        # Return `True` if permission is granted, `False` otherwise.
        # 超级用户可以访问，除了超级用户以外，都不能访问
        if not request.session.get('isLogin', None):
            return False
        else:
            authority = request.session.get('userAuthority', None)
            if authority and authority == "超级管理员":
                return True
            else:
                return False
