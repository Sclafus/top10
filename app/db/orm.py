from datetime import datetime
from pony.orm import Database, Optional, PrimaryKey, Set, Required, db_session
from app.config.db import DBConfig
from app.api.osu import get_osu_user_info

db = Database()



class User(db.Entity):
	id = PrimaryKey(int, auto=True)
	user_id = Required(int, size=24, unique=True, unsigned=True)
	country_code = Required(str, 2)
	first_login = Optional(datetime)
	last_login = Optional(datetime, default=lambda: datetime.utcnow())
	votes = Set('Vote', reverse='user')
	voted_by = Set('Vote', reverse='voted_user')


class Vote(db.Entity):
	id = PrimaryKey(int, auto=True)
	timestamp = Required(datetime, default=lambda: datetime.utcnow())
	weight = Required(int, size=8, unsigned=True)
	user = Required(User, reverse='votes')
	voted_user = Required(User, reverse='voted_by')


def init(config: DBConfig) -> Database:
	db.bind(
		provider=config.provider,
		user=config.user,
		password=config.password,
		host=config.host,
		database=config.database
	)
	db.generate_mapping(create_tables=True)
	return db

class Top10DB:
	@staticmethod
	def add_user(user_id: int):
		with db_session:
			user_is_in_db: User = User.exists(user_id=user_id)
			if user_is_in_db:
				user = User.get(user_id=user_id)
				user.last_login = datetime.utcnow()
				return

			user_info = get_osu_user_info()
			country_code = user_info["country"]["code"]
			User(
				user_id=user_id,
				country_code=country_code,
				first_login=datetime.utcnow()
			)

	@staticmethod
	def cast_vote(user_id: int, voted_user_id: int):
		with db_session:
			user = User.get(user_id=user_id)
			voted_user = User.get(user_id=voted_user_id)
			Vote(user=user, voted_user=voted_user)
