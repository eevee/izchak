"""Script to load NetHack logs into a useful database form.

Doesn't actually use any part of Pylons.  The database URL is hard-coded.
"""

pylons_dir = '/home/eevee/nethack.veekun.com'
nethack_playground = '/opt/nethack.veekun.com/nethack/var'

from datetime import datetime, timedelta
import os.path

import elixir
from sqlalchemy import create_engine, func

import nethack.model as model
from nethack.model import *

engine = create_engine("sqlite:///{0}/development.db".format(pylons_dir))
init_model(engine)

for line in open(os.path.join(nethack_playground, 'xlogfile')):
    # Parse line: a=b:c=d:e=f
    logdata = {}
    for chunk in line.strip().split(':'):
        k, v = chunk.split('=', 1)
        logdata[k] = unicode(v)

    # Only count games from uid 5, which is games.  There are some logs of
    # root, which are just from testing crashes
    if int(logdata['uid']) != 5:
        continue

    end_reason = logdata['death']
    # Death reasons look like:
    # "quit"
    # "escaped"
    # "ascended"
    # killed by {end_killer} called {end_killer_name}, while {end_helpless}
    end_killer = None
    end_killer_name = None
    end_helpless = None
    if end_reason == 'quit':
        end_type = EndType.query.filter_by(identifier=u'quit').one()
    elif end_reason == 'escaped':
        end_type = EndType.query.filter_by(identifier=u'escape').one()
    elif end_reason == 'ascended':
        end_type = EndType.query.filter_by(identifier=u'ascension').one()
    else:
        end_type = EndType.query.filter_by(identifier=u'death').one()

        # Lop off "killed by " -- 10 characters
        temp_reason = end_reason[10:]
        if ', while ' in temp_reason:
            temp_reason, end_helpless = temp_reason.rsplit(', while ', 1)

        if ' called ' in temp_reason:
            temp_reason, end_killer_name = temp_reason.split(' called ', 1)

        end_killer = temp_reason


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
        end_reason      = logdata['death'],
        end_killer      = end_killer,
        end_killer_name = end_killer_name,
        end_helpless    = end_helpless,
    )

    conduct_bitfield = int(logdata['conduct'], 16)
    for conduct in Conduct.query.all():
        if conduct_bitfield & conduct.flag_value:
            game.conducts.append(conduct)

    milestone_bitfield = int(logdata['achieve'], 16)
    for milestone in Milestone.query.all():
        if milestone_bitfield & milestone.flag_value:
            game.milestones.append(milestone)

    elixir.session.commit()
