<%inherit file="/base.mako"/>

<%def name="title()">Overview</%def>

<p id="big-honkin-telnet-command">telnet nethack.veekun.com</a>

<h1>NetHack</h1>
<p><a href="http://www.nethack.org/">NetHack</a> is a decades-old terminal game.  It's complicated and unforgiving.  And it's great.  Wikipedia has a <a href="http://en.wikipedia.org/wiki/NetHack">good overview</a>.</p>

<h1>Playing</h1>
<p>You can play on my server by telnetting to <code>nethack.veekun.com</code>.  If you're on Linux, OS X, or any other Unix derivative, built-in <code>telnet</code> ought to work fine.  If you're on Windows, your best bet is <a href="http://nethack.wikia.com/wiki/PuTTY">PuTTY</a>.</p>
<p>If you're enjoying yourself, swing by <a href="irc://irc.veekun.com/cafe">irc.veekun.com #cafe</a>, our general gaming channel, and enjoy our NetHack death-reporting bot.  It's like Rodney, but less useful!</p>

<h1>Configuring</h1>
<p>Log in and press <kbd>o</kbd> to edit your options file.  The base NetHack options are <a href="http://www.nethack.org/v343/Guidebook.html#_TOCentry_43">described in the documentation</a>.  There are a few extra options provided by modifications we have made to the game; these are listed at the bottom of the default configuration file.</p>
<p>All of the following are on by default.</p>
<dl>
    <dt><var>menucolors</var></dt>
    <dd>Enables the menucolors patch, allowing color to brighten your inventory and spell/skill lists.  Colors are configured with the <var>MENUCOLOR</var> variable.</dd>
    <dt><var>statuscolors</var></dt>
    <dd>Enables the statuscolors patch, allowing color to brighten your status bar.  Colors are configured with the <var>STATUSCOLOR</var> variable.</dd>
    <dt><var>paranoid_hit</var></dt>
    <dt><var>paranoid_quit</var></dt>
    <dt><var>paranoid_remove</var></dt>
    <dd>Enables various parts of the paranoid patch, making it difficult to hit peaceful monsters, quit the game, or remove armor accidentally.</dd>
    <dt><var>pickup_thrown</var></dt>
    <dd>Enables the pickup_thrown patch, causing you to automatically pick up items you threw.</dd>
    <dt><var>quiver_fired</var></dt>
    <dd>Enables the quiver_fired patch, which automatically quivers any item you <kbd>f</kbd>ire if your quiver were previously empty.</dd>
    <dt><var>like_swimming</var></dt>
    <dd>Enables the <code>r</code> item category from the itemcat patch, allowing you to use <code>r</code> as an item category for <kbd>D</kbd>rop or <kbd>I</kbd>nventory to select all rustable items.</dd>
    <dt><var>sortloot</var></dt>
    <dd>Enables the sortloot patch, grouping items in loot/pickup menus by category.</dd>
    <dt><var>showbuc</var></dt>
    <dd>Enables the showbuc patch, including 'uncursed' in the name of fully-identified wands et al. so they can be colored correctly by menucolors.</dd>
    <dt><var>showsym</var></dt>
    <dd>Enables the showsym patch, which puts item category characters in the respective category headers.</dd>
</dl>
<p>Additionally, the game has been compiled with <var>autopickup_exceptions</var> support.  The default is to autopickup all money, magical items, gems (but not rocks/stones), and food (but not corpses).</p>

<h1>Modifications</h1>
<p>Our copy of NetHack has been substantially modified.  Most of the changes are interface enhancements, but there are also a handful of small gameplay changes.</p>
<h2>Bugs</h2>
<dl>
    <dt><a href="http://bilious.homelinux.org/?340">acid drop fix</a></dt>
    <dd>Fixes some crashes related to dropping acid.  Hm.</dd>
    <dt><a href="http://bilious.homelinux.org/?337">astral call exploit fix</a></dt>
    <dd>It's possible to figure out the correct altar on the Astral Plane by using telepathy and trying to <kbd>C</kbd>all a priest; the game will reveal the priest's corresponding god in the resulting error message.  This patch randomizes the named god, fixing this minor exploit.</dd>
    <dt><a href="http://bilious.homelinux.org/?349">secure random number generator</a></dt>
    <dd>The default NetHack PRNG is easily broken.  This one should be effectively impossible to exploit.</dd>
</dl>
<h2>Gameplay</h2>
<dl>
    <dt><a href="http://bilious.homelinux.org/?270">ring of memory</a></dt>
    <dd>Adds a single new item: the ring of memory, which protects against amnesia, stops brain-sucking, and extends how long spells are remembered.</dd>
</dl>
<h2>Dungeon</h2>
<dl>
    <dt><a href="http://bilious.homelinux.org/?18">extra bigrooms</a></dt>
    <dt><a href="http://bilious.homelinux.org/?27">extra castles</a></dt>
    <dt><a href="http://bilious.homelinux.org/?25">extra medusas</a></dt>
    <dt><a href="http://bilious.homelinux.org/?26">extra sokobans</a></dt>
    <dd>Adds new variations on some fixed-layout special levels.</dd>
    <dt><a href="http://bilious.homelinux.org/?254">flipped levels</a></dt>
    <dd>Fixed special levels can be randomly flipped: horizontally, vertically, or both.</dd>
    <dt><a href="http://bilious.homelinux.org/?264">moonphase</a></dt>
    <dd>Fewer rooms are dark around a full moon, and more are dark around a new moon.</dd>
    <dt><a href="http://bilious.homelinux.org/?218">spore colony</a></dt>
    <dd>Adds a new special room, the spore colony, which contains a chain reaction of gas spores waiting to happen.</dd>
</dl>
<h2>Player actions</h2>
<dl>
    <dt><a href="http://bilious.homelinux.org/?87">alchemy: acid</a></dt>
    <dd>Just like SLASH'EM, valuable gems may be dissolved in acid to create a potion of the appropriate color.  The exact combinations are <a href="http://nethack.wikia.com/wiki/Alchemy#SLASH.27EM">listed on WikiHack</a>, with the following changes: amber creates amber potions, jasper creates brown potions, and aquamarine creates viscous potions.  These modifications were necessary to work with color alchemy, which changed two potion colors.</dd>
    <dt><a href="http://bilious.homelinux.org/?59">alchemy: colors</a></dt>
    <dd>Alchemy is based on the colors of the ingredients rather than their effects.  For example, <kbd>#dip</kbd>ping a ruby potion into a golden potion will create either an amber or an orange potion.</dd>
    <dt><a href="http://bilious.homelinux.org/?179">cats and can openers</a></dt>
    <dd>When you use a tin opener, your pet cats come running.</dd>
    <dt><a href="http://bilious.homelinux.org/?23">coinflip</a></dt>
    <dd><kbd>a</kbd>pply <kbd>$</kbd> to flip a coin.</dd>
    <dt><a href="http://bilious.homelinux.org/?193">dragon hoard</a></dt>
    <dd>A player polymorphed into a dragon may <kbd>#sit</kbd> on a pile of gold for a silly message.</dd>
    <dt><a href="http://bilious.homelinux.org/?147">trap cancel</a></dt>
    <dd>Stand over a magic trap and zap cancellation downwards to remove it.</dd>
</dl>
<h2>Interface</h2>
<dl>
    <dt><a href="http://www.netsonic.fi/~walker/nethack.html#adjsplit">adjsplit</a></dt>
    <dd><kbd>#adjust</kbd> may now be used to split a stack of items, by providing a number before the inventory letter.  That number of items will be moved to the new letter, and the rest will stay where they are.</dd>
    <dt><a href="http://bilious.homelinux.org/?267">dungeon overview</a></dt>
    <dd>The protagonist now remembers what features are on each dungeon level.  Use <kbd>#overview</kbd> or <kbd>ctrl-o</kbd> to see a list of what you've seen, or <kbd>#annotate</kbd> to name a dungeon level.  Amnesia will erase parts of this list as appropriate.</dd>
    <dt><a href="http://nh.gmuf.com/#itemcat">itemcat</a></dt>
    <dd>Adds several new item categories usable at <kbd>D</kbd>rop and <kbd>I</kbd>nventory prompts: <code>I</code> for unidentified items, <code>P</code> for the last group of items picked up or looted, <code>Q</code> for the last group of items auto-picked up, <code>r</code> for items that can rust, or <code>Z</code> to invert the selection.</dd>
    <dt><a href="http://www.netsonic.fi/~walker/nethack.html#paranoid">paranoid</a></dt>
    <dd>Requires the player to type 'yes' rather than merely 'y' at important prompts.  Enabled by <var>paranoid_hit</var>, <var>paranoid_quit</var>, and <var>paranoid_remove</var>, which correspond to attacking a peaceful creature, quitting the game, and removing the last accessory or piece of armor (which will show the normal list instead of automatically removing it).  All three are on by default.</dd>
    <dt><a href="http://bilious.homelinux.org/?98">pickup_thrown</a></dt>
    <dd>Items specifically thrown by the player can be auto-picked up.  Enabled by the <var>pickup_thrown</var> option, which is on by default.</dd>
    <dt><a href="http://www.netsonic.fi/~walker/nethack.html#quivfir">quiverfire</a></dt>
    <dd>If the <kbd>f</kbd>ire command is used with an empty quiver, the item selected to fire will automatically be quivered.  Enabled by the <var>quiver_fire</var> option, which is on by default.</dd>
    <dt>simple_mail  (comes with <a href="http://nethack.wikia.com/wiki/Dgamelaunch">dgamelaunch</a>)</dt>
    <dd>Observers can send a player mail.</dd>
</dl>
<h2>Display</h2>
<dl>
    <dt><a href="http://bilious.homelinux.org/?296">colored walls/floor</a></dt>
    <dd>Some special areas have colored walls or floor.  For example, altars are colored like unicorns, and the randomly-generated walls of the Gnomish Mines are now brown.</dd>
    <dt><a href="http://bilious.homelinux.org/?116">dark room</a></dt>
    <dd>Dark parts of rooms that have been previously explored are now indicated with a dark gray floor character, to distinguish them from solid rock.</dd>
    <dt><a href="http://www.netsonic.fi/~walker/nethack.html#makedefs">makedefs</a></dt>
    <dd>Lists many common patches in the <kbd>#version</kbd> response.</dd>
    <dt><a href="http://bilious.homelinux.org/?11">menucolors</a></dt>
    <dd>Provides colors for your inventory, the spell menu, and the #enhance menu.  The coloring can be customized by the <var>MENUCOLOR</var> variable.  The default is to color cursed/uncursed/blessed items as red/yellow/green, bold holy and unholy water, and color spells in the spell menu according to success rate.</dd>
    <dt><a href="http://bilious.homelinux.org/?198">showbuc</a></dt>
    <dd>Always show '<code>uncursed</code>' in the name of identified items.  Vanilla NetHack names fully-identified wands, for example, as merely "a wand of nothing (0:6)" .  Enabled by the <var>showbuc</var> option, which is on by default.</dd>
    <dt><a href="http://bilious.homelinux.org/?15">showsym</a></dt>
    <dd>When showing a menu of items where an item category character can be pressed to select all items of that type, show the character in each category header.  Enabled by the <var>showsym</var> option, which is on by default.</dd>
    <dt><a href="http://www.netsonic.fi/~walker/nethack.html#sortloot">sortloot</a></dt>
    <dd>When picking up items from a pile or looting a container, items are sorted into categories just like with the built-in <var>sortpack</var> option.</dd>
    <dt><a href="http://bilious.homelinux.org/?142">statuscolors</a></dt>
    <dd>Allows recoloring of parts of the status bar, as controlled by the <var>STATUSCOLOR</var> variable.  The default is to color power and hp in blue/green/yellow/red as they decrease and color status effects in various appropriate colors.</dd>
    <dt><a href="http://bilious.homelinux.org/?200">toonhit</a></dt>
    <dd>Fighting while hallucinating will greatly resemble old Batman fight scenes.</dd>
    <dt><a href="http://bilious.homelinux.org/?205">use_darkgray</a>  (<a href="http://github.com/tycho/nethack/commit/6290e48011e3e9d4a72491f3b3d746e784367f9f">mirror</a>)</dt>
    <dd>Uses dark gray instead of dark blue for monsters and items that are actually gray or black.  Enabled by the <var>use_darkgray</var> option, which is on by default.  Turn this off if you're running into invisible unicorns!</dd>
    <dt><a href="http://bilious.homelinux.org/?309">whack</a>  (<a href="http://l.j-factor.com/nethack/whack.diff">mirror</a>)</dt>
    <dd>"The gnome hits!" is changed to a more descriptive verb based on the type of monster and what it's attacking with.</dd>
</dl>
<h2>Game over</h2>
<dl>
    <dt><a href="http://bilious.homelinux.org/?119">conducts</a></dt>
    <dd>Adds conducts for virginity, avoiding being human in Hell, never using conflict, sobriety, never using Elbereth, never wearing armor, and Zen (being blind the whole game).  Also shows time spent playing on the final conduct list.</dd>
    <dt><a href="http://www.netsonic.fi/~walker/nethack.html#dump">dumplog</a></dt>
    <dd>At the end of the game, everything shown to the player is dumped to a file: the final state of the map, the most recent messages, the player's inventory, conducts, known spells and skills, vanquished and extinct creatures, the death message, and the high score list.  This patch has also been updated to respect the new conducts added by the conducts patch.</dd>
    <dt><a href="http://bilious.homelinux.org/?170">epitaph</a></dt>
    <dd>When a player dies and will leave bones, the game now prompts for a custom epitaph to appear on the gravestone.  This epitaph only appears in a bones level, not on the high score board or in the log files.  As an added perk, the prompt for an epitaph makes it easy to tell if a particular game has left bones.</dd>
    <dt><a href="http://www.netsonic.fi/~walker/nethack.html#extborn">extborn</a></dt>
    <dd>At the end of the game, the list of vanquished and genocided creatures is extended to list how many of each creature have been born and which are extinct.</dd>
    <dt><a href="http://www.netsonic.fi/~walker/nethack.html#forgetquit">forgetquit</a></dt>
    <dd>Games ending in a <kbd>#quit</kbd> are not eligible to appear in the high score list.</dd>
    <dt><a href="http://www.netsonic.fi/~walker/nethack.html#helpless">helpless</a></dt>
    <dd>"while helpless" in death messages is replaced with a more informative description of exactly why the player was helpless.</dd>
    <dt><a href="http://sourceforge.net/apps/trac/unnethack/changeset/92">livelog</a></dt>
    <dd>Keeps a running log of the achievements added by <code>xlogfile</code> as they happen.</dd>
    <dt><a href="http://bilious.homelinux.org/?289">xlogfile</a></dt>
    <dd>Creates a secondary log of all played games that's easier to parse and includes conducts, number of turns, amount of time spent playing, the start and end times of the game, the player's starting gender and alignment, and any achievements (milestones within the plot, such as defeating Medusa or obtaining the Amulet).  This patch has also been updated to respect the new conducts added by the conducts patch.</dd>
</dl>
