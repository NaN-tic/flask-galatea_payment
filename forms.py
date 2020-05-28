from flask_babel import lazy_gettext
from flask_wtf import Form
from wtforms import TextField, RadioField, validators
from wtforms.fields.html5 import DecimalField


class PaymentForm(Form):
    '''Payment form'''
    amount = DecimalField(lazy_gettext('Amount'), [validators.Required()])
    reference = TextField(lazy_gettext('Reference'))
    payment_type = RadioField(lazy_gettext('Payment Type'), [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def reset(self):
        self.amount.data = ''
        self.reference.data = ''
