from flask import render_template, request
from core.db_manager import DBManager
from datetime import datetime, timedelta

db = DBManager()


def intro():
    return render_template('cashier/intro.html')
