# -*- coding: utf-8 -*-

import uuid, json

from flask import Flask, request, render_template, make_response, url_for, jsonify
from sae.kvdb import KVClient

app = Flask(__name__)
app.debug = True

kv = KVClient()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/bonus', methods=['POST'])
def add_bonus():
    app.logger.info(request.form)

    bonus_key = 'bonus-greatghoul-%s' % uuid.uuid4().hex 
    bonus_value = json.dumps(request.form)

    kv.add(bonus_key, bonus_value)

    response = make_response(render_template('add_bonus.js'))
    response.headers['Content-Type'] = 'text/javascript'
    return response
    
