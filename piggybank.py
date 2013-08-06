# -*- coding: utf-8 -*-

import os, re, datetime, time, json, logging

from functools import wraps

from sae.kvdb import KVClient
from weibo import APIClient 

from flask import Flask, request, render_template, make_response, \
                  url_for, jsonify, session, redirect
from filters import escapejs, dateformat

instance_path = os.path.dirname(__file__)

app = Flask(__name__)

# 配置日志
app.debug_log_format = '[%(levelname)s] %(message)s'
app.logger.setLevel(logging.INFO)
logger = app.logger

app.config.from_pyfile(os.path.join(instance_path, 'config.cfg'), silent=True)

app.jinja_env.filters['escapejs'] = escapejs
app.jinja_env.filters['dateformat'] = dateformat

kv = KVClient()
client = APIClient(app_key=app.config['APP_KEY'], \
                   app_secret=app.config['APP_SECRET'], \
                   redirect_uri=app.config['REDIRECT_URL'])

def get_referer():
    """ 获取中转地址 """

    return request.headers.get('HTTP_REFERER', url_for('home'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:
            return redirect(url_for('login'))

        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/board', methods=['GET'])
@login_required
def board():
    uid = session['uid']
    logger.info("Fetching targets and bonuses for user %s ...", uid)
    target_list = [target for _, target in kv.get_by_prefix('target-%s' % uid)]
    logger.info("  %s targets loaded.", len(target_list))
    bonus_list = [bonus for _, bonus in kv.get_by_prefix('bonus-%s' % uid)]
    logger.info("  %s bonuses loaded.", len(bonus_list))
    return render_template('board.html', target_list=target_list, bonus_list=bonus_list)

@app.route('/target', methods=['POST'])
@login_required
def add_target():
    logger.info("Creating target %(name)s with price %(price)s", request.form)
    timestamp = time.time()
    target_key = str('target-%s-%i' % (session['uid'], 1000 * timestamp))
    target = dict(name=request.form.get('name'),
                 price=int(request.form.get('price')),
                 timestamp=datetime.datetime.fromtimestamp(timestamp))

    kv.add(target_key, target)
    logger.info("Target saved with key: %s", target_key)

    response = make_response(render_template('add_target.js', target=target))
    response.headers['Content-Type'] = 'text/javascript'
    return response

@app.route('/bonus', methods=['POST'])
@login_required
def add_bonus():
    timestamp = time.time()
    bonus_key = str('bonus-%s-%i' % (session['uid'], 1000 * timestamp))
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
    return redirect(client.get_authorize_url())

@app.route('/callback')
def callback():
    code = request.args.get('code')
    auth = client.request_access_token(code)

    access_token = auth.access_token
    uid = auth.uid
    expires_in = auth.expires_in
    client.set_access_token(access_token, expires_in)
    app.logger.info('User %s logged in with access_token: %s and code: %s', uid, access_token, code)

    user = client.users.show.get(access_token=access_token, uid=uid)
    kv.set('user-%s', user) 
    session['access_token'] = access_token
    session['uid'] = uid 
    session['name'] = user['name'] 
    app.logger.info('User %s is updated', uid)

    return redirect(url_for('board'))

@app.route('/logout')
@login_required
def logout():
    del session['access_token']
    del session['uid']
    del session['name']
    return redirect(url_for('home'))
