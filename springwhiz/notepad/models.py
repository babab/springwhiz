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

from pygments import highlight
from pygments.lexers import get_lexer_by_name, ClassNotFound
from pygments.formatters import HtmlFormatter

from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms.widgets import TextInput, Select, Textarea

from string_generator import stringGenerator


class Notepad(models.Model):
    LANGUAGES = (
        ('', (
            (u'txt', u'Plain text'),
            (u'html', u'HTML'),
            (u'markdown', u'Markdown'),
            (u'rst', u'reStructuredText'))),
        (u'languages', (
            (u'ada', u'Ada'),
            (u'c', u'C'),
            (u'c#', u'C#'),
            (u'c++', u'C++'),
            (u'diff', u'Diff'),
            (u'elisp', u'Emacs Lisp'),
            (u'erlang', u'Erlang'),
            (u'haskell', u'Haskell'),
            (u'javascript', u'Javascript'),
            (u'java', u'Java'),
            (u'lua', u'Lua'),
            (u'objective-c', u'Objectice-C'),
            (u'perl', u'Perl'),
            (u'php', u'PHP'),
            (u'python', u'Python'),
            (u'ruby', u'Ruby'),
            (u'scheme', u'Scheme'),
            (u'shell', u'Shell script'),
            (u'sql', u'SQL'),
            (u'vim', u'Vimscript'),
            (u'xml', u'XML')))
    )
    SHARE_OPTIONS = (
        (0, u'Private / Not shared'),
        (1, u'Shared using private link'),
        (2, u'Open / Viewable for everyone'),
    )

    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=20, choices=LANGUAGES,
                                default=u'txt')
    text = models.TextField()
    text_highlighted = models.TextField()
    last_edited = models.DateTimeField(default=datetime.datetime.now())
    shorthash = models.CharField(max_length=5, unique=True,
                                 default=stringGenerator(5))
    longhash = models.CharField(max_length=20, unique=True,
                                default=stringGenerator(20))
    share = models.SmallIntegerField(choices=SHARE_OPTIONS, default=0)

    def save(self):
        try:
            lexer = get_lexer_by_name(self.language, stripall=True)
        except ClassNotFound:
            lexer = get_lexer_by_name('text', stripall=True)
        formatter = HtmlFormatter(linenos=True, cssclass="syntaxhl")
        self.text_highlighted = highlight(self.text, lexer, formatter)
        super(Notepad, self).save()

    def __unicode__(self):
        return '%s - %s' % (self.user, self.name)


class NotepadForm(ModelForm):
    class Meta:
        model = Notepad
        fields = ('name', 'language', 'share', 'text')
        widgets = {
            'name': TextInput(attrs={'class': 'span5',
                                     'placeholder': 'name of note'}),
            'language': Select(attrs={'class': 'span3'}),
            'share': Select(attrs={'class': 'span3'}),
            'text': Textarea(attrs={'class': 'span12', 'rows': 24,
                                    'placeholder': 'note'}),
        }
