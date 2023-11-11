import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def select_goods(name, reference, factory):
    conn = sqlite3.connect("kucun.db")
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    sql = 'select * from goods where name like \'%' + name + '%\' and reference like \'%' + reference + '%\' and factory like\'%' + factory + '%\';'
    # sql = 'select * from goods where name like \'%' + name + '%\' and reference like \'%' + reference+ '%\';'
    cursor.execute(sql)
    goods = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return goods

def select_inventory(name, reference, factory):
    conn = sqlite3.connect("kucun.db")
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    sql = 'select * from inventory where name like \'%' + name + '%\' and reference like \'%' + reference + '%\' and factory like\'%' + factory + '%\';'
    # sql = 'select * from inventory where name like \'%' + name + '%\' and reference like \'%' + reference+ '%\';'
    cursor.execute(sql)
    inventoy = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return inventoy


def insert_inventory (name, reference, factory, num, lot, arrival_date, expiry_date):
    conn = sqlite3.connect('kucun.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('insert into inventory(name, reference, factory, num, lot, arrival, expiry) values(?,?,?,?,?,?,?);', (name, reference, factory, num, lot, arrival_date, expiry_date,))
    cursor.close()
    conn.commit()
    conn.close()


def del_inventory(reference, factory, lot, internal_lot):
    conn = sqlite3.connect('kucun.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    cursor.execute('delete from inventory where reference=? and factory=? and lot=? and internal_lot=?;', (int(reference), str(factory), int(lot), int(internal_lot),))
    cursor.close()
    conn.commit()
    conn.close()


def update_inventory(reference, factory, lot, internal_lot, change, kind):
    conn = sqlite3.connect('kucun.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    if kind == 1:
        # in-bound
        cursor.execute('update inventory set num=num+? where reference=? and factory=? and lot=? and internal_lot=?;', (int(change), int(reference), str(factory), int(lot), int(internal_lot),))
    else:
        # out-bound
        cursor.execute('update inventory set num=num-? where reference=? and factory=? and lot=? and internal_lot=?;', (int(change), int(reference), str(factory), int(lot), int(internal_lot),))
    cursor.close()
    conn.commit()
    conn.close()


def edit_safenumber(safenumber, reference, factory):
    conn = sqlite3.connect('kucun.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('update goods set safenumber=? where reference=? and factory=?;',
                   (int(safenumber), int(reference), str(factory),))
    cursor.close()
    conn.commit()
    conn.close()



