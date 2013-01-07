# Copyright (C) 2012-2013  Benjamin Althues
#
# This file is part of springwhiz.
#
# springwhiz is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# springwhiz is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with springwhiz.  If not, see <http://www.gnu.org/licenses/>.

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from springwhiz.settings import BASE_URL


def help(request):
    return render_to_response('help.html', {}, RequestContext(request))


def register(request):
    """Create new user from authenticate form"""

    data = {'auth_type': 'register'}

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        error = 0

        if password != password2:
            data.update(
                {'message': 'Passwords do not match, please try again.',
                 'msg_type': 'error'}
            )
            error += 1

        try:
            forms.EmailField().clean(email)
        except forms.ValidationError:
            data.update({'message': 'Invalid email address',
                         'msg_type': 'error'})
            error += 1

        if User.objects.filter(username=username):
            data.update({'message': 'That username already exists.',
                         'msg_type': 'error'})
            error += 1

        if User.objects.filter(email=email):
            data.update({'message': 'That email address already exists.',
                         'msg_type': 'error'})
            error += 1

        if not error:
            User.objects.create_user(username, email, password)
            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)

            return redirect(BASE_URL)

    context = RequestContext(request)
    return render_to_response('authenticate.html', data, context)


def login_view(request):
    """Handle logins"""

    data = {'auth_type': 'login'}

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                data.update({'message': 'You have logged in succesfully',
                             'msg_type': 'success'})
            else:
                data.update({'message': 'Your account is disabled',
                             'msg_type': 'error'})
        else:
            data.update({'message': 'Invalid username or password',
                         'msg_type': 'error'})
            context = RequestContext(request)
            return render_to_response('authenticate.html', data, context)

        context = RequestContext(request)
        return render_to_response('start/index.html', data, context)

    context = RequestContext(request)
    return render_to_response('authenticate.html', data, context)


def logout_view(request):
    """Handle logging out"""

    logout(request)
    return redirect(BASE_URL)
