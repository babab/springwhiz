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
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils import timezone

from springwhiz.tyd.models import (
    TydCategory, TydCategoryForm,
    TydProject, TydProjectForm,
    TydTask, TydTaskForm,
    TydEntry,
)


def _getdata(request):
    categories = TydCategory.objects.filter(user=request.user).order_by('name')
    projects = (TydProject.objects.filter(category__user=request.user)
                                  .order_by('category', 'name'))
    tasks = (TydTask.objects.filter(project__category__user=request.user)
                            .order_by('project__category', 'project', 'name'))
    return {'categories': categories, 'projects': projects, 'tasks': tasks}


@login_required
def start(request):
    if request.method == 'POST':
        task_id = request.POST['tydtask']
        task = TydTask.objects.get(
            project__category__user=request.user, pk=task_id
        )
        TydEntry(task=task, current=True).save()

    referer = request.META['HTTP_REFERER']
    if referer:
        return redirect(referer)
    return redirect(reverse('index'))


@login_required
def end(request):
    entry = TydEntry.objects.get(
        task__project__category__user=request.user, current=True
    )
    entry.current = False
    entry.end = timezone.now()
    entry.save()

    referer = request.META['HTTP_REFERER']
    if referer:
        return redirect(referer)
    return redirect(reverse('index'))


@login_required
def index(request):
    entries = TydEntry.objects.filter(
        task__project__category__user=request.user
    ).order_by('-start')[:10]

    dates = {0: datetime.date.today() - datetime.timedelta(days=6),
             1: datetime.date.today() - datetime.timedelta(days=5),
             2: datetime.date.today() - datetime.timedelta(days=4),
             3: datetime.date.today() - datetime.timedelta(days=3),
             4: datetime.date.today() - datetime.timedelta(days=2),
             5: datetime.date.today() - datetime.timedelta(days=1),
             6: datetime.date.today()}
    data = {'entries': entries, 'dates': dates}
    return render_to_response('tyd/index.html', data, RequestContext(request))


@login_required
def manage(request):
    data = _getdata(request)
    project_form = TydProjectForm(prefix='project')
    task_form = TydTaskForm(prefix='task')

    if request.method == 'POST':
        category_form = TydCategoryForm(request.POST)
        if category_form.is_valid():
            if (not category_form.instance.name in
                    [i.name for i in data['categories']]):
                category_form.instance.user = request.user
                category_form.save()
                return redirect(reverse('tyd_index'))
    else:
        category_form = TydCategoryForm(prefix='category')

    data.update({'category_form': category_form,
                 'project_form': project_form,
                 'task_form': task_form})
    return render_to_response('tyd/manage.html', data, RequestContext(request))


@login_required
def project_add(request):
    data = _getdata(request)

    if request.method == 'POST':
        project_form = TydProjectForm(request.POST, prefix='project')
        if project_form.is_valid():
            flt = data['projects'].filter(
                category=project_form.instance.category
            )
            if not project_form.instance.name in [i.name for i in flt]:
                project_form.save()
            return redirect(reverse('tyd_manage'))

        category_form = TydCategoryForm(prefix='category')
        data.update({'category_form': category_form,
                     'project_form': project_form})
        return render_to_response('tyd/manage.html', data,
                                  RequestContext(request))
