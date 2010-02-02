import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
import formencode

from nethack import model
from nethack.lib.base import BaseController, render

log = logging.getLogger(__name__)

class DatabaseRowValidator(formencode.validators.FancyValidator):
    """Converts incoming values to a unique database row.

    Empty strings and None become None and are considered legal.
    """

    def __init__(self, table, column, *args, **kwargs):
        self._table = table
        self._column = column
        super(DatabaseRowValidator, self).__init__(*args, **kwargs)

    def _to_python(self, value, state):
        """Fetch a database row."""
        if not value:
            return None

        row = self._table.get_by(**{ self._column: value })
        if row:
            return row

        raise formencode.Invalid("No such {0}.".format(self._table.name.lower()))

    def _from_python(self, row, state):
        """Convert a database row back into a string."""
        if not row:
            return u''

        return getattr(row, self._column)

class GameSearchForm(formencode.Schema):
    if_key_missing = None

    # Allow extraneous junk, but remove it
    allow_extra_fields = True
    filter_extra_fields = True

    player = DatabaseRowValidator(model.Player, 'name', not_empty=False)
    role = DatabaseRowValidator(model.Role, 'name', not_empty=False)
    race = DatabaseRowValidator(model.Race, 'name', not_empty=False)
    gender = DatabaseRowValidator(model.Gender, 'name', not_empty=False)
    alignment = DatabaseRowValidator(model.Alignment, 'name', not_empty=False)


def options_from_table(table):
    """Given a table, returns a list of tuples for populating a <select>
    element.  Values are taken from the `name` column.
    """
    return [('', 'any')] + \
           [(row.name, row.name) for row in table.query.all()]

class GamesController(BaseController):

    def list(self):
        # Parse the form.  We don't really care if it doesn't validate; we'll
        # just ignore that field and show an error
        c.form = GameSearchForm(validate_partial_form=True)
        c.form_data = c.form.to_python(request.params)

        # Constant stuff the form needs to know
        c.role_options = options_from_table(model.Role)
        c.race_options = options_from_table(model.Race)
        c.gender_options = options_from_table(model.Gender)
        c.alignment_options = options_from_table(model.Alignment)

        query = model.Game.query

        # Perform filtering
        for column in ['player', 'role', 'race', 'gender', 'alignment']:
            if c.form_data[column]:
                query = query.filter_by(**{ column: c.form_data[column] })

        # Sort by most recent by default
        query = query.order_by(model.Game.end_time.desc())

        # TODO: paging
        c.games = query.all()

        return formencode.htmlfill.render(
            render('/games/list.mako'),
            c.form.from_python(c.form_data)
        )

    def view(self, name, id):
        """Show details for a particular game."""
        try:
            c.game = model.Game.get(id)
        except:
            abort(404)

        if c.game.player.name != name:
            abort(404)

        return render('/games/view.mako')
