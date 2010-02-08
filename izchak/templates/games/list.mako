<%inherit file="/base.mako"/>

<%def name="title()">Games</%def>

<h1>All games</h1>
<p>
    <img src="/icons/points.png" alt="">
    <a href="${url.current(recency='30', sort='points', sortdir='desc')}">Top games, past month</a> &bull;
    <a href="${url.current(recency='365', sort='points', sortdir='desc')}">Top games, past year</a> &bull;
    <a href="${url.current(recency='all', sort='points', sortdir='desc')}">Top games, all time</a>
</p>
<p>
    <img src="/icons/trophy.png" alt="">
    <a href="${url.current(end_type='ascension', sort='points', sortdir='asc')}">Lowest ascensions</a> &bull;
    <a href="${url.current(end_type='ascension', sort='real_time', sortdir='desc')}">Fastest ascensions (time)</a> &bull;
    <a href="${url.current(end_type='ascension', sort='turns', sortdir='desc')}">Fastest ascensions (turns)</a>
</p>
<p>
    <img src="/icons/ghost.png" alt="">
    <a href="${url.current(end_type='death', sort='final_hp', sortdir='asc')}">Most egregious deaths</a>
</p>

${h.form('', method='get')}
<div class="columns2">
    <div class="columns2-left">
        <dl class="standard-form">
            ${self.print_field(c.form.player)}
            ${self.print_field(c.form.role)}
            ${self.print_field(c.form.race)}
            ${self.print_field(c.form.gender)}
            ${self.print_field(c.form.alignment)}
        </dl>
    </div>
    <div class="columns2-right">
        <dl class="standard-form">
            ${self.print_field(c.form.end_type)}
            ${self.print_field(c.form.recency)}
        </dl>
    </div>
</div>
<p><input type="submit" value="Search"></p>

% if any(True for field in c.form if field.data != field._default):
<p><a href="${url(controller='games', action='list')}">Reset filtering</a></p>
% endif
${h.end_form()}


## Stop right here if the form is bogus
% if not c.valid_form:
<% return %>\
% endif

## RESULTS
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
    <th class="hp1">${sort_header(u'final_hp', u'HP')}</td>
    <th class="hp2">${sort_header(u'max_hp', u'/Max HP')}</td>
    <th>Died in</th>
    <th>${sort_header(u'end_time', u'Time')}</th>
</tr>
</thead>
% for game in c.games:
<tbody>
<tr>
    <td class="icon" rowspan="2">
        ${h.end_type_icon(game.end_type)}
    </td>
    <td><a href="${url(controller='players', action='view', name=game.player.name)}">${game.player.name}</a></td>
    <td class="number">${game.points | h.format_commify}</td>
    <td class="number">${game.turns | h.format_commify}</td>
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
