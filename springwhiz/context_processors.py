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

from django import get_version as django_version
from sys import version as python_version

from settings import BASE_URL, SPRINGWHIZ_VERSION


def platform_version_info(request):
    return {'version_springwhiz': SPRINGWHIZ_VERSION,
            'version_python': python_version.split()[0],
            'version_django': django_version()}


def base_url(request):
    return {'BASE_URL': BASE_URL}
