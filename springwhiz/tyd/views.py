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
from django.db.models import Sum
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
    tyd_categories = (TydCategory.objects.filter(user=request.user)
                                 .order_by('name')
                                 .annotate(seconds=Sum(
                                     'project__task__entry__seconds')))
    tyd_projects = (TydProject.objects.filter(category__user=request.user)
                              .order_by('name')
                              .annotate(seconds=Sum(
                                  'task__entry__seconds')))

    tyd_tasks = TydTask.objects.filter(
        project__category__user=request.user
    ).annotate(seconds=Sum('entry__seconds'))

    tyd_entries = TydEntry.objects.filter(
        task__project__category__user=request.user
    ).order_by('-start')[:10]

    active_tyd = TydEntry.objects.filter(
        task__project__category__user=request.user, current=True
    )

    data = {'active_tyd': active_tyd,
            'tyd_categories': tyd_categories,
            'tyd_entries': tyd_entries,
            'tyd_projects': tyd_projects,
            'tyd_tasks': tyd_tasks}
    return render_to_response('tyd/index.html', data, RequestContext(request))


@login_required
def manage(request):
    data = _getdata(request)

    if request.method == 'POST':
        if 'category_submit' in request.POST:
            category_form = TydCategoryForm(request.POST, prefix='category')
            if category_form.is_valid():
                if (not category_form.instance.name in
                        [i.name for i in data['categories']]):
                    category_form.instance.user = request.user
                    category_form.save()
                    return redirect(reverse('tyd_manage'))
            project_form = TydProjectForm(prefix='project')
            task_form = TydTaskForm(prefix='task')
        elif 'project_submit' in request.POST:
            project_form = TydProjectForm(request.POST, prefix='project')
            if project_form.is_valid():
                flt = data['projects'].filter(
                    category=project_form.instance.category
                )
                if not project_form.instance.name in [i.name for i in flt]:
                    project_form.save()
                return redirect(reverse('tyd_manage'))
            category_form = TydCategoryForm(prefix='category')
            task_form = TydTaskForm(prefix='task')
        elif 'task_submit' in request.POST:
            task_form = TydTaskForm(request.POST, prefix='task')
            if task_form.is_valid():
                flt = data['tasks'].filter(
                    project=task_form.instance.project
                )
                if not task_form.instance.name in [i.name for i in flt]:
                    task_form.save()
                return redirect(reverse('tyd_manage'))
            category_form = TydCategoryForm(prefix='category')
            project_form = TydProjectForm(prefix='project')
    else:
        category_form = TydCategoryForm(prefix='category')
        project_form = TydProjectForm(prefix='project')
        task_form = TydTaskForm(prefix='task')

    data.update({'category_form': category_form,
                 'project_form': project_form,
                 'task_form': task_form})
    return render_to_response('tyd/manage.html', data, RequestContext(request))
