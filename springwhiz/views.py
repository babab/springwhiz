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
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from springwhiz.settings import BASE_URL
from springwhiz.notepad.models import Notepad
from springwhiz.tyd.models import TydTask, TydEntry


def _query_handler(request, query):
    if query[0] == '@':
        return _command_handler(request, query[1:])
    elif query[0] == '#':
        return render_to_response('index.html',
                                  {'error': 'Bookmarks are not supported yet',
                                   'query': query},
                                  RequestContext(request))
    else:
        return redirect('https://duckduckgo.com?q=%s' % query)


def _command_handler(request, query):
    if query == 'reg' or query == 'register':
        return redirect(reverse('register'))
    elif query == 'li' or query == 'login':
        return redirect(reverse('login'))
    elif query == 'lo' or query == 'logout':
        return redirect(reverse('logout'))
    elif query == 'np' or query == 'notepad':
        return redirect(reverse('notepad'))
    elif query == 'bm' or query == 'bookmark':
        return render_to_response('index.html',
                                  {'error': 'Bookmarks are not supported yet',
                                   'query': query},
                                  RequestContext(request))
    else:
        return render_to_response('index.html',
                                  {'error': 'Invalid command', 'query': query},
                                  RequestContext(request))


def index(request):
    if request.method == 'POST':
        if 'mode' in request.POST:
            mode = request.POST.get('mode')

        if 'q' in request.POST:
            q = request.POST.get('q')

        if mode == 'bang':
            return _query_handler(request, '!' + q)
        elif mode == 'ddg1st':
            return _query_handler(request, '\\' + q)
        elif mode == 'command':
            return _query_handler(request, '@' + q)
        elif mode == 'bookmark':
            return _query_handler(request, '#' + q)
        else:
            # Normal search or javascript is disabled
            return _query_handler(request, q)

    notes_open = (Notepad.objects.filter(share=2)
                                 .order_by('-last_edited'))
    if request.user.is_active:
        notes_priv = (Notepad.objects.filter(user=request.user)
                      .order_by('-last_edited')[:5])
        notes_open = notes_open.exclude(user=request.user)[:5]
        active_tyd = TydEntry.objects.filter(
            task__project__category__user=request.user, current=True
        )
        tyd_tasks = TydTask.objects.filter(
            project__category__user=request.user
        )
    else:
        notes_priv = {}
        active_tyd = {}
        tyd_tasks = {}

    data = {'notes_priv': notes_priv, 'notes_open': notes_open,
            'active_tyd': active_tyd, 'tyd_tasks': tyd_tasks}
    return render_to_response('index.html', data, RequestContext(request))


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
            messages.error(
                request, 'Passwords do not match, please try again.'
            )
            error += 1

        try:
            forms.EmailField().clean(email)
        except forms.ValidationError:
            messages.error(request, 'Invalid email address.')
            error += 1

        if User.objects.filter(username=username):
            messages.error(request, 'That username already exists.')
            error += 1

        if User.objects.filter(email=email):
            messages.error(request, 'That email address already exists.')
            error += 1

        if not error:
            User.objects.create_user(username, email, password)
            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                messages.success(
                    request, 'You have registered and logged in successfully.'
                )
                login(request, user)

            return redirect(reverse('index'))

    return render_to_response('authenticate.html', data,
                              RequestContext(request))


def login_view(request):
    """Handle logins"""
    data = {'auth_type': 'login'}
    context = RequestContext(request)

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'You have logged in successfully.')
            else:
                messages.error(request, 'Your account is disabled')
            return redirect(reverse('index'))
        else:
            messages.error(request, 'Invalid username or password')

    return render_to_response('authenticate.html', data, context)


def logout_view(request):
    """Handle logging out"""

    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return redirect(BASE_URL)
