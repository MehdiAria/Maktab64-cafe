from flask import render_template, request,redirect,url_for
from core.db_manager import DBManager
from models.model import MenuItems, Category
from views.utils import get_cashier_by_cookie
db = DBManager()


def edit_items():
    item = db.query(
        f"SELECT {MenuItems.class_aliases(to_str=True)},categories.name as cat_name FROM menu_items INNER JOIN categories ON menu_items.category_id=categories.id ORDER BY menu_items.id desc;",
        fetch='all')
    cat_list = db.all_query(Category,
                            f"SELECT * FROM categories where True;")
    if request.method == 'GET':
        if not get_cashier_by_cookie(request):
            return redirect(url_for('panel'))
        return render_template('cashier/edit_items.html', cat=cat_list, data=item)
    elif request.method == 'POST':
        # item.category_id = request.form.get('category_id')
        item=db.read(MenuItems, int(request.form.get('_id')))
        item.discount = request.form.get('discount')
        item.name = request.form.get('name')
        item.price = request.form.get('price')
        item.serving_time = request.form.get('serving_time')
        cat_name = request.form.get('cat_name')
        st = db.read_filter(Category, f"name=\'{cat_name}\'")[0]._id
        item.category_id = st
        print(st)
        db.update(item)
        return "success"

    return render_template('cashier/edit_items.html')
