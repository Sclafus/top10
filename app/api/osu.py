from requests_oauthlib import OAuth2Session
from app.common import OAUTH_CONFIG
from flask import session

def get_logged_in_user_info(token: str = None) -> dict:
	osu = OAuth2Session(
		OAUTH_CONFIG.client_id,
		token=token or session["oauth_token"],
	)
	user_info = osu.get("https://osu.ppy.sh/api/v2/me").json()
	return user_info


def get_top_players(token: str = None, players: int = 50, **kwargs) -> dict:
	page_size = 50
	result = []
	osu = OAuth2Session(
		OAUTH_CONFIG.client_id,
		token=token or session["oauth_token"],
	)

	# Get an extra page if the number of players is not a multiple of the page size
	pages_to_get, player_out_of_page = divmod(players, page_size)
	if player_out_of_page > 0:
		pages_to_get += 1

	for i in range(pages_to_get):
		kwargs["page"] = i + 1
		page = osu.get("https://osu.ppy.sh/api/v2/rankings/osu/performance", params=kwargs).json()
		result.extend([user_profile["user"] for user_profile in page["ranking"]])
	return result
