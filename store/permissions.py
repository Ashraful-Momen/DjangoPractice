from rest_framework import permissions



class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: #in safe methods has=> GET, HEAD, OPTIONS.
            return True
        return bool(request.user and request.user.is_staff)




class FullDjangoModelPermission(permissions.DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map['GET']:  ['%(app_label)s.view_%(model_name)s'] #only get is we allow here . though user have all permessions but only get permission we just provid.


#custom django model permission: 

class ViewCustomerModelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')   