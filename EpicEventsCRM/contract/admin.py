from django.contrib import admin

from client.models import Client
from event.models import Event

from .models import Contract


class EventInline(admin.TabularInline):
    model = Event
    readonly_fields = ('client', 'support_contact', 'event_status', 'attendees', 'event_date', 'notes')


class ContractAdmin(admin.ModelAdmin):

    list_display = ('id', 'status', 'sales_contact', 'client')
    inlines = [EventInline]
    search_fields = ('id', 'client__company_name', 'client__email', 'date_created', 'amount')
    exclude = ('sales_contact',)

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        context['adminform'].form.fields['client'].queryset = Client.objects.filter(sales_contact=request.user.id)
        return super(ContractAdmin, self).render_change_form(request, context)

    def save_model(self, request, obj, form, change):
        user = request.user
        sales_group = 'sales'
        if request.user.team == sales_group or request.user .is_superuser:
            obj.sales_contact = user
            obj.save()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if request.user != obj.sales_contact and not request.user.is_superuser:
                return [f.name for f in self.model._meta.fields]
        return super(ContractAdmin, self).get_readonly_fields(
            request, obj=obj
        )

    def get_queryset(self, request):
        queryset = super(ContractAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(sales_contact=request.user)


admin.site.register(Contract, ContractAdmin)
