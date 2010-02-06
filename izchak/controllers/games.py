from datetime import datetime
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
import wtforms

from izchak import model
from izchak.lib.base import BaseController, render

log = logging.getLogger(__name__)

class DatabaseRowField(wtforms.fields.Field):
    """Converts incoming values to a unique database row.

    Empty strings and None become None and are considered legal.
    """

    def __init__(self, table, column, *args, **kwargs):
        super(DatabaseRowField, self).__init__(*args, **kwargs)
        self.table = table
        self.column = column

    def process_data(self, value):
        """'Process' the default value coming from the Form constructor."""
        self.data = value

    def process_formdata(self, valuelist):
        """Processes and loads the form value."""

        # Default of None
        if not valuelist or valuelist[0] == '':
            self.data = None
            return

        row = self.table.get_by(**{ self.column: valuelist[0] })
        if row:
            self.data = row
            return

        raise ValueError("No such {0}.".format( self.table.table.name.lower() ))


class DatabaseRowSelectField(DatabaseRowField, wtforms.fields.SelectField):
    """Puts every valid value in a select field."""
    def __init__(self, *args, **kwargs):
        super(DatabaseRowSelectField, self).__init__(*args, **kwargs)

        # Fetch the list of choices from the table
        self.values = []
        for row in self.table.query.all():
            self.values.append( getattr(row, self.column) )

    def pre_validate(self, form):
        """Override the usual SelectField validator, which checks whether the
        value is in its choices.  process_formdata does the validation for us.
        """
        pass

    def iter_choices(self):
        """Yields the items in the selectbox (and whether they're selected)."""
        if self.data is None:
            current_value = None
        else:
            current_value = getattr(self.data, self.column)

        # Default value
        yield u'', u'any', current_value is None

        for value in self.values:
            yield value, value, value == current_value


class DatabaseRowTextField(DatabaseRowField, wtforms.fields.TextField):
    """Requires the user to enter something in a text field."""
    def _value(self):
        """Converts Python value back to a form value."""
        if self.data is None:
            return u''
        else:
            return getattr(self.data, self.column)


class GameSearchForm(wtforms.Form):
    player = DatabaseRowTextField(model.Player, 'name')
    role = DatabaseRowSelectField(model.Role, 'name')
    race = DatabaseRowSelectField(model.Race, 'name')
    gender = DatabaseRowSelectField(model.Gender, 'name')
    alignment = DatabaseRowSelectField(model.Alignment, 'name')


class GamesController(BaseController):

    def list(self):
        # Parse the form.  We don't really care if it doesn't validate; we'll
        # just ignore that field and show an error
        c.form = GameSearchForm(
            request.params,

            # Defaults
            player=None,
            role=None,
            race=None,
            gender=None,
            alignment=None,
        )
        c.form.validate()

        # Perform filtering
        query = model.Game.query

        print c.form.data
        for column in ['player', 'role', 'race', 'gender', 'alignment']:
            if c.form[column].data:
                query = query.filter_by(**{ column: c.form[column].data })

        # Sort by most recent by default
        query = query.order_by(model.Game.end_time.desc())

        # TODO: paging
        c.games = query.all()

        return render('/games/list.mako')

    def view(self, name, end_time):
        """Show details for a particular game, selected by end timestamp."""

        end_datetime = datetime.fromtimestamp( int(end_time) )

        try:
            c.game = model.Game.query \
                .join(model.Player) \
                .filter(model.Player.name == name) \
                .filter(model.Game.end_time == end_datetime) \
                .one()
        except:
            abort(404)

        return render('/games/view.mako')
