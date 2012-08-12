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

function start()
{
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

    var mode = 'default';

    function defaultMode()
    {
        q = $("#q").val();

        $("#mode").val('default');
        $("#modesymbol").css({'color': 'black'});
        $("#q").css({'color': 'black'});
        if (q == '')
            modeinfo.innerHTML = 'Enter search string or command';
        else
            modeinfo.innerHTML = 'Searching for: ' + q;
        modesymbol.innerHTML = "&gt;";
        $("#qcancel").hide();
        mode = 'default';
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
            $("#modesymbol").css({'color': '#1E90FF'});
            $("#q").css({'color': '#1E90FF'});
            if (!q[0])
                modeinfo.innerHTML = "Entering command";
            else
                modeinfo.innerHTML = "Entering command '" + q + "'";
            break;
        case 'bookmark':
            $("#mode").val('bookmark');
            $("#modesymbol").css({'color': '#00688b'});
            $("#q").css({'color': '#00688b'});
            if (!q[0])
                modeinfo.innerHTML = "Go to bookmark with label";
            else
                modeinfo.innerHTML = "Go to bookmark with label '" + q + "'";
            break;
        case 'bang':
            $("#mode").val('bang');
            $("#modesymbol").css({'color': '#8B4513'});
            $("#q").css({'color': '#8B4513'});
            if (!q[0])
                modeinfo.innerHTML = 'Searching using bang syntax';
            else
                modeinfo.innerHTML = "Searching for '" + q
                        + "' using bang syntax";
            break;
        case 'ddg1st':
            $("#mode").val('ddg1st');
            $("#modesymbol").css({'color': '#228B22'});
            $("#q").css({'color': '#228B22'});
            if (!q[0])
                modeinfo.innerHTML = 'Go to first result ';
            else
                modeinfo.innerHTML = 'Go to the first result for: ' + q;
            break;
        default:
            defaultMode();
        }
    });
};
