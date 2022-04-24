from django.db.models import Model, ForeignKey, DateTimeField, SET_NULL, DateField, \
    BooleanField, FloatField

from authentication.models import User
from client.models import Client


class Contract(Model):

    sales_contact = ForeignKey(User, limit_choices_to={'team': 'sales'}, on_delete=SET_NULL,
                               related_name='sales_contact_contract', null=True)
    client = ForeignKey(Client, on_delete=SET_NULL, related_name='client_contract', null=True)
    date_created = DateTimeField(auto_now_add=True, null=True)
    date_updated = DateTimeField(auto_now=True)
    status = BooleanField(default=False, help_text='Contrat actif')
    amount = FloatField()
    payment_due = DateField()

    def __str__(self):
        return str(self.pk) + " / %s / Echéance : %s " % (self.client, self.payment_due)
