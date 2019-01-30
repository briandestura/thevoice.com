from rest_framework import permissions


class CanViewTeamData(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'admin') or hasattr(request.user, 'mentor'):
            return True
        return False