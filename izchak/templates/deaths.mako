<%inherit file="/base.mako"/>

<%def name="title()">Deaths</%def>

<h1>Deaths</h1>
<table class="games">
<thead>
<tr>
    <th><!-- trophy --></th>
    <th>Count</th>
    <th>Total score</th>
    <th>Average score</th>
    <th>Deepest dlvl</th>
    <th>Average dlvl</th>
    <th>Epitaph</th>
</tr>
</thead>
% for death in c.deaths:
<tbody>
<tr>
    <td class="icon" rowspan="2">
        ${h.end_type_icon(death.end_type_identifier)}
    </td>
    <td class="number">${h.format_commify(death.count)}</td>
    <td class="number">${h.format_commify(death.total_points)}</td>
    <td class="number">${h.format_commify(h.format_float(death.average_points))}</td>
    <td class="number">${h.format_commify(death.max_dlvl)}</td>
    <td class="number">${h.format_commify(h.format_float(death.average_dlvl))}</td>
    <td>${death.epitaph_simple}</td>
</tr>
</tbody>
% endfor
</table>
