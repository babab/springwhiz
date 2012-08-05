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

YUI_COMP_EXEC="`which yui-compressor`"

if [ $? -gt 0 ]; then
    exit 1
fi

$YUI_COMP_EXEC -v --type js static/js/start.js > static/js/start.min.js
$YUI_COMP_EXEC -v --type css static/css/reset.css > static/css/reset.min.css
$YUI_COMP_EXEC -v --type css static/css/main.css > static/css/main.min.css

mv static/js/start.min.js static/js/start.js
mv static/css/reset.min.css static/css/reset.css
mv static/css/main.min.css static/css/main.css
