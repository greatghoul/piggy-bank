# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello'

