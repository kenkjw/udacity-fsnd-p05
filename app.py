from flask import Flask

from routes.catalog import Catalog
from routes.users import Users_bp
import config

app = Flask(__name__, static_folder='static', static_url_path='')

app.register_blueprint(Catalog)
app.register_blueprint(Users_bp)

from flask import session
from flask import render_template
@app.route('/debug')
def test():
    return render_template('debug.html')

if __name__ == '__main__':
    app.secret_key = config.secret_key
    app.debug = True
    app.run(host='0.0.0.0', port=8005)