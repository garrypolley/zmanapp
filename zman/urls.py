# -*- coding: utf-8 -*-

from .views import error
from .views import logout
from .views import AuthHomeView
from .views import PayZmanView
from .views import OweZmanView
from .views import UnAuthHomeView
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^/?$', UnAuthHomeView.as_view(), name='home'),
    url(r'^error/?$', error, name='error'),
    url(r'^logout/?$', logout, name='logout'),
    url(r'^admit-zman/?$', OweZmanView.as_view(), name='owe_zman'),
    url(r'^repay-zman/?$', PayZmanView.as_view(), name='pay_zman'),
    url(r'^repay-zman/(?P<username>[-\w]+)/?$', PayZmanView.as_view(), name='pay_zman'),
    url(r'^home/?$', AuthHomeView.as_view(), name='auth_user_home'),
    url(r'', include('social_auth.urls')),
)
