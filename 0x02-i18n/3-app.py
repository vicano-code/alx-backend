#!/usr/bin/env python3
"""Basic Flask App
"""
from flask import Flask, render_template, request
from flask_babel import Babel, gettext


class Config:
    """confugure available languages in app and set defaults"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__, template_folder='templates')
babel = Babel(app)
app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Get locale from request"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """render index.html template"""
    return render_template('3-index.html')


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
