# This Python file uses the following encoding: utf-8

from flask import Flask, request, redirect, url_for
from urlparse import urlparse

app = Flask(__name__)

@app.route("/")
def index():
    return u"""
<html>
    <head>
    </head>

    <body style="font-family: Helvetica, Arial, sans-serif;">
        <h1>Pretty URLs ✨</h1>
	<p>A url shortener that makes <a href="https://en.wikipedia.org/wiki/Semantic_URL">pretty emoji URLs</a>.</p>
        <form action="/new_url" method="post">
            url: <input style="font-size: 20px; padding: 8px;" type="text" name="url" placeholder="e.g. http://glench.com" />
<button type="submit">Get pretty url</button>
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

new_url_template = u"""
<html>
	<head>
	</head>

	<body style="font-family: Helvetica, Arial, sans-serif;">
		Pretty URL: <input type="text" style="padding: 8px; font-size: 20px;" value={url} size={size} />
		<script>
			var input = document.querySelector('input');
			input.setAttribute('value', window.location.origin+'/'+input.getAttribute('value'));
			input.setAttribute('size', input.getAttribute('value').length);
			input.select();
		</script>
	</body>
</html>
"""

@app.route('/new_url', methods=['POST'])
def new_url():
    parsed_url = urlparse(request.form['url'])
    if parsed_url.netloc and parsed_url.scheme:

        # if there's already a hash for this URL
        for hash, url in all_hashes.iteritems():
            if request.form['url'] == url:
                return new_url_template.format(url=hash, size=len(hash))

        # otherwise, generate a new hash
        new_hash = generate_hash()
        counter = 0
        while counter < 100 and not (new_hash in all_hashes):
            new_hash = generate_hash()
            counter += 1

        all_hashes[new_hash] = request.form['url']
        pickle.dump(all_hashes, open('db.pickle', 'wb'))

	return new_url_template.format(url=new_hash, size=len(new_hash))
    else:
        return 'please submit a valid url'

@app.route('/<hash>', methods=['GET'])
def forward_url(hash):
    if hash in all_hashes:
        return redirect(all_hashes[hash],  code=302)
    else:
        return 'url not found'






