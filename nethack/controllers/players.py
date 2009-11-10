import logging
from sqlalchemy import func

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from nethack import model
from nethack.lib.base import BaseController, render

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

        return render('/players/view.mako')
