from rest_framework.permissions import BasePermission


class OnlyOrderOfUser(BasePermission):
    message = "You can't view results of other users"

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id
