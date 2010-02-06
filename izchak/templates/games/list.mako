<%inherit file="/base.mako"/>

<%def name="title()">Games</%def>

<h1>All games</h1>

${h.form('', method='get')}
<dl class="standard-form">
    <dt>Player</dt>
    <dd>${c.form.player() | n}</dd>

    <dt>Role</dt>
    <dd>${c.form.role() | n}</dd>
    <dt>Race</dt>
    <dd>${c.form.race() | n}</dd>
    <dt>Gender</dt>
    <dd>${c.form.gender() | n}</dd>
    <dt>Alignment</dt>
    <dd>${c.form.alignment() | n}</dd>

    <dd><input type="submit" value="Search"></dd>
</dl>
% if any(True for field in c.form if field.data != field._default):
<p><a href="${url(controller='games', action='list')}">Reset filtering</a></p>
% endif
${h.end_form()}

<%def name="sort_header(column, label)">\
<%
    if c.form.sort.data == column:
        sortdir = 'asc' if c.form.sortdir.data == 'desc' else 'desc'
    elif column in c.descending_sort_fields:
        sortdir = 'desc'
    else:
        sortdir = 'asc'
%>
    <a href="${url.current(sort=column, sortdir=sortdir)}">
        % if c.form.sort.data == column:
            ## Assumes that descending-by-default fields are numeric
            <img src="/icons/sort-${'number' if column in c.descending_sort_fields else 'alphabet'}${'-descending' if c.form.sortdir.data == 'desc' else ''}.png" alt="${c.form.sortdir.data}"><br>
        % endif
        ${label}
    </a>
</%def>

<table class="games">
<thead>
<tr>
    <th><!-- trophy --></th>
    <th>Player</th>
    <th>${sort_header(u'points', u'Score')}</th>
    <th>${sort_header(u'turns', u'Turns')}</th>
    <th>Duration</th>
    <th>Deaths</th>
    <th>Role</th>
    <th>Race</th>
    <th>Gender</th>
    <th>Align</th>
    <th colspan="2">HP</th>
    <th>Died in</th>
    <th>${sort_header(u'end_time', u'Time')}</th>
</tr>
</thead>
% for game in c.games:
<tbody>
<tr>
    <td class="icon" rowspan="2">
        % if game.end_type.identifier == 'ascension':
        <img src="/icons/trophy.png" alt="">
        % elif game.end_type.identifier == 'escape':
        <img src="/icons/door-open-out.png" alt="">
        % elif game.end_type.identifier == 'quit':
        <img src="/icons/cross-small.png" alt="">
        % endif
    </td>
    <td><a href="${url(controller='players', action='view', name=game.player.name)}">${game.player.name}</a></td>
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
    <td rowspan="2" class="time">
    <a href="${url(controller='games', action='view', name=game.player.name, end_time=game.end_time.strftime('%s'))}">
        ${game.start_time.strftime(h.datetime_format)}
        <br>
        % if game.start_time.date() == game.end_time.date():
        to ${game.end_time.time().strftime(h.time_format)}
        % else:
        to ${game.end_time.strftime(h.datetime_format)}
        % endif
        </a>
    </td>
</tr>
<tr>
    <td class="epitaph" colspan="7">${game.epitaph}</td>
</tr>
</tbody>
% endfor
</table>
