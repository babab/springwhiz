/* Copyright (C) 2012-2013  Benjamin Althues
 *
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

(function ($) {
    $(document).ready(function () {
        // Settings
        var sprwz_prefix_command = '@';
        var sprwz_prefix_bookmark = '#';

        // Hide divs (when javascript is enabled)
        $("#qcancel").hide();

        // Focus on input field
        $("#q").focus();

        // Mode handling
        modeinfo = document.getElementById('modeinfo');
        modesymbol = document.getElementById('modesymbol');

        // Activate typeahead
        typeahead_list = [];
        $("#q").typeahead({
            'items': 15,
            'source': function(){return typeahead_list},
        });

        var mode = 'default';

        function defaultMode() {
            q = $("#q").val();

            $("#mode").val('default');
            $("#modesymbol").css({'background-color': 'black',
                                  'border': '1px solid black'});
            $("#q").css({'color': 'black'});
            if (q == '')
                modeinfo.innerHTML = 'Enter search string or command';
            else
                modeinfo.innerHTML = 'Searching for: '
                  + '<span id="modeinfo-inner">' + q + '</span>';
            $("#modeinfo-inner").css({'color': 'black'});
            modesymbol.innerHTML = "&gt;";
            $("#qcancel").hide();
            mode = 'default';
            typeahead_list = [];
        }

        $("#qcancel").click(function(){
            $("#q").val('');
            defaultMode();
            $("#q").focus();
        });

        $("#q").keyup(function(){
            q = $("#q").val();

            switch(q[0]) {
                case sprwz_prefix_command:
                    $("#q").val($("#q").val().slice(1));
                    modesymbol.innerHTML = sprwz_prefix_command;
                    $("#qcancel").show(2000);
                    mode = 'command';
                    break;
                case sprwz_prefix_bookmark:
                    $("#q").val($("#q").val().slice(1));
                    modesymbol.innerHTML = sprwz_prefix_bookmark;
                    $("#qcancel").show(2000);
                    mode = 'bookmark';
                    break;
                case '!':
                    $("#q").val($("#q").val().slice(1));
                    modesymbol.innerHTML = '!';
                    $("#qcancel").show(2000);
                    mode = 'bang';
                    break;
                case "\\":
                    $("#q").val($("#q").val().slice(1));
                    modesymbol.innerHTML = "\\";
                    $("#qcancel").show(2000);
                    mode = 'ddg1st';
                    break;
                case ">":
                    $("#q").val($("#q").val().slice(1));
                    modesymbol.innerHTML = "&gt;";
                    mode = 'default';
            }

            switch (mode) {
                case 'command':
                    $("#mode").val('command');
                    $("#modesymbol").css({'background-color': '#1E90FF',
                                          'border': '1px solid #1E90FF'});
                    $("#q").css({'color': '#1E90FF'});
                    if (!q[0])
                        modeinfo.innerHTML = "Entering command";
                    else
                        modeinfo.innerHTML = "Entering command '<span "
                          + 'id="modeinfo-inner">' + q + "</span>'";
                    $("#modeinfo-inner").css({'color': '#1E90FF'});
                    typeahead_list = typeahead_command_list;
                    break;
                case 'bookmark':
                    $("#mode").val('bookmark');
                    $("#modesymbol").css({'background-color': '#00688b',
                                          'border': '1px solid #00688b'});
                    $("#q").css({'color': '#00688b'});
                    if (!q[0])
                        modeinfo.innerHTML = "Go to bookmark with label";
                    else
                        modeinfo.innerHTML = "Go to bookmark with label '"
                           + '<span id="modeinfo-inner">' + q + "</span>'";
                    $("#modeinfo-inner").css({'color': '#00688b'});
                    typeahead_list = [];
                    break;
                case 'bang':
                    $("#mode").val('bang');
                    $("#modesymbol").css({'background-color': '#8B4513',
                                          'border': '1px solid #8B4513'});
                    $("#q").css({'color': '#8B4513'});
                    if (!q[0])
                        modeinfo.innerHTML = 'Searching using bang syntax';
                    else
                        modeinfo.innerHTML = "Searching for '"
                           + '<span id="modeinfo-inner">' + q + "</span>'";
                           + 'using bang syntax';
                    $("#modeinfo-inner").css({'color': '#8B4513'});
                    typeahead_list = typeahead_bang_list;
                    break;
                case 'ddg1st':
                    $("#mode").val('ddg1st');
                    $("#modesymbol").css({'background-color': '#228B22',
                                          'border': '1px solid #228B22'});
                    $("#q").css({'color': '#228B22'});
                    if (!q[0])
                        modeinfo.innerHTML = 'Go to first result ';
                    else
                        modeinfo.innerHTML = 'Go to the first result for: '
                           + '<span id="modeinfo-inner">' + q + '</span>';
                    $("#modeinfo-inner").css({'color': '#228B22'});
                    typeahead_list = [];
                    break;
                default:
                    defaultMode();
            }
        });
    });
})(jQuery);
