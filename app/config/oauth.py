import os
from attrs import define, field

@define(slots=True, frozen=True)
class OAuthConfig:
	client_id: str = field(default=os.getenv("OAUTH_CLIENT_ID"))
	client_secret: str = field(default=os.getenv("OAUTH_CLIENT_SECRET"))
	authorization_url: str = field(default='https://osu.ppy.sh/oauth/authorize')
	token_url: str = field(default='https://osu.ppy.sh/oauth/token')
