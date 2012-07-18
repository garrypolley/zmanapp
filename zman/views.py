# -*- coding: utf-8 -*-


from .forms import ZmanForm
from .models import OwedItem
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.contrib.messages.api import get_messages
from django.utils.translation import ugettext as _


class OweZmanView(FormView):
    form_class = ZmanForm
    template_name = "owe_zman.html"
    success_url = reverse_lazy("home")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return FormView.dispatch(self, request, *args, **kwargs)

    def get_initial(self):
        """Sets amount equal to 1 for form default"""
        initial_args = self.initial.copy()
        initial_args['amount'] = 1
        return initial_args

    def form_valid(self, form):
        # Currently defaults to a zman
        OwedItem.ensure_owed_item(form.cleaned_data['owed_username'],
                                  self.request.user.username,
                                  'zman', form.cleaned_data['amount'])
        return super(OweZmanView, self).form_valid(form)


class PayZmanView(FormView):
    form_class = ZmanForm
    template_name = "pay_zman.html"
    success_url = reverse_lazy("home")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return FormView.dispatch(self, request, *args, **kwargs)

    def get_initial(self):
        """Used to get the username if the form is going to be paid"""
        initial_args = self.initial.copy()
        if 'username' in self.kwargs:
            initial_args['owed_username'] = self.kwargs.get('username')
        initial_args['amount'] = 1
        return initial_args

    def form_valid(self, form):
        # Remove the given debt
        debt_paid = OwedItem.ensure_paid_item(form.cleaned_data.get('owed_username', None),
                                              self.request.user.username,
                                              'zman', form.cleaned_data.get('amount', None))
        if debt_paid:
            return super(PayZmanView, self).form_valid(form)

        form._errors['owed_username'] = form.error_class([_("You do not owe @{0} any zmans.").format(form.cleaned_data.get('owed_username', ''))])
        if 'owed_username' in form.cleaned_data:
            del form.cleaned_data['owed_username']
        return self.form_invalid(form)


class AuthHomeView(TemplateView):
    template_name = "auth_home.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return TemplateView.dispatch(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        context['zmans_gotten'] = OwedItem.total_getting_count(self.request.user.username)
        context['gotten_zmans'] = OwedItem.to_get(self.request.user.username, 'zman')
        context['zmans_owed'] = OwedItem.total_to_give_count(self.request.user.username)
        context['owed_zmans'] = OwedItem.to_give(self.request.user.username, 'zman')
        return context


class UnAuthHomeView(TemplateView):
    template_name = "unauth_home.html"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('auth_user_home'))
        return super(UnAuthHomeView, self).get(*args, **kwargs)


def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'messages': messages},
                              RequestContext(request))


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect(reverse('home'))
