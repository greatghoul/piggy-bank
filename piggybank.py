# -*- coding: utf-8 -*-

import uuid, json, re

from flask import Flask, request, render_template, make_response, url_for, jsonify
from sae.kvdb import KVClient
from filters import escapejs

kv = KVClient()

app = Flask(__name__)
app.debug = True

app.jinja_env.filters['escapejs'] = escapejs

@app.route('/', methods=['GET'])
def home():
    bonus_list = [json.loads(bonus) for _, bonus in kv.get_by_prefix('bonus-greatghoul')]
    app.logger.info(bonus_list)
    return render_template('index.html', bonus_list=bonus_list)

@app.route('/bonus', methods=['POST'])
def add_bonus():
    bonus_key = 'bonus-greatghoul-%s' % uuid.uuid4().hex 
    bonus = dict(label=request.form.get('label'),
                 content=request.form.get('content'),
                 bonus=int(request.form.get('bonus')))
    bonus_value = json.dumps(bonus)

    kv.add(bonus_key, bonus_value)

    response = make_response(render_template('add_bonus.js', bonus=bonus))
    response.headers['Content-Type'] = 'text/javascript'
    return response
    
