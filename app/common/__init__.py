from app.config.oauth import OAuthConfig
from app.config.db import DBConfig
from app.db.orm import init

OAUTH_CONFIG = OAuthConfig()
DB_CONFIG = DBConfig()
db = init(DB_CONFIG)
