#This file is part paypalgateway blueprint for Flask.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from flask import Blueprint, request, render_template, flash, current_app, g, \
    abort, url_for, redirect
from flask_babel import gettext as _
from galatea.tryton import tryton
from decimal import Decimal, InvalidOperation
from .forms import PaymentForm

payment = Blueprint('payment', __name__, template_folder='templates')

GALATEA_WEBSITE = current_app.config.get('TRYTON_GALATEA_SITE')
SHOP = current_app.config.get('TRYTON_SALE_SHOP')

Website = tryton.pool.get('galatea.website')
Shop = tryton.pool.get('sale.shop')
Lang = tryton.pool.get('ir.lang')

@payment.route("/", methods=["GET", "POST"], endpoint="payment")
@tryton.transaction()
def payment_form(lang):
    '''Payment Form'''
    # Two steps:
    # 1. Form with amount and reference
    # 2. POST request. Show amount and reference (readonly) and show payment types
    # Finally send form data to virtual payment blueprint (payment type, esale_code)

    shop = Shop(SHOP)
    website = Website(GALATEA_WEBSITE)
    form_action = '.payment'

    payment_types = [(p.payment_type.id, p.payment_type.name)
        for p in shop.esale_payments if p.payment_type.esale_payment]
    if not payment_types:
        abort(404)

    form_payment = PaymentForm()
    form_payment.payment_type.choices = payment_types

    if request.method == 'POST':
        amount = request.form.get('amount')

        try:
            form_payment.amount.data = Decimal(amount)
        except InvalidOperation:
            flash(_('Insert an amount numeric value.'), "danger")
            return redirect(url_for('.payment', lang=g.language))
        except TypeError:
            flash(_('Insert an amount numeric value.'), "danger")
            return redirect(url_for('.payment', lang=g.language))

        form_payment.reference.data = request.form.get('reference')

        if request.form.get('payment_type') and form_payment.amount.data:
            try:
                payment_type_id = int(request.form.get('payment_type'))
            except ValueError:
                flash(_('Select a payment type.'), "danger")
                return redirect(url_for('.payment', lang=g.language))

            form_payment.payment_type.data = payment_type_id
            if not form_payment.validate_on_submit():
                for k, v in form_payment.errors.items():
                    flash('%s: %s' % (getattr(form_payment, k).label.text,
                        ', '.join(v)))
            else:
                for epayment_type in shop.esale_payments:
                    if epayment_type.payment_type.id == payment_type_id:
                        form_action = epayment_type.payment_type.esale_code
                        break

    # Breadcumbs
    breadcrumbs = [{
        'slug': url_for('.payment', lang=g.language),
        'name': _('Payment'),
        }]

    return render_template('payment-payment.html',
            website=website,
            breadcrumbs=breadcrumbs,
            shop=shop,
            form_action=form_action,
            form_payment=form_payment,
            )
