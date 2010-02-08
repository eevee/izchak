<%inherit file="/base.mako"/>

<%def name="title()">Deaths</%def>

<h1>Deaths</h1>
<table class="games">
<thead>
<tr>
    <th><!-- trophy --></th>
    <th>Count</th>
    <th>Total points</th>
    <th>Epitaph</th>
</tr>
</thead>
% for death in c.deaths:
<tbody>
<tr>
    <td class="icon" rowspan="2">
        ##${h.end_type_icon(game.end_type)}
    </td>
    <td class="number">${h.format_commify(death.count)}</td>
    <td class="number">${h.format_commify(death.total_points)}</td>
    <td>${death.epitaph_simple}</td>
</tr>
</tbody>
% endfor
</table>
