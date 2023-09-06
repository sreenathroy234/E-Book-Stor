from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os
from werkzeug.utils import import_string, secure_filename
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_msearch import Search


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SECRET_KEY']="key"
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
search = Search()
search.init_app(app)

migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = u"Please login first"

from utils.admin import routes
from utils.products import routes
from utils.carts import carts
from utils.customers import routes