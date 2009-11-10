import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from nethack.lib.base import BaseController, render

log = logging.getLogger(__name__)

class GamesController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/games.mako')
        # or, return a response
        return 'Hello World'
