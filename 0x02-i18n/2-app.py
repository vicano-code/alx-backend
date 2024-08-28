#!/usr/bin/env python3
"""Basic Flask App
"""
from flask import Flask, render_template
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


class Config:
    """confugure available languages in app and set defaults"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Get locale from request"""
    return request.accept_languages.best_match(Config.LANGUAGES)


@app.route('/', strict_slashes=False)
def index():
    """render index.html template"""
    return render_template('2-index.html')


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
