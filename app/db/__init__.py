from pony.orm import Database
from app.common import DB_CONFIG

db = Database()

db.bind(
	provider=DB_CONFIG.provider,
	user=DB_CONFIG.user,
	password=DB_CONFIG.password,
	host=DB_CONFIG.host,
	database=DB_CONFIG.database
)

print()
