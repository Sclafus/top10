from datetime import datetime
from pony.orm import Database, Optional, PrimaryKey, Set, Required, db_session, LongStr
from app.config.db import DBConfig
from app.api.osu import get_logged_in_user_info

db = Database()


class User(db.Entity):
	id = PrimaryKey(int, auto=True)
	user_id = Required(int, size=32, unique=True, unsigned=True)
	country_code = Required(str, 2)
	is_votable = Required(bool)
	first_login = Optional(datetime)
	last_login = Optional(datetime)
	scores = Set('Score')
	votes = Set('Vote', reverse='user')
	voted_by = Set('Vote', reverse='voted_user')

class Vote(db.Entity):
	id = PrimaryKey(int, auto=True)
	timestamp = Required(datetime, default=lambda: datetime.utcnow())
	weight = Required(int, size=8, unsigned=True)
	user = Required(User, reverse='votes')
	voted_user = Required(User, reverse='voted_by')

class Score(db.Entity):
	id = PrimaryKey(int, auto=True)
	link = Optional(str)
	user = Required(User)
	comment = Optional(LongStr)


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
	def add_current_user(user_id: int):
		with db_session:
			user_already_in_db: bool = User.exists(user_id=user_id)

			if user_already_in_db:
				user = User.get(user_id=user_id)
				user.last_login = datetime.utcnow()
				if user.first_login is None:
					user.first_login = user.last_login

				user_info = get_logged_in_user_info()
				country_rank = user_info['statistics']['country_rank']
				user.is_votable = country_rank <= 200
				return

			user_info = get_logged_in_user_info()
			country_code = user_info["country"]["code"]
			timestamp = datetime.utcnow()
			User(
				user_id=user_id,
				country_code=country_code,
				first_login=timestamp,
				last_login=timestamp,
				votable=None
			)

	@staticmethod
	def cast_vote(user_id: int, voted_user_id: int, weight: int):
		with db_session:
			user = User.get(user_id=user_id)
			voted_user = User.get(user_id=voted_user_id)
			Vote(user=user, voted_user=voted_user, weight=weight)

	@staticmethod
	def add_votable_users_bulk(user_infos: list[dict]):
		with db_session:
			for user_info in user_infos:
				user_already_in_db: bool = User.exists(user_id=user_info["id"])
				if user_already_in_db:
					user = User.get(user_id=user_info["id"])
					user.is_votable = True
					continue

				User(
					user_id=user_info["id"],
					country_code=user_info["country"]["code"],
					is_votable=True
				)
