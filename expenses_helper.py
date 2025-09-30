import sqlite3


def get_statistic_data():
    all_data = []
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        query = """SELECT * FROM payments JOIN expenses ON expenses.id = payments.expense_id"""
        cursor.execute(query)
        all_data = cursor
    return all_data


def get_most_common_item():
    data = get_statistic_data()
    quantity = {}
    for payments in data:
        if payments['expense_id'] in quantity:
            quantity[payments['expense_id']]['qty'] += 1
        else:
            quantity[payments['expense_id']] = {'qty': 1, 'name': payments['name']}
    return max(quantity.values(), key=lambda x: x['qty'])['name']
