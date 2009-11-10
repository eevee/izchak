from nethack.tests import *

class TestGamesController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='games', action='index'))
        # Test response...
