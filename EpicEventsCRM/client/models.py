from django.db.models import Model, ForeignKey, DateTimeField, CharField, SET_NULL, \
     EmailField, BooleanField

from authentication.models import User


class Client(Model):

    first_name = CharField(max_length=25, null=True)
    last_name = CharField(max_length=25, null=True)
    email = EmailField(max_length=100, null=True)
    phone = CharField(max_length=20, null=True)
    mobile = CharField(max_length=20, null=True)
    company_name = CharField(max_length=250, unique=True, null=True)
    date_created = DateTimeField(auto_now_add=True, null=True)
    date_updated = DateTimeField(auto_now=True)
    sales_contact = ForeignKey(User, limit_choices_to={'team': 'sales'}, on_delete=SET_NULL,
                               related_name='sales_contact', null=True)
    prospect = BooleanField(default=True)

    def __str__(self):
        if self.company_name:
            return self.company_name
        else:
            return "A DEFINIR"
