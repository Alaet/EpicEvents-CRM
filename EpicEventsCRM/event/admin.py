from django.contrib import admin

from client.models import Client
from contract.models import Contract
from event.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "event_status", "event_date", "contract", "client", "support_contact",)
    search_fields = ('client__company_name', 'client__email', 'event_date')

    def get_form(self, request, obj=None, change=False, **kwargs):
        current_user = request.user
        if current_user.team == 'support':
            self.exclude = ('client', 'support_contact',)
            self.list_display = ("id", "event_status", "event_date",)
        form = super(EventAdmin, self).get_form(request, obj, **kwargs)
        if current_user.team != 'support':
            form.base_fields['client'].queryset = Client.objects.filter(sales_contact=current_user.id)
            form.base_fields['contract'].queryset = Contract.objects.filter(sales_contact=current_user.id)
        if current_user.team == 'support':
            form.base_fields['contract'].queryset = Contract.objects.filter(
                contract_event__support_contact=current_user.id)
        if current_user.is_superuser:
            form = super(EventAdmin, self).get_form(request, obj, **kwargs)
        form.current_user = current_user
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if request.user != obj.support_contact \
                    and not request.user.is_superuser and request.user != obj.contract.sales_contact:
                return [f.name for f in self.model._meta.fields]
        return super(EventAdmin, self).get_readonly_fields(
            request, obj=obj
        )

    def get_queryset(self, request):
        queryset = super(EventAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.team == 'sales':
            return queryset.filter(contract__sales_contact=request.user)
        elif request.user.team == 'support':
            return queryset.filter(support_contact=request.user)


admin.site.register(Event, EventAdmin)
