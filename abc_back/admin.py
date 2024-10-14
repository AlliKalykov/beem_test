

class SuperUserModuleMixin:

    def has_module_permission(self, request):
        return request.user.is_superuser
