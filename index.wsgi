import sae
from ourgame import wsgi

application = sae.create_wsgi_app(wsgi.application)
