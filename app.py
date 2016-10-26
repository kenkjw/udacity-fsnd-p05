from flask import Flask

from routes.catalog import catalog
from routes.users import users_bp

app = Flask(__name__)

app.register_blueprint(catalog)
app.register_blueprint(users_bp)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)