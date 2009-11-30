import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from nethack import model
from nethack.lib.base import BaseController, render

log = logging.getLogger(__name__)

class GamesController(BaseController):

    def list(self):
        # Sort by most recent by default
        c.games = model.Game.query.order_by(model.Game.end_time.desc()).all()
        return render('/games/list.mako')
