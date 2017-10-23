# -*- coding: utf-8 -*-

from . import dashboard_blueprint
from app import app
from flask import render_template


@dashboard_blueprint.route('/')
@dashboard_blueprint.route('/index')
def index():
    """
    Renders index page.
    :return:
    """
    return render_template('index.html')
