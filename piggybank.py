# -*- coding: utf-8 -*-

import json, re, time, datetime

from flask import Flask, request, render_template, make_response, url_for, jsonify
from sae.kvdb import KVClient
from filters import escapejs, dateformat

kv = KVClient()

app = Flask(__name__)
app.debug = True

app.jinja_env.filters['escapejs'] = escapejs
app.jinja_env.filters['dateformat'] = dateformat

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
    
