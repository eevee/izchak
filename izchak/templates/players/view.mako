<%inherit file="/base.mako"/>

<%def name="title()">Player ${c.player.name}</%def>

<h1>${c.player.name}</h1>

<h2>Stats</h2>
<ul>
    <li>Played <a href="${url(controller='games', action='list', player=c.player.name)}">${c.game_count} game${'' if c.game_count == 1 else 's'}</a></li>
</ul>


<h2>Breakdowns</h2>
<%! from izchak.model import EndType %>
<%def name="print_breakdown(label)">
<h3>${label}</h3>
<table class="bargraph">
<col class="col-category">
<col class="col-count">
<% max_count = c.breakdowns[label][0].count %>\
% for category, count in c.breakdowns[label]:
<tr>
    <td class="col-category">
        ${category.name}
        % if isinstance(category, EndType):
        ${h.end_type_icon(category)}
        % endif
    </td>
    <td>
        % if count:
        <div class="bargraph-bar" style="margin-right: ${100 - 100.0 * count / max_count}%;">
            ${count}
        </div>
        % else:
        <div class="bargraph-bar-zero">0</div>
        % endif
    </td>
</tr>
% endfor
</table>
</%def>

<div class="columns2">
<div class="columns2-left">
${print_breakdown(u'Ending')}
${print_breakdown(u'Race')}
${print_breakdown(u'Gender')}
</div>
<div class="columns2-right">
${print_breakdown(u'Role')}
${print_breakdown(u'Alignment')}
</div>
</div>
