#!/usr/bin/env python3
"""
Flask app with mock login
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'fr']
babel = Babel(app)

# Mock users database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Retrieve a user from the mock database by ID."""
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Set user in flask.g if logged in via the login_as parameter."""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Select the best match for supported locales."""
    return request.accept_languages.best_match(
            app.config['BABEL_SUPPORTED_LOCALES'])


@app.route('/')
def index():
    """Render index with conditional message based on login status."""
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(debug=True)
