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

YUI_COMP_EXEC="`which yui-compressor`"
STATIC_PATH="springwhiz/static"

if [ $? -gt 0 ]; then
    echo "Could not find yui-compressor"
    exit 1
fi

${YUI_COMP_EXEC} -v --type js ${STATIC_PATH}/js/start.js > \
                                 ${STATIC_PATH}/js/start.min.js
${YUI_COMP_EXEC} -v --type css ${STATIC_PATH}/css/main.css > \
                                ${STATIC_PATH}/css/main.min.css

mv ${STATIC_PATH}/js/start.min.js ${STATIC_PATH}/js/start.js
mv ${STATIC_PATH}/css/main.min.css ${STATIC_PATH}/css/main.css
