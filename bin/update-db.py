#!/usr/bin/env python
"""Script to load NetHack logs into a useful database form.  Intended to be
left running in the background; it will check for new deaths periodically.  It
puts its pid in /var/tmp/izchak-update-db.pid, which can be used for restarting
it when necessary.

This script works incrementally; any records before the latest one in the
database are ignored.  New players are likewise loaded incrementally.

The location of the database and playground and the uid of the games user are
currently, alas, hard-coded.  This is a bug.

Make sure you run setup-app before running this!  It needs the tables and base
data (like death types) to be set up first!
"""

from datetime import datetime, timedelta
import os
import os.path
import re
import sqlite3
import subprocess
import sys
import time

import elixir
from sqlalchemy import create_engine, func

import izchak.model
from izchak.model import *

# Maps the epitaph text to my identifier
non_death_epitaphs = {
    u'quit':        u'quit',
    u'escaped':     u'escape',
    u'ascended':    u'ascension',
    u'a trickery':  u'trickery',
    u'panic':       u'panic',

    # Less obvious epitaphs
    u'escaped (in celestial disgrace)':
                    u'escape',
    u'escaped (with a fake Amulet)':
                    u'escape',
    # Levelport to -10 or above
    u'went to heaven prematurely':
                    u'escape',
}


# Constants
PIDFILE = '/var/tmp/izchak-update-db.pid'
PYLONS_DIR = '/home/eevee/nethack.veekun.com/izchak'
DATABASE_URL = 'postgres://@/izchak'
DGLDIR = '/opt/nethack.veekun.com/dgldir'
NETHACK_PLAYGROUND = '/opt/nethack.veekun.com/nethack/var'

# Globals!  Oh, no!
izchak_engine = None
dgl_connection = None
xlog_file = None
last_dgl_user_id = None

def init():
    """Connect to respective databases and remember latest games and players we
    know about.
    """
    # Connect to the main database
    global izchak_engine
    izchak_engine = create_engine(DATABASE_URL)
    izchak.model.init_model(izchak_engine)

    # Connect to the dgamelaunch database and get the id of the latest user we
    # know about.  This assumes that users are created in the same order in
    # both databases!
    global dgl_connection
    global last_dgl_user_id
    dgl_connection = sqlite3.connect( os.path.join(DGLDIR, 'dgamelaunch.db') )

    last_user = Player.query.order_by(Player.id.desc()).first()
    if last_user:
        cursor = dgl_connection.cursor()
        cursor.execute("SELECT id FROM dglusers WHERE name = ?",
                       (last_user.name,))
        (last_dgl_user_id,) = cursor.fetchone()


    # Check for the latest game
    last_game = Game.query.order_by(Game.end_time.desc()).first()

    # Open the xlog!
    global xlog_file
    xlog_file = open( os.path.join(NETHACK_PLAYGROUND, 'xlogfile') )

    # Need to scroll through the log and skip all the log entries we've already
    # seen.  The next line read (if any) should be the first new one.

    # Last game's player and timestamp should uniquely identify it in the log.
    # It's possible for two games to end in the same second, but extremely
    # unlikely that two games by the same player will end in the same second.
    # Izchak makes this assumption elsewhere, anyway.
    if last_game:
        last_game_name = last_game.player.name
        last_game_time = last_game.end_time.strftime('%s')  # unix time
        last_game_match = False
        for record in xlog_file:
            data = parse_logfile_record(record)

            # If this matches the last game we saw, hooray!  We're far enough
            # through the file
            if data['name'] == last_game_name \
                and data['endtime'] == last_game_time:

                # Next line is new, so just break here
                last_game_match = True
                break

        # If there were no matches at all in the file, then either someone has
        # tampered with the log (unlikely) or everything in it is new (somewhat
        # likely).  It's possible to check for older timestamps than we have
        # now, but that's a lot of work for something that really shouldn't
        # happen.  So, don't mess with the log file.
        # TODO: Fix this sometime.
        if not last_game_match:
            xlog_file.seek(0, os.SEEK_SET)

    # The stage is now set for the first update!


def check_for_updates():
    """Checks the user database and logfiles for new stuff."""

    # Check users first, in case a new game is from a new user!
    global last_dgl_user_id
    cursor = dgl_connection.cursor()
    cursor.execute(
        "SELECT id, username FROM dglusers WHERE id > ? ORDER BY id",
        (last_dgl_user_id or 0,)
    )
    for id, name in cursor:
        last_dgl_user_id = id
        add_player(name)

    elixir.session.commit()


    # Check for new games
    xlog_file.seek(0, os.SEEK_CUR)  # reset EOF
    for record in xlog_file:
        data = parse_logfile_record(record)
        add_game(data)

    elixir.session.commit()


def add_player(name):
    Player(name=unicode(name))


def add_game(logdata):
    # Only count games from uid 5, which is games.  There are some logs of
    # root, which are just from testing crashes
    if int(logdata['uid']) != 5:
        return

    epitaph = logdata['death']
    epitaph_simple = epitaph

    # Pick the end-of-the-game type.  Most of these are deaths.
    if epitaph in non_death_epitaphs:
        end_type = EndType.query \
                          .filter_by(identifier=
                                     non_death_epitaphs[epitaph]) \
                          .one()
    else:
        end_type = EndType.query.filter_by(identifier=u'death').one()

        # Strip out irrelevant differences between otherwise identical
        # reasons for dying
        epitaph_simple = re.sub(u' \(with the Amulet\)$', '', epitaph_simple)
        epitaph_simple = re.sub(u', while (.+?)$', '', epitaph_simple)
        epitaph_simple = re.sub(u' called (.+?)$', '', epitaph_simple)
        epitaph_simple = re.sub(u' named (.+?)$', '', epitaph_simple)
        epitaph_simple = re.sub(u' invisible ', ' ', epitaph_simple)
        epitaph_simple = re.sub(u' hallucinogen-distorted ', ' ', epitaph_simple)
        epitaph_simple = re.sub(u'by (.+?), the shopkeeper', 'by a shopkeeper', epitaph_simple)
        epitaph_simple = re.sub(u' (him|her)self ', ' him/herself ', epitaph_simple)
        epitaph_simple = re.sub(u' (his|her) ', ' his/her ', epitaph_simple)

    # Load the rest of the data, more or less verbatim, into a Game row
    game = Game(
        start_time      = datetime.fromtimestamp(int(logdata['starttime'])),
        end_time        = datetime.fromtimestamp(int(logdata['endtime'])),
        real_time       = timedelta(seconds=int(logdata['realtime'])),

        points          = logdata['points'],
        turns           = logdata['turns'],
        final_dlvl      = logdata['deathlev'],
        final_dungeon   = DungeonBranch.query.filter_by(
                            dnum=logdata['deathdnum']).one(),
        deepest_dlvl    = logdata['maxlvl'],
        final_hp        = logdata['hp'],
        max_hp          = logdata['maxhp'],
        deaths          = logdata['deaths'],

        player          = Player.query.filter_by(
                            name=logdata['name']).one(),
        role            = Role.query.filter_by(
                            abbreviation=logdata['role']).one(),
        race            = Race.query.filter_by(
                            abbreviation=logdata['race']).one(),
        gender          = Gender.query.filter_by(
                            abbreviation=logdata['gender0']).one(),
        alignment       = Alignment.query.filter_by(
                            abbreviation=logdata['align0']).one(),
        final_gender    = Gender.query.filter_by(
                            abbreviation=logdata['gender']).one(),
        final_alignment = Alignment.query.filter_by(
                            abbreviation=logdata['align']).one(),

        end_type        = end_type,
        epitaph         = epitaph,
        epitaph_simple  = epitaph_simple,
    )

    ### Break apart the conduct and milestone bitfields
    conduct_bitfield = int(logdata['conduct'], 16)
    for conduct in Conduct.query.all():
        if conduct_bitfield & conduct.flag_value:
            game.conducts.append(conduct)

    milestone_bitfield = int(logdata['achieve'], 16)
    for milestone in Milestone.query.all():
        if milestone_bitfield & milestone.flag_value:
            game.milestones.append(milestone)

    # Done


### Utility functions

def parse_logfile_record(record):
    # key1=val1:key2=val2:...
    data = {}
    for chunk in record.strip().split(':'):
        k, v = chunk.split('=', 1)
        data[k] = unicode(v)

    return data


### Entry

def main():
    init()

    # See if we're already running
    if os.path.exists(PIDFILE):
        pidfile = open(PIDFILE)
        pid = pidfile.readline()
        pid = pid.strip()
        if subprocess.call(['ps', '-p', pid]) == 0:
            sys.stderr.write("Already running!")
            sys.exit(1)
        pidfile.close()

    # Save pid
    pidfile = open(PIDFILE, 'w')
    pidfile.write( str(os.getpid()) )
    pidfile.close()

    # Event loop
    while True:
        check_for_updates()
        time.sleep(10)


if __name__ == '__main__':
    main()
