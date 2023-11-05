from requests_oauthlib import OAuth2Session
from app.common import OAUTH_CONFIG
from flask import session

def get_osu_user_info(token: str = None) -> dict:
	osu = OAuth2Session(
		OAUTH_CONFIG.client_id,
		token=token or session["oauth_token"],
	)
	user_info = osu.get("https://osu.ppy.sh/api/v2/me").json()
	return user_info
