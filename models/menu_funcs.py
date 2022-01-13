from models.model import Category, db, MenuItems

all_categories = db.read_all(Category)
all_menu_items = db.read_all(MenuItems)


def find_category(c_id):
    for category in all_categories:
        category: Category
        if category._id == c_id:
            return category


def category_parent(category):
    category: Category
    parent_id = category.category_id
    if parent_id:
        return category_parent(find_category(parent_id))
    return category


def category_parent_dict():
    cat_dict = {}
    for category in all_categories:
        category: Category
        cat_dict[category._id] = category_parent(category).name
    return cat_dict



