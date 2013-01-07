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

from django.conf.urls import patterns, include, url
from django.contrib import admin

from notepad.views import NotepadCreate, NotepadUpdate, NotepadDelete

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', include('start.urls')),
    url(r'^notepad/$', 'notepad.views.notepad', name='notepad'),
    url(r'^notepad/new/$', NotepadCreate.as_view(), name='notepad_new'),
    url(r'^notepad/list/$', 'notepad.views.list', name='notepad_list'),
    url(r'^notepad/(?P<idhash>\w+)/$', 'notepad.views.detail',
        name='note_detail'),
    url(r'^notepad/(?P<idhash>\w+)/raw/$', 'notepad.views.detail_raw',
        name='note_detail_raw'),
    url(r'^notepad/(?P<idhash>\w+)/edit/$', NotepadUpdate.as_view(),
        name='note_edit'),
    url(r'^notepad/(?P<idhash>\w+)/delete/$', NotepadDelete.as_view(),
        name='note_delete'),
    url(r'^help/$', 'springwhiz.views.help', name='help'),
    url(r'^register/$', 'springwhiz.views.register', name='register'),
    url(r'^login/$', 'springwhiz.views.login_view', name='login_view'),
    url(r'^logout/$', 'springwhiz.views.logout_view', name='logout_view'),
    url(r'^admin/', include(admin.site.urls)),
)
