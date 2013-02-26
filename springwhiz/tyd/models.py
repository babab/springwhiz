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


class ModelBase(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class MainCategory(ModelBase):
    user = models.ForeignKey(User)


class Project(ModelBase):
    main_category = models.ForeignKey('MainCategory')

    def __unicode__(self):
        return '{} - {}'.format(self.main_category, self.name)


class Task(ModelBase):
    project = models.ForeignKey('Project')

    def __unicode__(self):
        return '{} - {}'.format(self.project, self.name)


class Entry(models.Model):
    task = models.ForeignKey('Task')
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)
    current = models.BooleanField(default=False)

    def __unicode__(self):
        return '{} - {} - {} - {}'.format(self.task, self.start, self.end,
                                          self.current)
