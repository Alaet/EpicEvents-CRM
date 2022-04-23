from django.contrib import admin
from django.contrib.auth.models import Group

from contract.models import Contract
from .models import Client


class ContractInline(admin.TabularInline):
    model = Contract
    readonly_fields = ('status', 'sales_contact', 'amount', 'payment_due')


class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "company_name", "sales_contact", "prospect")
    inlines = [ContractInline]
    search_fields = ('company_name', 'email')
    exclude = ('sales_contact',)

    def save_model(self, request, obj, form, change):
        user = request.user
        sales_group = Group.objects.get(name='SalesTeam')
        if request.user.groups == sales_group or request.user .is_superuser:
            obj.sales_contact = user
            obj.save()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if request.user != obj.sales_contact and not request.user.is_superuser:
                return [f.name for f in self.model._meta.fields]
        return super(ClientAdmin, self).get_readonly_fields(
            request, obj=obj
        )

    def get_queryset(self, request):
        queryset = super(ClientAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.groups == Group.objects.get(name='SalesTeam'):
            return queryset.filter(sales_contact=request.user)
        elif request.user.groups == Group.objects.get(name='SupportTeam'):
            return queryset.filter(client_event__support_contact=request.user)


admin.site.register(Client, ClientAdmin)
