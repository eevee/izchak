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

    player = DatabaseRowValidator(model.Player, 'name', not_empty=False)


class GamesController(BaseController):

    def list(self):
        # Parse the form.  We don't really care if it doesn't validate; we'll
        # just ignore that field and show an error
        c.form = GameSearchForm()
        form_data = c.form.to_python(request.params)

        query = model.Game.query

        # Perform filtering
        if form_data['player']:
            query = query.filter_by(player=form_data['player'])

        # Sort by most recent by default
        query = query.order_by(model.Game.end_time.desc())

        # TODO: paging
        c.games = query.all()

        return formencode.htmlfill.render(
            render('/games/list.mako'),
            c.form.from_python(form_data)
        )
