<%inherit file="/base.mako"/>

<table class="games">
<thead>
<tr>
    <th>Player</th>
    <th>Points</th>
    <th>Turns</th>
    <th>Duration</th>
    <th>Deaths</th>
    <th>Role</th>
    <th>Race</th>
    <th>Sex</th>
    <th>Align</th>
    <th colspan="2">HP</th>
    <th>Died in</th>
    <th>Time</th>
</tr>
</thead>
% for game in c.games:
<tbody>
<tr>
    <td>${game.player.name}</td>
    <td class="number">${game.points}</td>
    <td class="number">${game.turns}</td>
    <td class="number">${game.real_time}</td>
    <td class="number">${game.deaths}</td>

    <td>${game.role.name}</td>
    <td>${game.race.name}</td>
    <td rowspan="2">
        % if game.gender != game.final_gender:
        <del>${game.gender.name}</del><br>
        % endif
        ${game.final_gender.name}
    </td>
    <td rowspan="2">
        % if game.alignment != game.final_alignment:
        <del>${game.alignment.name}</del><br>
        % endif
        ${game.final_alignment.name}
    </td>

    <td rowspan="2" class="hp1">${game.final_hp}</td>
    <td rowspan="2" class="hp2">/${game.max_hp}</td>
    <td rowspan="2" class="dlvl">
        ${game.final_dungeon.short_name} dlvl ${game.final_dlvl}
        % if game.final_dlvl != game.deepest_dlvl:
        <br>out of ${game.deepest_dlvl}
        % endif
    </td>
    <td rowspan="2">
        ${game.start_time}
        <br>
        ${game.end_time}
    </td>
</tr>
<tr>
    <td class="epitaph" colspan="7">${game.epitaph}</td>
</tr>
</tbody>
% endfor
</table>
