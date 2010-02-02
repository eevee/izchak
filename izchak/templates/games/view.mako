<%inherit file="/base.mako"/>

<%def name="title()">Games</%def>

<h1><a href="${url(controller='players', action='view', name=c.game.player.name)}">${c.game.player.name}</a>'s game ending ${c.game.end_time.strftime(c.datetime_format)}</h1>

<p id="epitaph">${c.game.epitaph}</p>

<dl>
    <dt>Started on</dt>
    <dd>${c.game.start_time.strftime(c.datetime_format)}</dd>
    <dt>Lasted</dt>
    <dd>${c.game.end_time - c.game.start_time}</dd>
</dl>

<h2>Dump log</h2>
<iframe id="dumplog" src="http://nethack.veekun.com/userdata/Eevee/dumplog/${c.game.start_time.strftime("%s")}-${c.game.end_time.strftime("%s")}.nh343.txt"></iframe>
