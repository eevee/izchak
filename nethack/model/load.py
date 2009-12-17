"""Script to load NetHack logs into a useful database form.

Doesn't actually use any part of Pylons.  The database URL is hard-coded.
"""

pylons_dir = '/home/eevee/nethack.veekun.com'
nethack_playground = '/opt/nethack.veekun.com/nethack/var'

from datetime import datetime, timedelta
import os.path
import re

import elixir
from sqlalchemy import create_engine, func

import nethack.model as model
from nethack.model import *

# Maps the epitaph text to my identifier
non_death_epitaphs = {
    u'quit':         u'quit',
    u'escaped':      u'escape',
    u'ascended':     u'ascension',
    u'a trickery':   u'trickery',
    u'panic':        u'panic',
}

def load_nethack_logfiles():
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

        elixir.session.commit()
