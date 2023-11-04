import os
from attrs import define, field

@define(slots=True)
class DBConfig:
	provider: str = field(default=os.getenv("DATABASE_PROVIDER"))
	user: str = field(default=os.getenv("DATABASE_USER"))
	password: str = field(default=os.getenv("DATABASE_PASSWORD"))
	host: str = field(default=os.getenv("DATABASE_HOST"))
	database: str = field(default=os.getenv("DATABASE_NAME"))
