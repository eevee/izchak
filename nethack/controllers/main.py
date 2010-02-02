import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from nethack.lib.base import BaseController, render

log = logging.getLogger(__name__)

class MainController(BaseController):

    def index(self):
        """Main page, with a server overview and some links and whatever."""
        return render('/index.mako')

    def trophy(self):
        """The nethack.veekun.com trophy gallery."""
        return render('/trophy.mako')
