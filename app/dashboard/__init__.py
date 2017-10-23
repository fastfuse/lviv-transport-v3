# -*- coding: utf-8 -*-

from flask import Blueprint


dashboard_blueprint = Blueprint('dasboard_blueprint', __name__)

from . import views
