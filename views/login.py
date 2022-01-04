from flask import render_template, request
from core.db_manager import DBManager
from models.model import *


def login():
    return render_template('login.html')
