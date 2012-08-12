/*
 * This file is part of springwhiz.
 *
 * springwhiz is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * springwhiz is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with springwhiz.  If not, see <http://www.gnu.org/licenses/>.
 */

$(document).ready(function ()
{
    $("#help").hide();

    // Show help when link is clicked
    $("#helplink").click(function(){
        $("#help").show(1200);
    });
});
