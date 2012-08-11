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

from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

def query_handler(query):
    return redirect('https://duckduckgo.com?q=%s' % query)

def index(request):
    data = {}

    if request.POST:
        if request.POST.has_key('mode'):
            mode = request.POST.get('mode')

        if request.POST.has_key('q'):
            q = request.POST.get('q')

        if mode == 'unset':
            return query_handler(q)
        elif mode == 'bang':
            return query_handler('!' + q)
        elif mode == 'ddg1st':
            return query_handler('\\' + q)
        else:
            data = {'mode': mode, 'query': q}

    context = RequestContext(request)
    return render_to_response('start/index.html', data, context)
