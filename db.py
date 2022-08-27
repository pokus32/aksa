import os
import sqlite3
from sqlite3 import Error

class DataBase():
    db_cursor = ''
    def __init__(self):
        wd = os.getcwd() 
        print(wd+'/sqlite.db')
        self.db_conn = sqlite3.connect(r"./sqlite.db")

    def get_all(self):
        c = self.db_conn.cursor()
        c.execute("select clients.id, clients.name, sum(aksa.balance_tl),\
         sum(aksa.balance_dl), sum(aksa.balance_eu) from clients LEFT OUTER JOIN aksa \
         on aksa.client_id = clients.id group by clients.name order by clients.id")
        rows = c.fetchall()
        c.close()
        return rows

    def get_all_clients(self):
        c = self.db_conn.cursor()
        c.execute("select id, name, contact1, contact2, contact3, contact4, contact5, is_active, adress from clients where is_active is true")
        rows = c.fetchall()
        c.close()
        return rows

    def get_all_prods(self):
        c = self.db_conn.cursor()
        c.execute("select id, name from prod where is_active is true")
        rows = c.fetchall()
        c.close()
        return rows

    def get_by_client_id(self, client_id):
        c = self.db_conn.cursor()
        c.execute("select clients.name, aksa.* from aksa LEFT OUTER JOIN \
            clients on aksa.client_id = clients.id \
            where aksa.client_id like '{}' order by aksa.date ASC".format(client_id))
        rows = c.fetchall()
        c.close()
        return rows

    def insert_new_client(self, name, adress, contact1):
        contact2 = ''
        contact3 = ''
        contact4 = ''
        contact5 = ''
        is_active = 1
        try:
            c = self.db_conn.cursor()
            # query = f"insert into clients (name, contact1, contact2, contact3, contact4, contact5, adress, is_active) \
            # values ('{name}', '{contact1}', '{contact2}', '{contact3}', '{contact4}', '{contact5}', '{adress}', '{is_active}')"
            query = "insert into clients (name, contact1, contact2, contact3, contact4, contact5, adress, is_active) \
            values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(name, contact1, contact2, contact3, contact4, contact5, adress, is_active)
            c.execute(query)
            self.db_conn.commit()
            c.close()
        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)

    def insert_new_prod(self, name):
        is_active = 1
        try:
            c = self.db_conn.cursor()
            query = "insert into prod (name, is_active) values ('{}', '{}')".format(name, is_active)
            c.execute(query)
            self.db_conn.commit()
            c.close()
        except sqlite3.Error as error:
            print(error)

    def update_client(self, name, client_id, adress, contact1):
        try:
            c = self.db_conn.cursor()
            query = "update clients set name = '{}', adress = '{}', contact1 = '{}' \
            where id = '{}'".format(name, adress, contact1, client_id)
            c.execute(query)
            self.db_conn.commit()
            c.close()
        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)

    def update_prod(self, name, prod_id):
        try:
            c = self.db_conn.cursor()
            query = "update prod set name = '{}' where id = '{}'".format(name, prod_id)
            c.execute(query)
            self.db_conn.commit()
            c.close()
        except sqlite3.Error as error:
            print(error)


    def insert_data(self, data):
        try:
            c = self.db_conn.cursor()
            # ['AKSA KONYA', '"12"', '"22"', '3', '033', '0', '0', '99.0', '0.0', '0.0', '0', '0', '0', '99.0', '0.0', '0.0']
            query = "insert into aksa (client_id, date, type, quantity, price_tl, price_dl, price_eu,\
            total_tl, total_dl, total_eu, payed_tl, payed_dl, payed_eu, balance_tl, balance_dl, balance_eu) \
            values ('{0}', {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15})".\
            format(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],\
                data[11],data[12],data[13],data[14],data[15])
            c.execute(query)
            self.db_conn.commit()
            c.close()
        except sqlite3.Error as error:
            print(error)

    def remove_rows(self, ids_list):
        ids = ','.join(map(str, ids_list))
        try:
            c = self.db_conn.cursor()
            query = "DELETE FROM aksa WHERE id IN ({0});".format(ids)
            # print('query ============================\n', query)
            c.execute(query)
            self.db_conn.commit()
            c.close()
        except sqlite3.Error as error:
            print(error)

    def remove_prod(self, ids_list):
        ids = ','.join(map(str, ids_list))
        try:
            c = self.db_conn.cursor()
            query = "DELETE FROM prod WHERE id IN ({0});".format(ids)
            # print('query ============================\n', query)
            c.execute(query)
            self.db_conn.commit()
            c.close()
        except sqlite3.Error as error:
            print(error)