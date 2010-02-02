<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="/reset.css" type="text/css">
    <link rel="stylesheet" href="/layout.css" type="text/css">
    <title>${title()} – Veekun NetHack</title>
</head>
<body>
    <div id="header">
        <div id="title"><a href="http://cafeofbrokendreams.com">cafe</a> + <a href="http://veekun.com">veekun</a> NetHack server</div>
        <ul id="menu">
            <li><a href="${url(controller='games', action='list')}">games</a></li>
            <li><a href="${url(controller='players', action='list')}">players</a></li>
        </ul>
    </div>
    <div id="content">
        ${next.body()}
    </div>
</body>
</html>

<%def name="title()">Untitled</%def>
