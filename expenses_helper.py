import sqlite3
import datetime


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


def get_most_exp_item():
    data = get_statistic_data()
    return max(list(data), key=lambda x: x['amount'])['name']


def get_timestamp(y, m, d):
    return int(datetime.datetime.timestamp(datetime.datetime(y, m, d)))


def get_timestamp_from_string(s):
    t = s.split('-')
    return get_timestamp(int(t[2]), int(t[1]), int(t[0]))


def get_date(tmstmp):
    return datetime.datetime.fromtimestamp(tmstmp).date()


def get_most_exp_day(lang):
    data = get_statistic_data()
    weekdays = {
        "ru": ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"),
        "en": ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    }
    days = {}
    for payment in data:
        if get_date(payment['payment_date']).weekday() in days:
            days[get_date(payment['payment_date']).weekday()] += payment['amount']
        else:
            days[get_date(payment['payment_date']).weekday()] = payment['amount']
    return weekdays[lang][max(days, key=days.get)]


def get_most_exp_month(lang):
    data = get_statistic_data()
    month_list = {
        "ru": ("0", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
               "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"),
        "en": ("0", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December")
    }
    days = {}
    for payment in data:
        if get_date(payment['payment_date']).month in days:
            days[get_date(payment['payment_date']).month] += payment['amount']
        else:
            days[get_date(payment['payment_date']).month] = payment['amount']
    return month_list[lang][max(days, key=days.get)]


def get_table_data():
    data = get_statistic_data()
    return [(i['id'], i['name'], i['amount'], '{:%d-%m-%Y}'.format(
        get_date(i['payment_date']))) for i in data]


def get_all_expenses_items():
    all_data = {'accordance': {}, 'names': []}
    result = {}
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        query = """SELECT id, name FROM expenses"""
        cursor.execute(query)
        result = dict(cursor)
    all_data['accordance'] = {result[k]: k for k in result}
    all_data['names'] = [v for v in result.values()]
    return all_data


def insert_payments(insert_payment):
    success = False
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        query = """INSERT INTO payments(amount, payment_date, expense_id) VALUES (?,?,?);"""
        cursor.execute(query, insert_payment)
        db.commit()
        success = True
    return success


def get_lang_schema(lang):
    result = {}
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        query = """SELECT ls_name, ls_{} FROM lang_schema""".format(lang)
        cursor.execute(query)
        result = dict(cursor)
    return result
