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
            func.count(Game.id)   .label('count'),
            func.sum(Game.points) .label('total_points'),
            ) \
            .group_by(Game.epitaph_simple) \
            .order_by(func.count(Game.id).desc())

        c.deaths = q.all()

        return render('/deaths.mako')
