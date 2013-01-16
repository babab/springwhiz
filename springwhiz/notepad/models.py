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
        ('text', 'Plain text'),
        ('Renderable', (
            ('markdown', 'Markdown'),
            ('restructuredtext', 'reStructuredText'))),
        ('Popular', (
            ('apacheconf', 'ApacheConf'),
            ('bash', 'Bash'),
            ('bat', 'Batchfile'),
            ('c', 'C'),
            ('cpp', 'C++'),
            ('common-lisp', 'Common Lisp'),
            ('console', 'Bash Session'),
            ('csharp', 'C#'),
            ('css', 'CSS'),
            ('diff', 'Diff'),
            ('django', 'Django/Jinja'),
            ('go', 'Go'),
            ('html', 'HTML'),
            ('irc', 'IRC logs'),
            ('java', 'Java'),
            ('js', 'JavaScript'),
            ('make', 'Makefile'),
            ('perl', 'Perl'),
            ('php', 'PHP'),
            ('python', 'Python 2'),
            ('pytb', 'Python 2 Traceback'),
            ('python3', 'Python 3'),
            ('py3tb', 'Python 3 Traceback'),
            ('pycon', 'Python console session'),
            ('sql', 'SQL'),
            ('vim', 'Vim Script'))),
        ('Other', (
            ('abap', 'ABAP'),
            ('ada', 'Ada'),
            ('ahk', 'autohotkey'),
            ('antlr', 'ANTLR'),
            ('antlr-as', 'ANTLR With ActionScript Target'),
            ('antlr-cpp', 'ANTLR With CPP Target'),
            ('antlr-csharp', 'ANTLR With C# Target'),
            ('antlr-java', 'ANTLR With Java Target'),
            ('antlr-objc', 'ANTLR With ObjectiveC Target'),
            ('antlr-perl', 'ANTLR With Perl Target'),
            ('antlr-python', 'ANTLR With Python Target'),
            ('antlr-ruby', 'ANTLR With Ruby Target'),
            ('applescript', 'AppleScript'),
            ('as3', 'ActionScript 3'),
            ('as', 'ActionScript'),
            ('aspx-cs', 'aspx-cs'),
            ('aspx-vb', 'aspx-vb'),
            ('asy', 'Asymptote'),
            ('awk', 'Awk'),
            ('basemake', 'Base Makefile'),
            ('bbcode', 'BBCode'),
            ('befunge', 'Befunge'),
            ('blitzmax', 'BlitzMax'),
            ('boo', 'Boo'),
            ('brainfuck', 'Brainfuck'),
            ('bro', 'Bro'),
            ('cfengine3', 'CFEngine3'),
            ('cfm', 'Coldfusion HTML'),
            ('cfs', 'cfstatement'),
            ('cheetah', 'Cheetah'),
            ('clojure', 'Clojure'),
            ('cmake', 'CMake'),
            ('c-objdump', 'c-objdump'),
            ('coffee-script', 'CoffeeScript'),
            ('control', 'Debian Control file'),
            ('coq', 'Coq'),
            ('cpp-objdump', 'C++ object dump'),
            ('css+django', 'CSS + Django/Jinja'),
            ('css+erb', 'CSS + Ruby'),
            ('css+genshitext', 'CSS + Genshi Text'),
            ('css+mako', 'CSS + Mako'),
            ('css+myghty', 'CSS + Myghty'),
            ('css+php', 'CSS + PHP'),
            ('css+smarty', 'CSS + Smarty'),
            ('cython', 'Cython'),
            ('dart', 'Dart'),
            ('d', 'D'),
            ('delphi', 'Delphi'),
            ('d-objdump', 'd-objdump'),
            ('dpatch', 'Darcs Patch'),
            ('dtd', 'DTD'),
            ('duel', 'Duel'),
            ('dylan', 'Dylan'),
            ('ec', 'eC'),
            ('ecl', 'ECL'),
            ('elixir', 'Elixir'),
            ('erb', 'ERB'),
            ('erlang', 'Erlang'),
            ('erl', 'Erlang erl session'),
            ('evoque', 'Evoque'),
            ('factor', 'Factor'),
            ('fancy', 'Fancy'),
            ('fan', 'Fantom'),
            ('felix', 'Felix'),
            ('fortran', 'Fortran'),
            ('fsharp', 'FSharp'),
            ('gas', 'GAS'),
            ('genshi', 'Genshi'),
            ('genshitext', 'Genshi Text'),
            ('glsl', 'GLSL'),
            ('gnuplot', 'Gnuplot'),
            ('gooddata-cl', 'GoodData-CL'),
            ('gosu', 'Gosu'),
            ('groff', 'Groff'),
            ('groovy', 'Groovy'),
            ('gst', 'Gosu Template'),
            ('haml', 'Haml'),
            ('haskell', 'Haskell'),
            ('html+cheetah', 'HTML + Cheetah'),
            ('html+django', 'HTML + Django/Jinja'),
            ('html+evoque', 'HTML + Evoque'),
            ('html+genshi', 'HTML + Genshi'),
            ('html+mako', 'HTML + Mako'),
            ('html+mako', 'HTML + Mako'),
            ('html+myghty', 'HTML + Myghty'),
            ('html+php', 'HTML + PHP'),
            ('html+smarty', 'HTML + Smarty'),
            ('html+velocity', 'HTML + Velocity'),
            ('http', 'HTTP'),
            ('hx', 'haXe'),
            ('hybris', 'Hybris'),
            ('iex', 'Elixir iex session'),
            ('ini', 'INI'),
            ('io', 'Io'),
            ('ioke', 'Ioke'),
            ('jade', 'Jade'),
            ('js+cheetah', 'JavaScript + Cheetah'),
            ('js+django', 'JavaScript + Django/Jinja'),
            ('js+erb', 'JavaScript + Ruby'),
            ('js+genshitext', 'JavaScript + Genshi Text'),
            ('js+mako', 'JavaScript + Mako'),
            ('js+mako', 'JavaScript + Mako'),
            ('js+myghty', 'JavaScript + Myghty'),
            ('json', 'JSON'),
            ('js+php', 'JavaScript + PHP'),
            ('jsp', 'Java Server Page'),
            ('js+smarty', 'JavaScript + Smarty'),
            ('kotlin', 'Kotlin'),
            ('lhs', 'Literate Haskell'),
            ('lighty', 'Lighttpd configuration file'),
            ('llvm', 'LLVM'),
            ('logtalk', 'Logtalk'),
            ('lua', 'Lua'),
            ('mako', 'Mako'),
            ('mako', 'Mako'),
            ('maql', 'MAQL'),
            ('mason', 'Mason'),
            ('matlab', 'Matlab'),
            ('matlabsession', 'Matlab session'),
            ('minid', 'MiniD'),
            ('modelica', 'Modelica'),
            ('modula2', 'Modula-2'),
            ('moocode', 'MOOCode'),
            ('moon', 'MoonScript'),
            ('mupad', 'MuPAD'),
            ('mxml', 'MXML'),
            ('myghty', 'Myghty'),
            ('mysql', 'MySQL'),
            ('nasm', 'NASM'),
            ('nemerle', 'Nemerle'),
            ('newlisp', 'NewLisp'),
            ('newspeak', 'Newspeak'),
            ('nginx', 'Nginx configuration file'),
            ('nimrod', 'Nimrod'),
            ('numpy', 'NumPy'),
            ('objdump', 'objdump'),
            ('objective-c', 'Objective-C'),
            ('objective-j', 'Objective-J'),
            ('ocaml', 'OCaml'),
            ('octave', 'Octave'),
            ('ooc', 'Ooc'),
            ('opa', 'Opa'),
            ('openedge', 'OpenEdge ABL'),
            ('plpgsql', 'PL/pgSQL'),
            ('postgresql', 'PostgreSQL SQL dialect'),
            ('postscript', 'PostScript'),
            ('pot', 'Gettext Catalog'),
            ('pov', 'POVRay'),
            ('powershell', 'PowerShell'),
            ('prolog', 'Prolog'),
            ('properties', 'Properties'),
            ('protobuf', 'Protocol Buffer'),
            ('psql', 'PostgreSQL console (psql)'),
            ('pypylog', 'PyPy Log'),
            ('ragel-cpp', 'Ragel in CPP Host'),
            ('ragel-c', 'Ragel in C Host'),
            ('ragel-d', 'Ragel in D Host'),
            ('ragel-em', 'Embedded Ragel'),
            ('ragel-java', 'Ragel in Java Host'),
            ('ragel-objc', 'Ragel in Objective C Host'),
            ('ragel', 'Ragel'),
            ('ragel-ruby', 'Ragel in Ruby Host'),
            ('rbcon', 'Ruby irb session'),
            ('rb', 'Ruby'),
            ('rconsole', 'RConsole'),
            ('rebol', 'REBOL'),
            ('redcode', 'Redcode'),
            ('rhtml', 'RHTML'),
            ('sass', 'Sass'),
            ('scala', 'Scala'),
            ('scaml', 'Scaml'),
            ('scheme', 'Scheme'),
            ('scilab', 'Scilab'),
            ('scss', 'SCSS'),
            ('smalltalk', 'Smalltalk'),
            ('smarty', 'Smarty'),
            ('sml', 'Standard ML'),
            ('snobol', 'Snobol'),
            ('sourceslist', 'Debian Sourcelist'),
            ('splus', 'S'),
            ('sqlite3', 'sqlite3con'),
            ('squidconf', 'SquidConf'),
            ('ssp', 'Scalate Server Page'),
            ('sv', 'systemverilog'),
            ('tcl', 'Tcl'),
            ('tcsh', 'Tcsh'),
            ('tea', 'Tea'),
            ('tex', 'TeX'),
            ('trac-wiki', 'MoinMoin/Trac Wiki markup'),
            ('urbiscript', 'UrbiScript'),
            ('vala', 'Vala'),
            ('vb.net', 'VB.net'),
            ('velocity', 'Velocity'),
            ('vhdl', 'vhdl'),
            ('v', 'verilog'),
            ('xml+cheetah', 'XML + Cheetah'),
            ('xml+django', 'XML + Django/Jinja'),
            ('xml+erb', 'XML + Ruby'),
            ('xml+evoque', 'XML + Evoque'),
            ('xml+mako', 'XML + Mako'),
            ('xml+mako', 'XML + Mako'),
            ('xml+myghty', 'XML + Myghty'),
            ('xml+php', 'XML + PHP'),
            ('xml+smarty', 'XML + Smarty'),
            ('xml+velocity', 'XML + Velocity'),
            ('xml', 'XML'),
            ('xquery', 'XQuery'),
            ('xslt', 'XSLT'),
            ('yaml', 'YAML')))
    )
    SHARE_OPTIONS = (
        (0, 'Private / Not shared'),
        (1, 'Shared using private link'),
        (2, 'Open / Viewable for everyone'),
    )

    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=20, choices=LANGUAGES,
                                default='text')
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
