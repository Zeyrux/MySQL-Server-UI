import mimetypes

from application.backend import App


mimetypes.add_type("application/javascript", ".js")
application = App().app
application.debug = True
