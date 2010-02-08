import elixir
import logging
from sqlalchemy import func

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from izchak.lib.base import BaseController, render
from izchak.model import EndType, Game

log = logging.getLogger(__name__)

class DeathsController(BaseController):

    def list(self):
        q = elixir.session.query(
            Game.epitaph_simple,
            EndType.identifier          .label('end_type_identifier'),
            func.count(Game.id)         .label('count'),
            func.sum(Game.points)       .label('total_points'),
            func.avg(Game.points)       .label('average_points'),
            func.max(Game.deepest_dlvl) .label('max_dlvl'),
            func.avg(Game.deepest_dlvl) .label('average_dlvl'),
            ) \
            .join(Game.end_type) \
            .group_by(Game.epitaph_simple,
                      EndType.identifier) \
            .order_by(func.count(Game.id).desc(),
                      Game.epitaph_simple.asc())

        c.deaths = q.all()

        return render('/deaths.mako')
