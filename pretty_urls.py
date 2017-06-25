# This Python file uses the following encoding: utf-8

from flask import Flask, request, redirect, url_for
from urlparse import urlparse

app = Flask(__name__)

@app.route("/")
def index():
    return """
<html>
    <head>
    </head>

    <body>
        <form action="/new_url" method="post">
            url: <input type="text" name="url" placeholder="e.g. http://glench.com" />
        </form>
    </body>
</html>
    """

import pickle
try:
    all_hashes = pickle.load(open('db.pickle'))
except:
    all_hashes = {}

emoji = [
u"🌙",
u"🌈",
u"❤️",
u"🌱",
u"🌿",
u"🌷",
u"🌹",
u"🌻",
u"🌼",
u"🌸",
u"🌺",
u"🌳",
u"🌎",
u"🌍",
u"🌏",
u"💫",
u"⭐",
u"️",
u"🌟",
u"✨",
u"☀",
u"️",
u"❄",
u"️",
u"🏵",
u"🌅",
u"🌄",
u"🌠",
u"🎇",
u"🎆",
u"🎈",
u"💛",
u"💚",
u"💙",
u"💜",
u"💖",
u"💕",
u"💞",
u"💓",
u"🌌",
u"🏝",
u"⛰",
u"🍉",
u"🍎",
u"🍓",
u"🍒",
u"🍊",
u"🍋",
u"🍇",
]

import random

def generate_hash(length=4):
    return u''.join(random.sample(emoji, length))

@app.route('/new_url', methods=['POST'])
def new_url():
    parsed_url = urlparse(request.form['url'])
    if parsed_url.netloc and parsed_url.scheme:

        # if there's already a hash for this URL
        for hash, url in all_hashes.iteritems():
            if request.form['url'] == url:
                return hash

        # otherwise, generate a new hash
        new_hash = generate_hash()
        counter = 0
        while counter < 100 and not (new_hash in all_hashes):
            new_hash = generate_hash()
            counter += 1

        all_hashes[new_hash] = request.form['url']
        pickle.dump(all_hashes, open('db.pickle', 'wb'))

        return url_for('/{}'.format(new_hash), _external=True)

    else:
        return 'bad url, buddy'

@app.route('/<hash>', methods=['GET'])
def forward_url(hash):
    if hash in all_hashes:
        return redirect(all_hashes[hash],  code=302)
    else:
        return 'url not found'






