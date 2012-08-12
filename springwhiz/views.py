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

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.template import RequestContext

def login_view(request):
    """Handle logins"""

    data = {}

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                data = {'message': 'You have logged in succesfully',
                        'msg_type': 'message'}
            else:
                data = {'message': 'Your account is disabled',
                        'msg_type': 'error'}
        else:
            data = {'message': 'Invalid username or password',
                    'msg_type': 'error'}
            context = RequestContext(request)
            return render_to_response('authenticate.html', data, context)

        context = RequestContext(request)
        return render_to_response('start/index.html', data, context)

    context = RequestContext(request)
    return render_to_response('authenticate.html', data, context)

def logout_view(request):
    """Handle logging out"""

    logout(request)
    data = {'message': 'You have logged out succesfully',
            'msg_type': 'message'}
    context = RequestContext(request)
    return render_to_response('start/index.html', data, context)
