<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="/reset.css" type="text/css">
    <link rel="stylesheet" href="/layout.css" type="text/css">
    <title>${self.title()} – Cafe / Veekun NetHack</title>
</head>
<body>
    <div id="header">
        <div id="title"><a href="http://cafeofbrokendreams.com">cafe</a> + <a href="http://veekun.com">veekun</a> NetHack server</div>
        <ul id="menu">
            <li><a href="${url(controller='main', action='index')}">overview</a></li>
            <li><a href="${url(controller='games', action='list')}">games</a></li>
            <li><a href="${url(controller='players', action='list')}">players</a></li>
            <li><a href="${url(controller='deaths', action='list')}">deaths</a></li>
        </ul>
    </div>
    <div id="content">
        ${next.body()}
    </div>
</body>
</html>

<%def name="title()">Untitled</%def>

<%def name="print_field(field)">
    <dt>${unicode(field.label) | n}</dt>
    <dd>
        ${field() | n}
        % for error in field.errors:
        <div class="form-error">${error}</div>
        % endfor
    </dd>
</%def>
