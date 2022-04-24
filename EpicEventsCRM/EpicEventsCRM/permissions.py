from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission

from client.models import Client
from contract.models import Contract
from event.models import Event


class GroupPermissions(BasePermission):
    def has_permission(self, request, view):
        support_group = 'support'
        sales_group = 'sales'
        if request.user.team == support_group or request.user.team == sales_group:
            return True

    def has_object_permission(self, request, view, obj):
        support_group = 'support'
        sales_group = 'sales'
        if request.user.team == support_group or request.user.team == sales_group:
            return True


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.has_perm('client.view_client') \
                or request.user.has_perm('contract.add_contract') \
                or request.user.has_perm('event.add_event') \
                or request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.has_perm('client.view_client'):
            return True


class IsMainContact(BasePermission):
    """
    Check if request.user is creator of an object, based on obj type
    """

    support_group = 'support'

    def has_permission(self, request, view):
        print(request.user.team)
        if request.user.team == self.support_group:
            if request.method in ["POST", "DELETE"]:
                return False
            else:
                return True
        if request.user.has_perm('client.add_client') \
                or request.user.has_perm('contract.add_contract')\
                or request.user.has_perm('event.delete_event')\
                or request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        """
        Grant permissions base on type object in params and request user relation/group to obj
        :return: bool
        """
        sales_group = 'sales'
        if isinstance(obj, Client) or isinstance(obj, Contract):
            if request.user.id == obj.sales_contact.id or request.user.is_superuser:
                return True
            elif isinstance(obj, Client):
                raise ValidationError("Seul l'utilisateur responsable du client (%s) peut le modifier ou le supprimer"
                                      % obj.sales_contact)
            elif isinstance(obj, Contract):
                raise ValidationError(
                    "Seul l'utilisateur responsable du contrat (%s) peut le modifier ou le supprimer" %
                    obj.sales_contact)
        elif isinstance(obj, Event):
            if request.user.id == obj.support_contact.id or request.user.is_superuser \
                    or request.user.team == sales_group:
                return True
            raise ValidationError("Seul l'utilisateur responsable de l'évènement (%s) peut le modifier" %
                                  obj.support_contact)
