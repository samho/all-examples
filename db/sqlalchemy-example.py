from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Numeric, String, Boolean, DateTime, ForeignKey
from sqlalchemy import insert, select, desc, func, and_, or_, not_, update, delete, text
from datetime import datetime
import os

def get_connection():
    return get_engine().connect()


def get_engine():
    return create_engine('sqlite:///cookie.db')


def tables():
    metadata = MetaData()
    engine = get_engine()
    cookies = Table('cookies', metadata,
                    Column('cookie_id', Integer(), primary_key=True),
                    Column('cookie_name', String(50), index=True),
                    Column('cookie_recipe_url', String(255)),
                    Column('cookie_sku', String(55)),
                    Column('cookie_quantity', Integer()),
                    Column('cookie_unit_cost', Numeric(12, 2))
    )
    users = Table('users', metadata,
                  Column('user_id', Integer(), primary_key=True),
                  Column('user_name', String(15), nullable=False, unique=True),
                  Column('user_email', String(255), nullable=False),
                  Column('user_phone', String(20), nullable=False),
                  Column('user_password', String(25), nullable=False),
                  Column('user_created_on', DateTime(), default=datetime.now),
                  Column('user_updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
    )

    orders = Table('orders', metadata,
                   Column('order_id', Integer(), primary_key=True),
                   Column('order_user_id', ForeignKey('users.user_id')),
                   Column('order_shipped', Boolean(), default=False)
    )

    line_items = Table('line_items', metadata,
                       Column('line_item_id', Integer(), primary_key=True),
                       Column('line_item_order_id', ForeignKey('orders.order_id')),
                       Column('line_item_cookie_id', ForeignKey('cookies.cookie_id')),
                       Column('line_item_quantity', Integer()),
                       Column('line_item_extended_cost', Numeric(12, 2))
    )

    if os.path.exists("cookie.db"):
        table_obj_dict = {"cookies": cookies, "users": users, "orders": orders, "line_items": line_items}
    else:
        metadata.create_all(engine)
        table_obj_dict = {"cookies": cookies, "users": users, "orders": orders, "line_items": line_items}

    return table_obj_dict


def insert_data():
    table_list = tables()
    cookies = table_list['cookies']
    ins = cookies.insert().values(
        cookie_name="chocolate chip",
        cookie_recipe_url="http://www.baidu.com",
        cookie_sku="CC01",
        cookie_quantity="12",
        cookie_unit_cost="0.50"
    )
    #
    # print(str(ins.compile().params))
    conn = get_connection()
    result = conn.execute(ins)
    print (result.inserted_primary_key)

    ins2 = cookies.insert()
    result = conn.execute(
        ins2,
        cookie_name="dark chocolate chip",
        cookie_recipe_url="http://www.baidu.com",
        cookie_sku="CC02",
        cookie_quantity="1",
        cookie_unit_cost="0.75"
    )
    print (result.inserted_primary_key)

    ins3 = cookies.insert()
    inventory_list = [
        {
            "cookie_name": "peanut butter",
            "cookie_recipe_url": "http://www.baidu.com",
            "cookie_sku": "PB01",
            "cookie_quantity": "24",
            "cookie_unit_cost": "0.25"
        },
        {
            "cookie_name": "oatmeal raisin",
            "cookie_recipe_url": "http://www.baidu.com",
            "cookie_sku": "EWW01",
            "cookie_quantity": "100",
            "cookie_unit_cost": "1.00"
        }
    ]
    result = conn.execute(ins3, inventory_list)
    print (result.inserted_primary_key)


def query_object():
    conn = get_connection()
    cookies = tables()["cookies"]
    orders = tables()["orders"]
    users = tables()["users"]
    line_items = tables()["line_items"]

    # common query
    s = select([cookies.c.cookie_quantity, cookies.c.cookie_name])
    # query with order
    s = s.order_by(desc(cookies.c.cookie_quantity))
    # query with limitation
    # s = s.limit(2)
    rp = conn.execute(s)
    # print the columns
    print rp.keys()
    # results = rp.fetchall()

    # print the first column value of first record.
    # print rp.scalar()

    # print result with iteration and with string format.
    for rs in rp:
        print '{} - {}'.format(rs.cookie_quantity, rs.cookie_name)

    # query with built-in func
    # s1 = select([func.sum(cookies.c.cookie_quantity)])
    # rp1 = conn.execute(s1)
    # print rp1.scalar()

    # query with built-in func and market it with lable
    s2 = select([func.count(cookies.c.cookie_name).label("inventory_count")])
    rp2 = conn.execute(s2)
    record = rp2.first()
    print record.keys()
    print record.inventory_count

    # query with filter, equal
    s3 = select([cookies.c.cookie_name]).where(cookies.c.cookie_name == "chocolate chip")
    rp3 = conn.execute(s3)
    record = rp3.first()
    print (record.items())

    # query with filter, using clause elements - like
    s4 = select([cookies.c.cookie_unit_cost]).where(cookies.c.cookie_name.like('%chocolate%'))
    rp4 = conn.execute(s4)
    records = rp4.fetchall()
    for r in records:
        print r.cookie_unit_cost

    # query and format the display
    s5 = select([cookies.c.cookie_name, 'SKU-'+cookies.c.cookie_sku])
    for row in conn.execute(s5):
        print (row)

    # query with calculating
    s6 = select([cookies.c.cookie_name, (cookies.c.cookie_quantity * cookies.c.cookie_unit_cost).label('inv_cost')])
    for row in conn.execute(s6):
        print(row)

    # query wth and conjunction
    # s7 = select([cookies]).where(
    #     and_(
    #         cookies.c.cookie_unit_cost < 0.40,
    #         cookies.c.cookie_quantity > 23
    #     )
    # )
    # query with or conjunction
    s7 = select([cookies]).where(
        or_(
            cookies.c.cookie_quantity.between(10,50),
            cookies.c.cookie_name.contains('clip')
        )
    )
    for row in conn.execute(s7):
        print row

    # query with join
    # columns = [orders.c.order_id, users.c.user_name, users.c.user_phone, cookies.c.cookie_name,
    #            line_items.c.line_item_quantity, line_items.c.line_item_extended_cost]
    #
    # cookiesmon_orders = select(columns)
    # cookiesmon_orders = cookiesmon_orders.select_from(orders.join(users).join(line_items).join(cookies))\
    #                     .where(users.c.user_name == 'cookiemon')
    #
    # result = conn.execute(cookiesmon_orders).fetchall()
    # for row in result:
    #     print row

    # Query with raw sql statement
    stmt = "select * from cookies"
    rpraw = conn.execute(stmt).fetchall()
    print rpraw


def update_data():
    conn = get_connection()
    cookies = tables()["cookies"]

    # Update data
    u = update(cookies).where(cookies.c.cookie_name == "chocolate chip")
    u = u.values(cookie_quantity=(cookies.c.cookie_quantity + 120))
    result = conn.execute(u)
    print result.rowcount

    # query the updated record
    s = select([cookies]).where(cookies.c.cookie_name == "chocolate chip")
    result = conn.execute(s).first()
    for key in result.keys():
        print('{:>20}: {}'.format(key, result[key]))


def delete_data():
    conn = get_connection()
    cookies = tables()["cookies"]

    # Delete record
    d =  delete(cookies).where(cookies.c.cookie_name == "dark chocolate chip")
    result = conn.execute(d)
    print result.rowcount

    # Query for the deleted record
    s = select([cookies]).where(cookies.c.cookie_name == "dark chocolate chip")
    result = conn.execute(s).fetchall()
    print len(result)


if __name__ == '__main__':
    # tables()
    # insert_data()
    query_object()
    # update_data()
    # delete_data()
