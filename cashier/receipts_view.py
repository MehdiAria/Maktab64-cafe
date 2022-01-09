from flask import *
from core.db_manager import DBManager
from models.model import Receipt
from datetime import datetime, timedelta

db = DBManager()


def time_receipts(time_filter=0):
    receipt_date_time = datetime.now() - timedelta(days=time_filter)
    date_receipts = db.read_filter(Receipt, f"time_stamp >= {receipt_date_time}")
