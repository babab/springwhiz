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

function start() {

    var sprwz_prefix_command = '@';
    var sprwz_prefix_bookmark = '#';

    $("#qcancel").hide();
    $("#help").hide();

    $("#helplink").click(function(){
        $("#help").show(1200);
    });

    $("#q").focus();
    modeinfo = document.getElementById('modeinfo');
    modesymbol = document.getElementById('modesymbol');

    var mode = 'default';

    function modeReset() {
        q = $("#q").val();

        mode = 'default';
        $("#mode").val('default');
        $("#modesymbol").css({'color': 'black'});
        $("#q").css({'color': 'black'});
        if (q == '')
            modeinfo.innerHTML = 'Enter search string or command';
        else
            modeinfo.innerHTML = 'Searching for: ' + q;
        modesymbol.innerHTML = "&gt;";
        $("#qcancel").hide();
    };

    $("#qcancel").click(function(){
        $("#q").val('');
        modeReset();
    });

    $("#q").keyup(function(){
        q = $("#q").val();

        if (q[0] == sprwz_prefix_command || mode == 'command') {
            mode = 'command';
            $("#mode").val('command');
            $("#modesymbol").css({'color': '#1E90FF'});
            $("#q").css({'color': '#1E90FF'});

            if (q[0] == sprwz_prefix_command) {
                $("#q").val($("#q").val().slice(1));
                modesymbol.innerHTML = sprwz_prefix_command;
                $("#qcancel").show(2000);
            }

            if (!q[1])
                modeinfo.innerHTML = "Entering command";
            else
                modeinfo.innerHTML = "Entering command '" + q.substr(1) + "'";
        }
        else if (q[0] == sprwz_prefix_bookmark || mode == 'bookmark') {
            mode = 'bookmark';
            $("#mode").val('bookmark');
            $("#modesymbol").css({'color': '#00688b'});
            $("#q").css({'color': '#00688b'});

            if (q[0] == sprwz_prefix_bookmark) {
                $("#q").val($("#q").val().slice(1));
                modesymbol.innerHTML = sprwz_prefix_bookmark;
                $("#qcancel").show(2000);
            }

            if (!q[1])
                modeinfo.innerHTML = "Go to bookmark with label";
            else
                modeinfo.innerHTML = "Go to bookmark with label '"
                        + q.substr(1) + "'";
        }
        else if (q[0] == '!' || mode == 'bang') {
            mode = 'bang';
            $("#mode").val('bang');
            $("#modesymbol").css({'color': '#8B4513'});
            $("#q").css({'color': '#8B4513'});

            if (q[0] == '!') {
                $("#q").val(
                    $("#q").val().slice(1)
                );
                modesymbol.innerHTML = '!';
                $("#qcancel").show(2000);
            }

            if (!q[1])
                modeinfo.innerHTML = 'Searching using bang syntax';
            else
                modeinfo.innerHTML = "Searching for '" + q.substr(1)
                        + "' using bang syntax";
        }
        else if (q[0] == "\\" || mode == 'ddg1st') {
            mode = 'ddg1st';
            $("#mode").val('ddg1st');
            $("#modesymbol").css({'color': '#228B22'});
            $("#q").css({'color': '#228B22'});

            if (q[0] == "\\") {
                $("#q").val(
                    $("#q").val().slice(1)
                );
                modesymbol.innerHTML = "\\";
                $("#qcancel").show(2000);
            }

            if (!q[1])
                modeinfo.innerHTML = 'Go to first match ';
            else
                modeinfo.innerHTML = 'Go to the first result for: '
                                     + q.substr(1);
        }
        else {
            modeReset();
        }
    });
};
