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
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView

from models import Notepad, NotepadForm
from string_generator import stringGenerator


def notepad(request):
    if request.user.is_active:
        return redirect(reverse('notepad_create'))
    else:
        return redirect(reverse('notepad_list'))


def detail(request, idhash):
    hashlen = len(idhash)

    if hashlen == 5:
        note = get_object_or_404(Notepad, shorthash=idhash)
        if note.share != 2:
            if not request.user.is_active:
                raise Http404
            elif note.user.pk != request.user.pk:
                raise Http404
    elif hashlen == 20:
        note = get_object_or_404(Notepad, longhash=idhash)
        if note.share == 0:
            if not request.user.is_active:
                raise Http404
            elif note.user.pk != request.user.pk:
                raise Http404
    else:
        raise Http404

    data = {'note': note}

    context = RequestContext(request)
    return render_to_response('notepad/notepad-detail.html', data, context)


def detail_raw(request, idhash):
    hashlen = len(idhash)

    if hashlen == 5:
        note = get_object_or_404(Notepad, shorthash=idhash)
        if note.share != 2:
            if not request.user.is_active:
                raise Http404
            elif note.user.pk != request.user.pk:
                raise Http404
    elif hashlen == 20:
        note = get_object_or_404(Notepad, longhash=idhash)
        if note.share == 0:
            if not request.user.is_active:
                raise Http404
            elif note.user.pk != request.user.pk:
                raise Http404
    else:
        raise Http404

    return HttpResponse(note.text, mimetype='text/plain')


def detail_rendered(request, idhash):
    hashlen = len(idhash)

    if hashlen == 5:
        note = get_object_or_404(Notepad, shorthash=idhash)
        if note.share != 2:
            if not request.user.is_active:
                raise Http404
            elif note.user.pk != request.user.pk:
                raise Http404
    elif hashlen == 20:
        note = get_object_or_404(Notepad, longhash=idhash)
        if note.share == 0:
            if not request.user.is_active:
                raise Http404
            elif note.user.pk != request.user.pk:
                raise Http404
    else:
        raise Http404

    data = {'note': note}

    context = RequestContext(request)
    return render_to_response('notepad/notepad-rendered.html', data, context)


def list(request):
    notes_open = (Notepad.objects.filter(share=2)
                                 .order_by('-last_edited'))
    if request.user.is_active:
        notes_priv = (Notepad.objects.filter(user=request.user)
                                     .order_by('-last_edited'))
        notes_open = notes_open.exclude(user=request.user)
    else:
        notes_priv = {}
    data = {'notes_priv': notes_priv,
            'notes_open': notes_open}

    context = RequestContext(request)
    return render_to_response('notepad/notepad-list.html', data, context)


class NotepadCreate(CreateView):
    model = Notepad
    form_class = NotepadForm
    template_name = 'notepad/notepad.html'

    def get_success_url(self):
        return reverse('notepad_list')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.pk
        form.instance.last_edited = datetime.datetime.now()

        # TODO: Make sure hashes are unique
        form.instance.shorthash = stringGenerator(5)
        form.instance.longhash = stringGenerator(20)
        return super(NotepadCreate, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NotepadCreate, self).dispatch(*args, **kwargs)


class NotepadUpdate(UpdateView):
    model = Notepad
    form_class = NotepadForm
    template_name = 'notepad/notepad-edit.html'

    def get_success_url(self):
        return reverse('notepad_update',
                       kwargs={'idhash': self.kwargs['idhash']})

    def get_object(self):
        kwargs = {'shorthash': self.kwargs['idhash']}
        obj = get_object_or_404(self.model, **kwargs)

        if obj.user != self.request.user:
            raise Http404
        return obj

    def form_valid(self, form):
        instance = self.get_object()
        form.instance.user_id = self.request.user
        form.instance.last_edited = datetime.datetime.now()
        form.instance.shorthash = instance.shorthash
        form.instance.longhash = instance.longhash
        return super(NotepadUpdate, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NotepadUpdate, self).dispatch(*args, **kwargs)


class NotepadDelete(DeleteView):
    model = Notepad
    template_name = 'notepad/notepad-delete.html'
    context_object_name = 'note'

    def get_success_url(self):
        return reverse('notepad_list')

    def get_object(self):
        kwargs = {'shorthash': self.kwargs['idhash']}
        obj = get_object_or_404(self.model, **kwargs)

        if obj.user != self.request.user:
            raise Http404
        return obj

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NotepadDelete, self).dispatch(*args, **kwargs)
