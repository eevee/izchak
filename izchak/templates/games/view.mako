<%inherit file="/base.mako"/>

<%def name="title()">Games</%def>

<h1><a href="${url(controller='players', action='view', name=c.game.player.name)}">${c.game.player.name}</a>'s game ending ${c.game.end_time.strftime(c.datetime_format)}</h1>

<p id="epitaph">${c.game.epitaph}</p>

<dl>
    <dt>Started on</dt>
    <dd>${c.game.start_time.strftime(h.datetime_format)}</dd>
    <dt>Ended</dt>
    <dd>${c.game.end_time.strftime(h.datetime_format)}</dd>
    <dt>Lasted</dt>
    <dd>${c.game.end_time - c.game.start_time}</dd>
</dl>

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
            context.write(line)
        dumplog.close()
    except IOError:
        context.write("Uh oh!  Can't find the log.")
%>
</pre>
