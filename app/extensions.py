from flask_assets import Environment
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_rq2 import RQ
from flask_travis import Travis
from werkzeug.contrib.cache import SimpleCache

assets = Environment()
babel = Babel()
bcrypt = Bcrypt()
cache = SimpleCache()
limiter = Limiter(key_func=get_remote_address)
lm = LoginManager()
mail = Mail()
migrate = Migrate()
rq = RQ()
travis = Travis()
