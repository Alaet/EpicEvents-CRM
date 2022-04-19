from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission

from client.models import Client
from contract.models import Contract
from event.models import Event


class GroupPermissions(BasePermission):
    def has_permission(self, request, view):
        support_group = Group.objects.get(name="SupportTeam")
        sales_group = Group.objects.get(name="SalesTeam")
        if request.user.groups == support_group or request.user.groups == sales_group:
            return True

    def has_object_permission(self, request, view, obj):
        support_group = Group.objects.get(name="SupportTeam")
        sales_group = Group.objects.get(name="SalesTeam")
        if request.user.groups == support_group or request.user.groups == sales_group:
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
    try:
        support_group = Group.objects.get(name="SupportTeam")
    except ObjectDoesNotExist:
        support_group = None

    def has_permission(self, request, view):
        if request.user.groups == self.support_group:
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
        sales_group = Group.objects.get(name="SalesTeam")
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
                    or request.user.groups == sales_group:
                print("LOLOLOL")
                return True
            raise ValidationError("Seul l'utilisateur responsable de l'évènement (%s) peut le modifier" %
                                  obj.support_contact)
