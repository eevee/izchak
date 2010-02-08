<%inherit file="/base.mako"/>
<%! from datetime import timedelta %>

<%def name="title()">${c.game.player.name}'s game of ${c.game.end_time.strftime(h.datetime_format)}</%def>

<h1><a href="${url(controller='players', action='view', name=c.game.player.name)}">${c.game.player.name}</a>'s game of ${c.game.end_time.strftime(h.datetime_format)}</h1>

<p id="epitaph">${h.end_type_icon(c.game.end_type)} ${c.game.epitaph}</p>

<dl class="standard-form">
    <dt>Time</dt>
    <dd>
        ${c.game.start_time.strftime(h.datetime_format)}
        through
        ${c.game.end_time.strftime(h.datetime_format)}
    </dd>
    <dt>Duration</dt>
    <dd>
        ${c.game.real_time} time played
        of ${c.game.end_time - c.game.start_time} total
        (dedication: ${h.divide_timedeltas(c.game.real_time, c.game.end_time - c.game.start_time) * 100.0 | h.format_float}%)
    </dd>

    <dt>Turns</dt>
    <dd>${c.game.turns | h.format_commify} (speed: ${c.game.real_time / c.game.turns} per turn)</dd>
    <dt>Score</dt>
    <dd>${c.game.points | h.format_commify} (efficiency: ${1.0 * c.game.points / c.game.turns | h.format_float} points per turn)</dd>

    <dt>Character</dt>
    <dd>
        ${c.game.role.name}
        ${c.game.race.name}
        ${c.game.gender.name}
        ${c.game.alignment.name}
        % if c.game.gender != c.game.final_gender \
          or c.game.alignment != c.game.final_alignment:
            (started as ${c.game.final_gender.name} ${c.game.final_alignment.name})
        % endif
    </dd>
    <dt>Ending</dt>
    <dd>
        ${c.game.end_type.identifier}
        on dlvl ${c.game.final_dlvl} of ${c.game.final_dungeon.name},
        % if c.game.final_dlvl != c.game.deepest_dlvl:
        having reached dlvl ${c.game.deepest_dlvl},
        % endif
        with ${c.game.final_hp}/${c.game.max_hp} HP
        % if (c.game.end_type.identifier == 'death' and c.game.deaths > 1) \
          or (c.game.end_type.identifier != 'death' and c.game.deaths > 0):
            and ${c.game.deaths} prior death${'' if c.game.deaths == 1 else 's'}
        % endif
    </dd>
</dl>

<div class="columns2">
    <dl class="standard-form columns2-left">
        <dt>Behavior</dt>
        <dd>
            <ul class="checklist">
                <%! from izchak.model import Conduct %>
                % for conduct in Conduct.query.order_by(Conduct.id.asc()):
                % if conduct in c.game.conducts:
                <li class="yes">${conduct.description}</li>
                % else:
                <li class="no">${conduct.description}</li>
                % endif
                % endfor
            </ul>
        </dd>
    </dl>
    <dl class="standard-form columns2-right">
        <dt>Accomplishments</dt>
        <dd>
            <ul class="checklist">
                <%! from izchak.model import Milestone %>
                % for milestone in Milestone.query.order_by(Milestone.id.asc()):
                % if milestone in c.game.milestones:
                <li class="yes">${milestone.description}</li>
                % else:
                <li class="no">${milestone.description}</li>
                % endif
                % endfor
            </ul>
        </dd>
    </dl>
</div>

<h2>Dump log</h2>
<%
    # <iframe>s suck.  <object>s suck more.  Stick the damn log in manually.
    # Should a template be doing this?  Well, is <%include> any different?
    dumplog_path = "userdata/{name}/dumplog/{start_time}-{end_time}.nh343.txt".format(
        name=c.game.player.name,
        start_time=c.game.start_time.strftime("%s"),
        end_time=c.game.end_time.strftime("%s"),
    )
%>
<p><a href="http://nethack.veekun.com/${dumplog_path}">
    <img src="/icons/book-brown.png" alt="">
    Direct link
</a></p>
<pre id="dumplog">
<%
    try:
        # TODO config
        dumplog = open('/opt/nethack.veekun.com/dgldir/' + dumplog_path)
        for line in dumplog:
            context.write( h.escape(line) )
        dumplog.close()
    except IOError:
        context.write("Uh oh!  Can't find the log.")
%>
</pre>
