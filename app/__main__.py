import os
from flask import Flask, session
from app.auth.osu import osu_oauth_blueprint

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(osu_oauth_blueprint, url_prefix="/auth")


@app.route("/")
def index():
	if 'username' in session:
		return f'Hello, {session["username"]}'
	else:
		return '<a href="/auth">Login</a>'

if __name__ == "__main__":
	app.run()
