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


def menu_categories():
    cat_items = {}
    cat_dict = category_parent_dict()
    for item in all_menu_items:
        item: MenuItems
        alias = cat_dict[item.category_id]
        if cat_items.get(alias, None):
            cat_items[alias].append(item)
        else:
            cat_items[alias] = [item]
    return cat_items

