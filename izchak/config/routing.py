"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    map.connect('/', controller='main', action='index')
    map.connect('/trophy', controller='main', action='trophy')

    map.connect('/players', controller='players', action='list')
    map.connect('/players/{name}', controller='players', action='view')
    map.connect('/players/{name}/games', controller='players', action='games')

    map.connect('/games', controller='games', action='list')
    map.connect('/players/{name}/games/{end_time}', controller='games', action='view')

    map.connect('/deaths', controller='deaths', action='list')

    return map
