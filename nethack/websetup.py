"""Setup the nethack application"""
import logging
import os

import elixir

from nethack import model
from nethack.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup nethack here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    elixir.metadata.create_all()

    ### Load static data
    model.Gender(name='Male')
    model.Gender(name='Female')

    model.Race(name='Human')
    model.Race(name='Dwarf')
    model.Race(name='Elf')
    model.Race(name='Gnome')
    model.Race(name='Orc')

    model.Role(name='Archeologist')
    model.Role(name='Barbarian')
    model.Role(name='Caveman')
    model.Role(name='Healer')
    model.Role(name='Knight')
    model.Role(name='Monk')
    model.Role(name='Priest')
    model.Role(name='Ranger')
    model.Role(name='Rogue')
    model.Role(name='Samurai')
    model.Role(name='Tourist')
    model.Role(name='Valkyrie')
    model.Role(name='Wizard')

    model.Alignment(name='Lawful')
    model.Alignment(name='Neutral')
    model.Alignment(name='Chaotic')

    # Dungeon branches, taken from dat/dungeon.def and parsexlog.pl
    model.DungeonBranch(dnum=0, name='the Dungeons of Doom')
    model.DungeonBranch(dnum=1, name='Gehennom')
    model.DungeonBranch(dnum=2, name='the Gnomish Mines')
    model.DungeonBranch(dnum=3, name='the Quest')
    model.DungeonBranch(dnum=4, name='Sokoban')
    model.DungeonBranch(dnum=5, name='Fort Ludios')
    model.DungeonBranch(dnum=6, name="Vlad's Tower")
    model.DungeonBranch(dnum=7, name='the Elemental Planes')

    model.EndType(identifier='death')
    model.EndType(identifier='quit')
    model.EndType(identifier='escape')
    model.EndType(identifier='ascension')

    # Conducts taken from src/topten.c
    model.Conduct(flag_value=0x00001, identifier='foodless',
                  description='Never ate food')
    model.Conduct(flag_value=0x00002, identifier='vegan',
                  description='Never ate animal products')
    model.Conduct(flag_value=0x00004, identifier='vegetarian',
                  description='Never ate meat')
    model.Conduct(flag_value=0x00008, identifier='atheist',
                  description='Ignored the gods')
    model.Conduct(flag_value=0x00010, identifier='weaponless',
                  description='Never hit with a wielded weapon')
    model.Conduct(flag_value=0x00020, identifier='pacifist',
                  description='Never killed a monster')
    model.Conduct(flag_value=0x00040, identifier='illiterate',
                  description='Never read anything')
    model.Conduct(flag_value=0x00080, identifier='polypileless',
                  description='Never polymorphed an object')
    model.Conduct(flag_value=0x00100, identifier='polyselfless',
                  description='Never polymorphed')
    model.Conduct(flag_value=0x00200, identifier='wishless',
                  description='Never made a wish')
    model.Conduct(flag_value=0x00400, identifier='artiwishless',
                  description='Never wished for an artifact')
    model.Conduct(flag_value=0x00800, identifier='genocideless',
                  description='Never caused genocide')

    model.Conduct(flag_value=0x01000, identifier='celibate',
                  description="Never lay in a foocubus's arms")
    model.Conduct(flag_value=0x02000, identifier='hellless',
                  description='Never entered Hell in human form')
    model.Conduct(flag_value=0x04000, identifier='conflictless',
                  description='Never caused conflict')
    model.Conduct(flag_value=0x08000, identifier='sober',
                  description='Never imbibed alcohol')
    model.Conduct(flag_value=0x10000, identifier='elberethless',
                  description='Never used the divine word')
    model.Conduct(flag_value=0x20000, identifier='armorless',
                  description='Never wore armor')
    model.Conduct(flag_value=0x40000, identifier='zen',
                  description='Never had sight')

    # "Achievements" from xlogfile, taken from src/topten.c
    model.Milestone(flag_value=1 << 0, order=3, identifier='bell',
                    description='Completed the Quest')
    model.Milestone(flag_value=1 << 1, order=5, identifier='gehennom',
                    description='Entered Gehennom')
    model.Milestone(flag_value=1 << 2, order=6, identifier='candelabrum',
                    description='Defeated Vlad')
    model.Milestone(flag_value=1 << 3, order=7, identifier='book',
                    description='Defeated the Wizard of Yendor')
    model.Milestone(flag_value=1 << 4, order=8, identifier='invocation',
                    description='Performed the Invocation')
    model.Milestone(flag_value=1 << 5, order=9, identifier='amulet',
                    description='Obtained the Amulet')
    model.Milestone(flag_value=1 << 6, order=10, identifier='planes',
                    description='Entered the Planes')
    model.Milestone(flag_value=1 << 7, order=11, identifier='astral',
                    description='Reached the Astral Plane')
    model.Milestone(flag_value=1 << 8, order=12, identifier='ascended',
                    description='Ascended to Demigod(dess)hood')
    model.Milestone(flag_value=1 << 9, order=1, identifier='mines',
                    description='Completed the Mines')
    model.Milestone(flag_value=1 << 10, order=2, identifier='sokoban',
                    description='Completed Sokoban')
    model.Milestone(flag_value=1 << 11, order=4, identifier='medusa',
                    description='Slew Medusa')

    ### Less hard-coded things not taken directly from the game
    for name in os.listdir('/opt/nethack.veekun.com/dgldir/userdata'):
        model.Player(name=name)

    elixir.session.commit()
