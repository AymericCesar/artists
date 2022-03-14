#!/usr/bin/env python3

"""
Main server
"""

import os
from time import gmtime, strftime
import argparse
from flask import Flask, jsonify, render_template, request, Response, flash, redirect, url_for, abort
# from utils import connect_db, get_header, send_mail
# from utils import fill_table, format_headers, format_comments, allowed_file
# from functools import wraps
import csv

os.chdir(os.path.split(os.path.realpath(__file__))[0])

AUTH_INFO = ".auth_info"
def load_auth_info():
    with open(AUTH_INFO) as fhandle:
        reader=csv.reader(fhandle, delimiter = ",")
        for line in reader:
            username, password = line
            break
    return username, password

USERNAME, PASSWORD = load_auth_info()
TRACKS_PATH = "./static/multitrack"

APP = Flask(__name__)

# APP.config.update(dict(
#     DATABASE=os.path.join(APP.root_path, 'static', 'ticketmanager.db'),
#     UPLOAD_FOLDER="uploads"
# ))

# AUTHENTICATION----------------------
# def check_auth(username, password):
#     """This function is called to check if a username /
#     password combination is valid.
#     """
#     return username == USERNAME and password == PASSWORD
#
# def authenticate():
#     """Sends a 401 response that enables basic auth"""
#     return Response(
#     'Could not verify your access level for that URL.\n'
#     'You have to login with proper credentials', 401,
#     {'WWW-Authenticate': 'Basic realm="Login Required"'})
#
# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#         if not auth or not check_auth(auth.username, auth.password):
#             return authenticate()
#         return f(*args, **kwargs)
#     return decorated

# TEMPLATE NAVIGATION----------------------
@APP.route('/')
def index():
    """
    Renders index.html template

    Returns
    -------
    'index.html': template
    """
    return render_template('index.html')

def get_dirs(d):
    return [o for o in os.listdir(d)
                    if os.path.isdir(os.path.join(d,o))]

def get_files(d):
    return [o for o in os.listdir(d)
                    if not os.path.isdir(os.path.join(d,o))]

@APP.route('/track')
def track():
    """
    Returns tracks list
    """
    trackList = get_dirs(TRACKS_PATH)

    return jsonify(trackList)

def is_sound_file(name):
    return name.endswith(('.mp3', '.ogg', '.wav', '.m4a'))
    # if (endsWith(name, ".mp3")): return True
    # if (endsWith(name, ".ogg")): return True
    # if (endsWith(name, ".wav")): return True
    # if (endsWith(name, ".m4a")): return True
    # return False;

def get_track(name):
    files = [o for o in get_files(TRACKS_PATH + '/' + name)
                     if is_sound_file(o)]
    track = {
        "id": name,
        "instruments": []
    }
    for file in files:
        track["instruments"].append({
            "name": file[:-3],
            "sound": file
        })
    return track

@APP.route('/track/<name>')
def track_name(name):
    """
    Returns tracks list
    """
    track = get_track(name)
    if not track:
        abort(404)
        # return res.send(404, 'Track not found with id "' + id + '"');
    print(track)
    return jsonify(track)

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description="neld_artists_webapp"
        )
    # PARSER.add_argument("password", type=str, help="medleydb gmail password")
    PARSER.add_argument(
        "--debug", action="store_const", const=True, default=False
    )
    ARGS = PARSER.parse_args()
    # APP.config.update(dict(MAIL_PASSWORD=ARGS.password))

    # MAIL = Mail(APP)
    MAIL = 0

    APP.run(port=80, host='0.0.0.0', debug=ARGS.debug)
