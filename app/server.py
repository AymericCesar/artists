#!/usr/bin/env python3

"""
Main server
"""

import os
import shutil
from time import gmtime, strftime
import argparse
from flask import Flask, jsonify, render_template, request, Response, flash, redirect, url_for, abort
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
# from utils import connect_db, get_header, send_mail
# from utils import fill_table, format_headers, format_comments, allowed_file
# from functools import wraps
import csv

os.chdir(os.path.split(os.path.realpath(__file__))[0])

auth = HTTPBasicAuth()
AUTH_INFO = ".auth_info"
users = {}
users_clear = {}

def load_auth_info():
    with open(AUTH_INFO) as fhandle:
        reader=csv.reader(fhandle, delimiter = ",")
        for line in reader:
            username, password = line
            users[username] = generate_password_hash(password)
            users_clear[username] = password

load_auth_info()
TRACKS_PATH = "./static/multitrack"

APP = Flask(__name__)

APP.config.update(dict(
    DATABASE=os.path.join(APP.root_path, 'static', 'ticketmanager.db'),
    UPLOAD_FOLDER="uploads"
))

# AUTHENTICATION----------------------
@auth.verify_password
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

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
    return jsonify(track)

@APP.route('/is_logged', methods = ['GET', 'POST'])
@auth.login_required(optional=True)
def private_page():
    user = auth.current_user()
    return jsonify(user)

@APP.route('/login', methods = ['GET', 'POST'])
@auth.login_required
def login():
    return "True"

@APP.route('/new_song', methods = ['POST'])
@auth.login_required
def new_song():
    name = request.form["name"]
    trackList = get_dirs(TRACKS_PATH)
    answer = {
        "status": "OK",
        "message": "Song added"
    }
    if name in trackList:
        answer["status"] = "KO"
        answer["message"] = "Song already exists"
        return jsonify(answer)
    os.mkdir(os.path.join(TRACKS_PATH, name))
    return jsonify(answer)

@APP.route('/del_song', methods = ['POST'])
@auth.login_required
def del_song():
    name = request.form["name"]
    trackList = get_dirs(TRACKS_PATH)
    answer = {
        "status": "OK",
        "message": "Song deleted"
    }
    if name not in trackList:
        answer["status"] = "KO"
        answer["message"] = "Song does not exist"
        return jsonify(answer)
    shutil.rmtree(os.path.join(TRACKS_PATH, name))
    return jsonify(answer)

@APP.route('/add_track', methods = ['POST'])
@auth.login_required
def add_track():
    song = request.form["song"]
    tracks = request.files["file"]

    trackList = get_dirs(TRACKS_PATH)
    answer = {
        "status": "OK",
        "message": "Tracks added"
    }
    if song not in trackList:
        answer["status"] = "KO"
        answer["message"] = "Song does not exist"
        return jsonify(answer)
    filename = tracks.filename
    sfilename = secure_filename(filename)
    fname = os.path.join(TRACKS_PATH, song, sfilename)
    if filename != "":
        tracks.save(fname)
        print("Saved", fname)
    print("out")
    return jsonify(answer)

@APP.route('/del_track', methods = ['POST'])
@auth.login_required
def del_track():
    name = request.form["name"]
    trackName = request.form["trackName"]
    songList = get_dirs(TRACKS_PATH)
    answer = {
        "status": "OK",
        "message": "Track deleted"
    }
    if name not in songList:
        answer["status"] = "KO"
        answer["message"] = "Song does not exist"
        return jsonify(answer)
    trackList = get_files(TRACKS_PATH + '/' + name)
    if trackName not in trackList:
        answer["status"] = "KO"
        answer["message"] = "Track does not exist"
        return jsonify(answer)
    os.remove(os.path.join(TRACKS_PATH, name, trackName))
    return jsonify(answer)

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description="neld_artists_webapp"
        )
    PARSER.add_argument(
        "--debug", action="store_const", const=True, default=True
    )
    ARGS = PARSER.parse_args()


    APP.run(port=80, host='0.0.0.0', debug=ARGS.debug)
