from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Numeric, String, Boolean, DateTime, ForeignKey
from sqlalchemy import insert, select, desc
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
                       Column('line_item_extended_cost', Numeric(12,2))
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
    # ins = cookies.insert().values(
    #     cookie_name="chocolate chip",
    #     cookie_recipe_url="http://www.baidu.com",
    #     cookie_sku="CC01",
    #     cookie_quantity="12",
    #     cookie_unit_cost="0.50"
    # )
    #
    # print(str(ins.compile().params))
    conn = get_connection()
    # result = conn.execute(ins)
    # print (result.inserted_primary_key)

    # ins2 = cookies.insert()
    # result = conn.execute(
    #     ins2,
    #     cookie_name="dark chocolate chip",
    #     cookie_recipe_url="http://www.baidu.com",
    #     cookie_sku="CC02",
    #     cookie_quantity="1",
    #     cookie_unit_cost="0.75"
    # )
    # print (result.inserted_primary_key)

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
    # print (result.inserted_primary_key)


def query_object():
    conn = get_connection()
    cookies = tables()["cookies"]
    # common query
    s = select([cookies.c.cookie_quantity, cookies.c.cookie_name])
    # query with order
    s = s.order_by(desc(cookies.c.cookie_quantity))
    # query with limitation
    s = s.limit(2)
    rp = conn.execute(s)
    # print the columns
    print rp.keys()
    # results = rp.fetchall()

    # print the first column value of first record.
    print rp.scalar()

    # print result with iteration and with string format.
    # for rs in rp:
    #     print '{} - {}'.format(rs.cookie_quantity, rs.cookie_name)


if __name__ == '__main__':
    # tables()
    # insert_data()
    query_object()
