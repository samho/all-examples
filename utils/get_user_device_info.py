#!/usr/bin/env python
from sqlalchemy import MetaData, create_engine, Table, select
from pymongo import MongoClient

def getallproducts():
    metadata = MetaData()
    engine = create_engine('mysql+pymysql://xcloud:go4xpggo4xpg@QRDS/xcloud', pool_recycle=3600)

    product_list = []
    product_table = Table('gizwits_site_product', metadata, autoload=True, autoload_with=engine)
    s = select([product_table])
    products = engine.execute(s).fetchall()
    for product in products:
            product_list.append((product['product_key'], product['id']))

    return dict(product_list)


def getdomainbyproductkey():
    metadata = MetaData()
    engine = create_engine('mysql+pymysql://xcloud:go4xpggo4xpg@QRDS/xcloud', pool_recycle=3600)

    product_list = getallproducts()
    openplatform_opapplication_table = Table('openplatform_opapplication', metadata, autoload=True, autoload_with=engine)
    openplatform_opapplication_product_table = Table('openplatform_opapplication_product', metadata, autoload=True, autoload_with=engine)

    domain_list = []
    for product_key, product_id in product_list.iteritems():
        try:
            select_app_id_by_product_id = select([openplatform_opapplication_product_table.c.id]).where(openplatform_opapplication_product_table.c.product_id == product_id).limit(1)
            app_rec_id = engine.execute(select_app_id_by_product_id).fetchall()
        except:
            pass
            continue

        try:
            select_domain_id_by_app_id = select([openplatform_opapplication_table.c.domainid]).where(openplatform_opapplication_table.c.id == app_rec_id[0][0]).limit(1)
            domain_id = engine.execute(select_domain_id_by_app_id).fetchall()
        except:
            pass
            continue

        domain_list.append((product_key, domain_id[0][0]))

    return dict(domain_list)


def getbindingbydomainid():
    rec_list = []
    client = MongoClient('QPDMGS02', 27018)
    db = client['gizwits_core']
    #domain_list = getdomainbyproductkey()
    domain_list= {"be606a7b34d441b59d7eba2c080ff805": "ffaabda3fff04369bc1537534d7f9049"}
    for product_key, domain_id in domain_list.iteritems():
        col_name = "domain.%s.user" % domain_id
        collection = db[col_name]
        items = collection.find()
        for item in items:
            try:
                uid = item['uid']
            except:
                uid = "Unknown"

            try:
                username = item['username']
            except:
                username = "None"

            try:
                email = item['email']
            except:
                email = "None"

            try:
                phoneid = item['phoneid']
            except:
                phoneid = "None"

            try:
                mac_list = item['binding_info'][domain_id]
            except:
                mac_list = "None"

            if mac_list == "None":
                rec_list.append((product_key, uid, username, email, phoneid, mac_list))
            else:
                for mac in mac_list:
                    rec_list.append((product_key, uid, username, email, phoneid, mac))

    return rec_list


def writetofile(record_list):
    f = open("user_device_info.csv", "a")
    for rec in record_list:
        f.write("%s, %s, %s, %s, %s, %s\n" % (rec[0], rec[1], rec[2], rec[3], rec[4], rec[5]))


    f.close()


if __name__ == '__main__':
    r_list = getbindingbydomainid()
    writetofile(r_list)

