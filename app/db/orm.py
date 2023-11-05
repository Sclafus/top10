from pony.orm import Database, PrimaryKey, Set, Required, db_session

from app.config.db import DBConfig


db = Database()


class User(db.Entity):
	id = PrimaryKey(int, auto=True)
	user_id = Required(int)
	votes = Set('Vote')


class Vote(db.Entity):
	id = PrimaryKey(int, auto=True)
	user = Required(User)


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

	@db_session
	@staticmethod
	def add_user(user_id: int):
		user_in_db: User = User.get(user_id=user_id)
		if user_in_db:
			return

		User(user_id=user_id)
