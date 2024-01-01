from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic import CreateView
from transactions.constants import DEPOSIT
from transactions.forms import DepositForm
from transactions.models import Transaction
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template, {
        'user': user,
        'amount': amount,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('deposit_money')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user
        # Check if the user has an associated account
        if hasattr(user, 'account'):
            kwargs.update({'account': user.account})
        else:
            # Handle the case where the user has no account
            raise Http404("User has no account.")
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        return context

class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        send_transaction_email(self.request.user, amount, "Deposit Message", "deposit_email.html")
        return super().form_valid(form)
