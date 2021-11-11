from flask_babel import lazy_gettext
from flask_wtf import FlaskForm as Form
from wtforms import StringField, RadioField, validators, DecimalField


class PaymentForm(Form):
    '''Payment form'''
    amount = DecimalField(lazy_gettext('Amount'), [validators.InputRequired()])
    reference = StringField(lazy_gettext('Reference'))
    payment_type = RadioField(lazy_gettext('Payment Type'), [validators.InputRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def reset(self):
        self.amount.data = ''
        self.reference.data = ''
