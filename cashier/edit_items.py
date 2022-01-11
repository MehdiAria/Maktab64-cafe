from flask import render_template, request
from core.db_manager import DBManager
from models.model import MenuItems

db = DBManager()


def edit_items():
    items = db.read_all(MenuItems)
    if request.method == 'GET':
        return render_template('cashier/edit_items.html', data=items)
    elif request.method == 'POST':
        item = db.read(MenuItems, int(request.form.get('_id')))
        item.category_id = request.form.get('category_id')
        item.discount = request.form.get('discount')
        item.price = request.form.get('price')
        item.image_url = request.form.get('image_url')
        item.serving_time = request.form.get('serving_time')
        db.update(item)
        return "success"

    return render_template('cashier/edit_items.html')
