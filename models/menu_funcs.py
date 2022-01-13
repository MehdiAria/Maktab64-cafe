from models.model import Category, db, MenuItems

all_categories = db.read_all(Category)
all_menu_items = db.read_all(MenuItems)
