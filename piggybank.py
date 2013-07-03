# -*- coding: utf-8 -*-

import json, re, time, datetime

from flask import Flask, request, render_template, make_response, \
                  url_for, jsonify, session, redirect
from sae.kvdb import KVClient
from filters import escapejs, dateformat

instance_path = os.path.dirname(__file__)

app = Flask(__name__)
app.config.from_pyfile(os.path.join(instance_path, 'config.cfg'), silent=True)

app.jinja_env.filters['escapejs'] = escapejs
app.jinja_env.filters['dateformat'] = dateformat

kv = KVClient()

def get_referer():
    """ 获取中转地址 """

    return request.headers.get('HTTP_REFERER', request.url_root)

@app.route('/', methods=['GET'])
def home():
    bonus_list = [bonus for _, bonus in kv.get_by_prefix('bonus-greatghoul')]
    return render_template('index.html', bonus_list=bonus_list)

@app.route('/bonus', methods=['POST'])
def add_bonus():
    timestamp = time.time()
    bonus_key = 'bonus-greatghoul-%i' % (1000 * timestamp)
    bonus = dict(label=request.form.get('label'),
                 content=request.form.get('content'),
                 bonus=int(request.form.get('bonus')),
                 timestamp=datetime.datetime.fromtimestamp(timestamp))
    # bonus_value = json.dumps(bonus)

    kv.add(bonus_key, bonus)

    response = make_response(render_template('add_bonus.js', bonus=bonus))
    response.headers['Content-Type'] = 'text/javascript'
    return response

@app.route('/login')
def login():
    session['login_ok_url'] = get_referer()
    callback = url_for('callback', _external=True) 

    auth = OAuthHandler(consumer_key, consumer_secret, callback)
    # Get request token and login url from the provider
    url = auth.get_authorization_url()
    session['oauth_request_token'] = auth.request_token
    # Redirect user to login
    return redirect(url)

