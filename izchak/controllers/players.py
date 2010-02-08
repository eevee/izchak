import elixir
import logging
from sqlalchemy import and_, func

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from izchak import model
from izchak.lib.base import BaseController, render

log = logging.getLogger(__name__)

class PlayersController(BaseController):

    def list(self):
        c.players = model.Player.query.order_by(
            func.lower(model.Player.name).asc()
        ).all()
        return render('/players/list.mako')

    def view(self, name):
        try:
            c.player = model.Player.query.filter_by(name=name).one()
        except:
            abort(404)

        games_q = model.Game.query.filter_by(player=c.player)

        # Pull some simple stats
        c.game_count = games_q.count()

        # Count how this player's games are distributed across various
        # categories
        session = elixir.session
        count = func.count(model.Game.id).label('count')
        c.breakdowns = {}  # label => [(table, count), ...]
        for table, label in [
            (model.EndType,   'Ending'),
            (model.Role,      'Role'),
            (model.Race,      'Race'),
            (model.Gender,    'Gender'),
            (model.Alignment, 'Alignment'),
        ]:
            # Create a LEFT JOIN to get all of this player's games without
            # eliminating options s/he has never used
            # property.primaryjoin mumbo-jumbo courtsey of:
            # http://www.mail-archive.com/sqlalchemy@googlegroups.com/msg16304.html
            join = and_(getattr(table, 'games').property.primaryjoin,
                        model.Game.player == c.player)

            # To be correct, the query must get the ids and their counts, then
            # join THAT again to get the full table rows.
            # Excellent subquery example from:
            # http://www.sqlalchemy.org/docs/ormtutorial.html#using-subqueries
            subq = session.query(table.id.label('table_id'), count) \
                .outerjoin((model.Game, join)) \
                .group_by(table.id) \
                .subquery()

            q = session.query(table, subq.c.count) \
                .outerjoin((subq, table.id == subq.c.table_id)) \
                .order_by(subq.c.count.desc())

            c.breakdowns[label] = q.all()

        return render('/players/view.mako')
