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

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms.widgets import TextInput, Select
from django.template.defaultfilters import timesince
from django.utils import timezone

from springwhiz.bases import ModelBase


class TydCategory(ModelBase):
    user = models.ForeignKey(User, editable=False)

    class Meta:
        verbose_name_plural = 'Tyd categories'


class TydProject(ModelBase):
    category = models.ForeignKey('TydCategory', related_name='project')

    def __unicode__(self):
        return '{0} - {1}'.format(self.category, self.name)


class TydTask(ModelBase):
    project = models.ForeignKey('TydProject', related_name='task')

    def __unicode__(self):
        return '{0} - {1}'.format(self.project, self.name)

    class Meta:
        ordering = ['project__category', 'project', 'name']


class TydEntry(models.Model):
    task = models.ForeignKey('TydTask', related_name='entry')
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)
    current = models.BooleanField(default=False)
    seconds = models.IntegerField(default=0)

    def __unicode__(self):
        return ('{0} - {1} - {2} - {3}'
                .format(self.task, self.start, self.end, self.current))

    def duration(self):
        if self.current:
            return timesince(self.start)

        timediff = self.end - self.start
        if timediff.total_seconds() < 60:
            return '%0.0f seconds' % timediff.total_seconds()
        return timesince(timezone.now() - timediff)

    def save(self):
        '''Calculate total number of seconds and update in DB'''
        if self.start:
            self.seconds = (timezone.now() - self.start).total_seconds()
        else:
            self.seconds = 0
        return super(TydEntry, self).save()

    class Meta:
        verbose_name_plural = 'Tyd entries'
        ordering = ['task__project__category', 'task__project',
                    'task', '-start']


class TydCategoryForm(ModelForm):
    class Meta:
        model = TydCategory
        widgets = {
            'name': TextInput(attrs={'class': 'span3',
                                     'placeholder': 'category name'}),
        }


class TydProjectForm(ModelForm):
    class Meta:
        model = TydProject
        widgets = {
            'category': Select(attrs={'class': 'span3'}),
            'name': TextInput(attrs={'class': 'span3',
                                     'placeholder': 'project name'}),
        }


class TydTaskForm(ModelForm):
    class Meta:
        model = TydTask
        widgets = {
            'project': Select(attrs={'class': 'span3'}),
            'name': TextInput(attrs={'class': 'span3',
                                     'placeholder': 'task name'}),
        }
