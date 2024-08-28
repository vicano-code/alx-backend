#!/usr/bin/env python3
"""Basic Flask App
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext
from typing import Union

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """confugure available languages in app and set defaults"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@app.before_request
def before_request(login_as: int = None):
    """function to execute before making request"""
    user: dict = get_user()
    print(user)
    g.user = user


def get_user() -> Union[dict, None]:
    """returns a dictionary of the user obj props or None"""
    login_user = request.args.get('login_as', None)

    if login_user is None:
        return None

    user: dict = {}
    user[login_user] = users.get(int(login_user))

    return user[login_user]


@babel.localeselector
def get_locale():
    """Get locale from request"""
    # Check if 'locale' argument is present in the request
    locale = request.args.get('locale', None)
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """render index.html template"""
    return render_template('5-index.html')


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
