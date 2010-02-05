"""The application's model objects"""
import elixir
from elixir import *
from sqlalchemy.orm import scoped_session, sessionmaker

elixir.session = scoped_session(sessionmaker(autoflush=True,
                                             autocommit=False))

# shortnames turns class Foo into 'foo' rather than 'izchak_model_foo'
elixir.options_defaults.update({'shortnames': True})

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    elixir.session.configure(bind=engine)
    elixir.metadata.bind = engine


### Tables with hard-coded data
class EntityPlusAbbreviation(EntityBase):
    """Entity base class that populates the 'abbreviation' column when rows are
    created.
    """
    __metaclass__ = EntityMeta

    def __init__(self, **kwargs):
        """Set abbreviation to the first three characters of the name."""
        super(EntityPlusAbbreviation, self).__init__(
            abbreviation=kwargs['name'][0:3],
            **kwargs
        )


class DungeonBranch(Entity):
    dnum = Field(Integer)
    short_name = Field(Unicode(8))
    name = Field(Unicode(32))

class EndType(Entity):
    """Identifies how a game ended: by quit, escape, death, or ascension."""
    identifier = Field(Unicode(16))

    games = OneToMany('Game')

    @property
    def name(self):
        """Alias for identifier, for consistency with most other tables."""
        return self.identifier

class Gender(EntityPlusAbbreviation):
    name = Field(Unicode(8))
    abbreviation = Field(Unicode(3))

    games = OneToMany('Game', inverse='gender')
    final_games = OneToMany('Game', inverse='final_gender')

class Race(EntityPlusAbbreviation):
    name = Field(Unicode(8))
    abbreviation = Field(Unicode(3))

    games = OneToMany('Game')

class Role(EntityPlusAbbreviation):
    name = Field(Unicode(16))
    abbreviation = Field(Unicode(3))

    games = OneToMany('Game')

class Alignment(EntityPlusAbbreviation):
    name = Field(Unicode(8))
    abbreviation = Field(Unicode(3))

    games = OneToMany('Game', inverse='alignment')
    final_games = OneToMany('Game', inverse='final_alignment')

class Conduct(Entity):
    flag_value = Field(Integer)
    identifier = Field(Unicode(16))
    description = Field(Unicode(64))

    games = ManyToMany('Game')

class Milestone(Entity):
    flag_value = Field(Integer)
    order = Field(Integer)
    identifier = Field(Unicode(16))
    description = Field(Unicode(64))

    games = ManyToMany('Game')


### Tables otherwise defined outside NetHack
class Player(Entity):
    """List of players is defined by dgl."""
    name = Field(Unicode(10))  # dgl limits to 10 chars


### Tables populated by NetHack logs
class Game(Entity):
    start_time      = Field(DateTime)
    end_time        = Field(DateTime, index=True)
    real_time       = Field(Interval)

    points          = Field(Integer)
    turns           = Field(Integer)
    final_dlvl      = Field(Integer)
    final_dungeon   = ManyToOne('DungeonBranch')
    deepest_dlvl    = Field(Integer)
    final_hp        = Field(Integer)
    max_hp          = Field(Integer)
    deaths          = Field(Integer)

    player          = ManyToOne('Player')
    role            = ManyToOne('Role')
    race            = ManyToOne('Race')
    gender          = ManyToOne('Gender')
    alignment       = ManyToOne('Alignment')
    final_gender    = ManyToOne('Gender')
    final_alignment = ManyToOne('Alignment')

    end_type        = ManyToOne('EndType')
    epitaph         = Field(Unicode(256))
    # This is the epitaph with any cruft (like 'while helpless') removed, to
    # make grouping by end reason simpler
    epitaph_simple  = Field(Unicode(256), index=True)

    conducts        = ManyToMany('Conduct')
    milestones      = ManyToMany('Milestone')


# Let elixir do its setup -- only after all the tables are defined
elixir.setup_all()
