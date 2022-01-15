from flask import render_template, request
from core.db_manager import DBManager
from models.model import MenuItems, Category

db = DBManager()


def edit_items():
    item = db.query(
        f"SELECT {MenuItems.class_aliases(to_str=True)},categories.name as cat_name FROM menu_items INNER JOIN categories ON menu_items.category_id=categories.id;",
        fetch='all')
    cat_list = db.all_query(Category,
                            f"SELECT * FROM categories where True;")
    if request.method == 'GET':
        return render_template('cashier/edit_items.html', cat=cat_list, data=item)
    elif request.method == 'POST':
        item.category_id = request.form.get('category_id')
        item.discount = request.form.get('discount')
        item.price = request.form.get('price')
        item.image_url = request.form.get('image_url')
        item.serving_time = request.form.get('serving_time')
        db.update(item)
        return "success"

    return render_template('cashier/edit_items.html')
