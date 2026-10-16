from rest_framework.permissions import BasePermission

AGENT_GROUP = "agente"


class AgentPermission(BasePermission):


    def has_permission(self, request, view):
        return True
