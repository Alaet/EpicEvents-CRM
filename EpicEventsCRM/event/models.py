from django.db.models import Model, CASCADE, ForeignKey, DateTimeField, CharField, SET_NULL, DateField, \
    IntegerField, TextField, OneToOneField

from client.models import Client
from authentication.models import User
from contract.models import Contract


class Event(Model):
    choices = (
        ('UPC', 'UPCOMING'),
        ('RUN', 'RUNNING'),
        ('OVR', 'OVER'),
    )

    client = ForeignKey(Client, on_delete=CASCADE, related_name='client_event')
    date_created = DateTimeField(auto_now_add=True, null=True)
    date_updated = DateTimeField(auto_now=True)
    support_contact = ForeignKey(User, limit_choices_to={'groups__name': 'SupportTeam'}, on_delete=SET_NULL,
                                 related_name='support_contact', null=True)
    event_status = CharField(max_length=50, choices=choices, default='UPC')
    attendees = IntegerField()
    event_date = DateField()
    notes = TextField()
    contract = OneToOneField(Contract, related_name='contract_event', on_delete=CASCADE, null=True)

    def __str__(self):
        return str(self.pk) + " / %s / Event date : %s" % (self.client, self.event_date)
