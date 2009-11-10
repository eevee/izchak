"""The application's model objects"""
import elixir
from elixir import *
from sqlalchemy.orm import scoped_session, sessionmaker

elixir.session = scoped_session(sessionmaker(autoflush=True,
                                             autocommit=False))

# shortnames turns class Foo into 'foo' rather than 'nethack_model_foo'
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
    name = Field(Unicode(32))

class EndType(Entity):
    identifier = Field(Unicode(16))

class Gender(EntityPlusAbbreviation):
    name = Field(Unicode(8))
    abbreviation = Field(Unicode(3))

class Race(EntityPlusAbbreviation):
    name = Field(Unicode(8))
    abbreviation = Field(Unicode(3))

class Role(EntityPlusAbbreviation):
    name = Field(Unicode(16))
    abbreviation = Field(Unicode(3))

class Alignment(EntityPlusAbbreviation):
    name = Field(Unicode(8))
    abbreviation = Field(Unicode(3))

class Conduct(Entity):
    flag_value = Field(Integer)
    identifier = Field(Unicode(16))
    description = Field(Unicode(64))

class Milestone(Entity):
    flag_value = Field(Integer)
    order = Field(Integer)
    identifier = Field(Unicode(16))
    description = Field(Unicode(64))


### Tables otherwise defined outside NetHack
class Player(Entity):
    """List of players is defined by dgl."""
    name = Field(Unicode(10))  # dgl limits to 10 chars


### Tables populated by NetHack logs
class Game(Entity):
    points          = Field(Integer)
    final_dlvl      = Field(Integer)
    final_dungeon   = ManyToOne('DungeonBranch')
    deepest_dlvl    = Field(Integer)
    final_hp        = Field(Integer)
    max_hp          = Field(Integer)
    deaths          = Field(Integer)
    start_time      = Field(DateTime)
    end_time        = Field(DateTime)
    role            = ManyToOne('Role')
    race            = ManyToOne('Race')
    gender          = ManyToOne('Gender')
    alignment       = ManyToOne('Alignment')
    final_gender    = ManyToOne('Gender')
    final_alignment = ManyToOne('Alignment')
    player          = ManyToOne('Player')
    turns           = Field(Integer)
    real_time       = Field(Interval)
    end_type        = ManyToOne('EndType')
    end_reason      = Field(Unicode(256))
    end_killer      = Field(Unicode(256), nullable=True)
    end_killer_name = Field(Unicode(256), nullable=True)
    end_helpless    = Field(Unicode(256), nullable=True)

    conducts        = ManyToMany('Conduct')
    milestones      = ManyToMany('Milestone')


# Let elixir do its setup -- only after all the tables are defined
elixir.setup_all()
