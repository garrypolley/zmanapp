# -*- coding: utf-8 -*-

from social_auth.models import User


def username(request, *args, **kwargs):
    if kwargs.get('user'):
        username = kwargs['user'].username
    else:
        username = request.session.get('saved_username')
    return {'username': username}


def create_user(backend, details, response, uid, username, user=None, *args,
                **kwargs):
    """Create user. Depends on get_username pipeline."""
    if user:
        return {'user': user}
    if not 'username' in details:
        return None

    email = details.get('email').lower()
    new_username = details.get('username').lower()
    return {
        'user': User.objects.create_user(username=new_username, email=email),
        'is_new': True
    }
