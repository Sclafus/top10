from requests_oauthlib import OAuth2Session
from app.common import OAUTH_CONFIG

def get_osu_user_info(token: str):
	osu = OAuth2Session(
		OAUTH_CONFIG.client_id,
		token=token,
	)
	user_info = osu.get("https://osu.ppy.sh/api/v2/me").json()
	return user_info
