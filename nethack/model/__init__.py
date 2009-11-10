"""The application's model objects"""
import elixir
from sqlalchemy.orm import scoped_session, sessionmaker

elixir.session = scoped_session(sessionmaker(autoflush=True,
                                             autocommit=False))

# shortnames turns class Foo into 'foo' rather than 'nethack_model_foo'
elixir.options_defaults.update({'shortnames': True})

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    elixir.session.configure(bind=engine)
    elixir.metadata.bind = engine


# Let elixir do its setup -- only after all the tables are defined
elixir.setup_all()
