from app.config.oauth import OAuthConfig
from app.config.db import DBConfig

OAUTH_CONFIG = OAuthConfig()
DB_CONFIG = DBConfig()

from app.db.orm import init  # noqa: E402
db = init(DB_CONFIG)
