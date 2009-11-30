<%inherit file="/base.mako"/>

<table>
% for game in c.games:
<tr>
    <td>${game.player.name}</td>
    <td>${game.role.name}</td>
    <td>${game.race.name}</td>
    <td>${game.gender.name}</td>
    <td>${game.alignment.name}</td>
    <td>${game.final_gender.name}</td>
    <td>${game.final_alignment.name}</td>

    <td>${game.start_time}</td>
    <td>${game.end_time}</td>
    <td>${game.real_time}</td>

    <td>${game.points}</td>
    <td>${game.turns}</td>
    <td>${game.final_dlvl}</td>
    <td>${game.final_dungeon.name}</td>
    <td>${game.deepest_dlvl}</td>
    <td>${game.final_hp}</td>
    <td>${game.max_hp}</td>
    <td>${game.deaths}</td>

    <td>${game.end_type.identifier}</td>
    <td>${game.epitaph_simple}</td>
</tr>
% endfor
</table>
