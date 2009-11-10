<%inherit file="/base.mako"/>

<table>
<tr>
    <th>Name</th>
</tr>
% for player in c.players:
<tr>
    <td><a href="${url(controller='players', action='view', name=player.name)}">${player.name}</a></td>
</tr>
% endfor
</table>
