from models.model import Category, db, MenuItems

all_categories = db.read_all(Category)
all_menu_items = db.read_all(MenuItems)


def find_category(c_id):
    for category in all_categories:
        category: Category
        if category._id == c_id:
            return category
