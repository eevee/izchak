from izchak.tests import *

class TestDeathsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='deaths', action='list'))
        # Test response...
