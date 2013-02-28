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

import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from springwhiz.tyd.models import TydTask, TydEntry


@login_required
def start(request):
    if request.method == 'POST':
        task_id = request.POST['tydtask']
        task = TydTask.objects.get(
            project__category__user=request.user, pk=task_id
        )
        TydEntry(task=task, current=True).save()
    return redirect(reverse('index'))


@login_required
def end(request):
    TydEntry.objects.filter(
        task__project__category__user=request.user, current=True
    ).update(current=False, end=datetime.datetime.now())
    return redirect(reverse('index'))
