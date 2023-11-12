from flask import Blueprint, request, session, redirect
from requests_oauthlib import OAuth2Session
from app.common import OAUTH_CONFIG
from app.api.osu import get_logged_in_user_info
from app.db.orm import Top10DB

osu_oauth_blueprint = Blueprint("auth", __name__)


@osu_oauth_blueprint.route("/")
def login():
	osu = OAuth2Session(
		OAUTH_CONFIG.client_id,
		redirect_uri=request.url + "callback",
		scope="public identify",
	)
	authorization_url, state = osu.authorization_url(
		OAUTH_CONFIG.authorization_url
	)
	session["oauth_state"] = state
	return redirect(authorization_url)

@osu_oauth_blueprint.route("/callback")
def callback():
	osu = OAuth2Session(
		OAUTH_CONFIG.client_id,
		state=session["oauth_state"],
		redirect_uri=request.base_url,
	)
	token = osu.fetch_token(
		OAUTH_CONFIG.token_url,
		client_secret=OAUTH_CONFIG.client_secret,
		authorization_response=request.url,
		include_client_id=True,
	)
	session["oauth_token"] = token

	user_info = get_logged_in_user_info()
	user_id = user_info["id"]
	username = user_info["username"]

	Top10DB.add_current_user(user_id)

	session["user_id"] = user_id
	session["username"] = username
	return redirect("/")

@osu_oauth_blueprint.route("/logout")
def logout():
	session.pop("username", None)
	session.pop("oauth_state", None)
	session.pop("oauth_token", None)
	return redirect("/")
