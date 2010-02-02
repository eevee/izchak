<%inherit file="/base.mako"/>

<%def name="title()">Player ${c.player.name}</%def>

<h1>${c.player.name}</h1>

<h2>Stats</h2>
<ul>
    <li>Played <a href="${url(controller='games', action='list', player=c.player.name)}">${c.game_count} game${'' if c.game_count == 1 else 's'}</a></li>
</ul>


<h2>Breakdowns</h2>
% for label, breakdown in c.breakdowns:

<h3>${label}</h3>
<table class="bargraph">
<col class="col-category">
<col class="col-count">
<% max_count = None %>\
% for category, count in breakdown:
<% if max_count is None: max_count = count * 1.0 %>\
<tr>
    <td>${category.name}</td>
    <td>
        % if count:
        <div class="bargraph-bar" style="margin-right: ${100 - count / max_count * 100}%;">
            ${count}
        </div>
        % else:
        -
        % endif
    </td>
</tr>
% endfor
</table>
% endfor
