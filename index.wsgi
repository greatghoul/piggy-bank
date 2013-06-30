import sae

from piggybank import app

application = sae.create_wsgi_app(app)
