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
from django.forms.widgets import TextInput

from springwhiz.bases import ModelBase


class TydCategory(ModelBase):
    user = models.ForeignKey(User, editable=False)

    class Meta:
        verbose_name_plural = 'Tyd categories'


class TydProject(ModelBase):
    category = models.ForeignKey('TydCategory')


class TydTask(ModelBase):
    project = models.ForeignKey('TydProject')

    def __unicode__(self):
        return '{0} - {1}'.format(self.project, self.name)


class TydEntry(models.Model):
    task = models.ForeignKey('TydTask')
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)
    current = models.BooleanField(default=False)

    def __unicode__(self):
        return ('{0} - {1} - {2} - {3}'
                .format(self.task, self.start, self.end, self.current))

    class Meta:
        verbose_name_plural = 'Tyd entries'


class TydCategoryForm(ModelForm):
    class Meta:
        model = TydCategory
        widgets = {
            'name': TextInput(attrs={'class': 'span2',
                                     'placeholder': 'category name'}),
        }


class TydProjectForm(ModelForm):
    class Meta:
        model = TydProject


class TydTaskForm(ModelForm):
    class Meta:
        model = TydTask
