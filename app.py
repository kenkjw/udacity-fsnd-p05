from flask import Flask

from routes.catalog import Catalog
from routes.users import Users_bp
import config
import utils

app = Flask(__name__, static_folder='static', static_url_path='')

# Register blueprints
app.register_blueprint(Catalog)
app.register_blueprint(Users_bp)

# Load methods to use in jinja templates
app.jinja_env.globals.update(signed_in=utils.signed_in)

if __name__ == '__main__':
    app.secret_key = config.secret_key
    app.debug = True
    app.run(host='0.0.0.0', port=8005)
