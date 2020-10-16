# Spotify Search Interface for Python

This package provides a server-side search interface for Spotify. It was developed as a part of another project, but works by itself as well.

## Installation

1. Register your app at [Spotify Developers Dashboard](https://developer.spotify.com/dashboard/applications)
2. Enter your Client ID and Client Secret to `secrets-template.py` and rename it as `secrets.py`
3. Set up your environment and install dependencies

## Usage

1. After installation, run `main.py`
2. Follow the authentication process in your browser and make sure that your app can write to a file named `tokens.ini`
3. After a successful authentication, you should see a simple search form on the page. Alternatively, you can go to `/search/` as well.

## Dependencies

* Python 3
* Bottle
* Requests

For full list of dependencies, check [requirements.txt](requirements.txt).

## Bugs, Comments, Ideas?

Don't hesitate contacting me, or sending a pull request. They are always welcome.
