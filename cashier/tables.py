from flask import render_template,request
from core.db_manager import DBManager
from models.model import CafeTable


db = DBManager()


def tables():
    tables = db.read_all(CafeTable)
    if request.method =='GET':
        return render_template('cashier/tables.html', data=tables)
    elif request.method =='POST':
        table = db.read(CafeTable, int(request.form.get('_id')))
        table.is_del = True if request.form.get('is_del') == 'true' else False
        table.space = request.form.get('space')
        table.is_empty = request.form.get('is_empty')
        db.update(table)
        return "success"

                <div>
                    <div class="topbar-divider d-none d-sm-block">ho</div>
                    <button class="btn btn-success" type="button" style="background-color: saddlebrown;" id="logins">
                        <a href="#" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Logout!"><i
                                class="fa fa-sign-out" style="font-size:20px; color: white"></i></a>
                    </button>

                </div>