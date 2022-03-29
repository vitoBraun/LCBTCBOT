
import sqlite3
import json
from PyQt5 import QtCore
from PyQt5.QtCore import QMutex


class dbExecutorClass():
    def add_profile(self, profile_name, api_key, api_secret):
        try:
            # Create table
            conn = sqlite3.connect("db/db.db", check_same_thread=False)
            crs = conn.cursor()
            sql_create_tbl = "CREATE TABLE IF NOT EXISTS local_profiles (id INTEGER PRIMARY KEY, profile_name text type UNIQUE, api_key text, api_secret text)"
            crs.execute(sql_create_tbl)
            conn.commit()

            # INsert some data
            sql_insert = "INSERT INTO local_profiles VALUES(NULL, '%s', '%s', '%s')"
            crs.execute(sql_insert % (profile_name, api_key, api_secret)
                        )
            # save it
            conn.commit()
            conn.close()
            print("DB: Records inserted successfully into profiles table ",
                  crs.rowcount)
        except sqlite3.Error as error:
            print("DB: Did not insert data....", error)

        # ADD BOT SET

    def add_bot_set(self, bot_set):
        conn = sqlite3.connect("db/db.db", check_same_thread=False)
        crs = conn.cursor()
        sql_create_tbl = """CREATE TABLE IF NOT EXISTS bot_sets (
            onoff integer,
            bot_id text type unique,
            profile_name text,
            bot_type text,
            ad_id integer,
            trade_type text,
            currency text,
            online_provider text,
            old_pos integer,
            new_pos integer,
            koeff integer,
            min_koeff integer,
            max_koeff integer,
            method_url text,
            ad_list text,
            autoreply_onoff integer,
            autoreply_msg text,
            trades text,
            last_time_upd integer,
            color text,
            price integer,
            sell_ad_ref text,
            margin integer,
            fee_total integer,
            sell_price integer,
            min_amount integer,
            max_amount integer,
            min_price integer,
            min_price_onoff integer
            )"""
        crs.execute(sql_create_tbl)
        conn.commit()

        # try:
        # Вставляем данные в таблицу
        sql_insert = """INSERT INTO bot_sets
                            VALUES (?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?,?,?)"""
        crs.execute(sql_insert, (
            1,
            bot_set['bot_id'],  # bot_id
            bot_set['profile_name'],  # profile_name
            bot_set['bot_type'],  # bot_type
            bot_set['ad_id'],  # ad_id
            bot_set['trade_type'],  # trade_type
            bot_set['currency'],  # currency
            bot_set['online_provider'],  # online_provider
            2,  # old_pos
            2,  # new_pos
            1.01,  # koeff
            1.01,  # min_koeff
            1.01,  # max_koeff
            bot_set['method_url'],  # method_url
            "None",  # ad_list
            0,  # autoreply_onoff
            'Welcome',  # autoreply_msg
            "{10000, 123123, 123414}",  # trades
            1607967838.650771,  # last time upd
            0,
            10000,  # price
            bot_set['sell_ad_ref'],  # sell ad ref
            2,  # margin
            2,  # fee total
            10000.00,  # sell_price
            1000,  # min_amount
            10000,  # max_amount
            10000.00,  # min_price
            0  # min_price_onoff
        )
        )
        # SAVE CHANGES
        conn.commit()
        conn.close()
        print("DB: Records inserted successfully into bot_sets table ",
              crs.rowcount)

    # except sqlite3.Error as error:
    #     print("Did not insert data....", error)

    def read_bot_set(self, bot_id):
        try:
            conn = sqlite3.connect("db/db.db", check_same_thread=False)
            crs = conn.cursor()
            crs.execute(
                "SELECT * FROM bot_sets WHERE bot_id='%s'" % bot_id)

            rows = [x for x in crs]
            cols = [x[0] for x in crs.description]
            conn.close()
            bot_set = []
            for row in rows:
                keyval = {}
                for prop, val in zip(cols, row):
                    keyval[prop] = val
                bot_set.append(keyval)

            return bot_set[0]
        except:
            print('DB: could not read bot_set by this bot id')

    def read_bot_single_set(self, bot_id, key):
        return self.db_get_cell('bot_sets', key, 'bot_id', bot_id)

    def write_bot_set(self, bot_set):
        try:
            for i in bot_set:
                conn = sqlite3.connect(
                    "db/db.db", check_same_thread=False)
                crs = conn.cursor()
                sql = """UPDATE bot_sets SET %s = '%s' WHERE bot_id = '%s'"""
                crs.execute(sql % (i, bot_set[i], bot_set['bot_id']))
                conn.commit()
                conn.close()
        except sqlite3.Error as error:
            print("DB: Could not update....", error)

    def write_bot_single_set(self, bot_id, key, val):
        conn = sqlite3.connect("db/db.db", check_same_thread=False)
        crs = conn.cursor()
        sql = """UPDATE bot_sets SET %s = '%s' WHERE bot_id = '%s'"""
        crs.execute(sql % (key, val, bot_id))
        conn.commit()
        conn.close()

    def delete_bot_set(self, bot_id):
        try:
            conn = sqlite3.connect("db/db.db", check_same_thread=False)
            crs = conn.cursor()
            sql_delete = """DELETE FROM bot_sets WHERE bot_id = '%s'"""
            crs.execute(sql_delete % bot_id)
            print("DB: Bot_set successfully deleted!")
            conn.commit()  # SAVE CHANGES
            conn.close()
        except sqlite3.Error as error:
            print("DB: Could not delete....", error)

    def delete_profile(self, profile):
        try:
            conn = sqlite3.connect("db/db.db", check_same_thread=False)
            crs = conn.cursor()
            sql_delete = """DELETE FROM local_profiles WHERE profile_name = '%s'"""
            crs.execute(sql_delete % profile)
            print("DB: Profile successfully deleted!")
            conn.commit()  # SAVE CHANGES
            conn.close()
        except sqlite3.Error as error:
            print("DB: Could not delete....", error)

    def db_get_table(self, table):
        conn = sqlite3.connect("db/db.db", check_same_thread=False)
        crs = conn.cursor()
        sql = crs.execute(
            "SELECT * FROM '%s'" % (table))
        allrows = sql.fetchall()
        conn.close()
        return allrows

        # table - table name in database
        # val1 - the cell, the value of which we want to get
        # key2 - column, specifying the search
        # val2 - value, specifying the search
        # It should work like this: in <table> get us <val1>, where <key2> = <val2>
    def db_get_cell(self, table, val1, key2, val2):
        # first we take all the table
        conn = sqlite3.connect("db/db.db", check_same_thread=False)
        crs = conn.cursor()
        sql = crs.execute(
            "SELECT * FROM '%s'" % (table))

        allrows = sql.fetchall()

        # then we get its columns names
        columns = list(map(lambda x: x[0], sql.description))
        conn.close()
        # in columns names we find index of the column the name of which is in key2 variable, and remember it in col_n
        x = 0
        for i in columns:
            if i == key2:
                col_n = x
                break
            else:
                x += 1

        # then, knowing column number we define row, where is our cell is situated
        x = 0
        for i in allrows:
            if i[col_n] == val2:
                row_n = x
                break
            else:
                x += 1

        # now we have to define in which column our aim cell sits, to finnally return it
        x = 0
        for i in columns:
            if i == val1:
                thekey = x
                break
            else:
                x += 1
        # done

        return allrows[row_n][thekey]

    def delete_table(self, table):
        conn = sqlite3.connect("db/db.db", check_same_thread=False)
        crs = conn.cursor()
        try:
            slq = '''DROP TABLE IF EXISTS '%s' '''
            crs.execute(slq % table)
            print('Deleted table')
        except:
            pass
        conn.commit()
        conn.close()

    def create_settings_table(self):
        conn = sqlite3.connect("db/db.db", check_same_thread=False)
        crs = conn.cursor()
        sql_create_tbl = """CREATE TABLE IF NOT EXISTS settings (
                    comment text,
                    domain text,
                    time_zone text,
                    last_open_bot text
                    )"""
        crs.execute(sql_create_tbl)
        conn.commit()

        sql_check = """SELECT * FROM settings"""
        crs.execute(sql_check)
        exist = crs.fetchall()
        if len(exist) == 0:
            sql_insert = """INSERT INTO settings
                                            VALUES (?,?,?,?)"""
            crs.execute(sql_insert, (
                'OK',
                'fi',
                '+4',
                ''
            )
            )
            # SAVE CHANGES
            conn.commit()
            print("DB: Records inserted successfully into settings table ",
                  crs.rowcount)
        conn.close()

    def read_settings_single(self, val):
        try:
            return self.db_get_cell('settings', val, 'comment', 'OK')
        except:
            print('error reading settings')

    def write_settings_single(self, key, val):
        try:
            conn = sqlite3.connect("db/db.db", check_same_thread=False)
            crs = conn.cursor()
            sql_insert = """ALTER TABLE settings ADD COLUMN '%s' text"""
            crs.execute(sql_insert % (key))
            sql_insert = """INSERT INTO settings(%s) VALUES('%s')"""
            crs.execute(sql_insert % (key, val))
            conn.commit()
            conn.close()
        except:
            conn = sqlite3.connect("db/db.db", check_same_thread=False)
            crs = conn.cursor()
            sql_insert = """UPDATE settings SET %s = '%s'"""
            crs.execute(sql_insert % (key, val))
            conn.commit()
            conn.close()

    def get_botsets(self):
        conn = sqlite3.connect("db/db.db", check_same_thread=False)
        crs = conn.cursor()
        crs.execute("SELECT * FROM bot_sets")
        rows = [x for x in crs]
        cols = [x[0] for x in crs.description]
        conn.commit()
        conn.close()
        bot_sets = []
        for row in rows:
            keyval = {}
            zipitem = zip(cols, row)
            for prop, val in zipitem:
                keyval[prop] = val
            if keyval['onoff'] == 1:
                bot_sets.append(keyval)
        return bot_sets

    def get_local_profiles(self):
        conn = sqlite3.connect("db/db.db", check_same_thread=False)
        crs = conn.cursor()
        crs.execute("SELECT * FROM local_profiles")
        rows = [x for x in crs]
        cols = [x[0] for x in crs.description]
        conn.commit()
        conn.close()
        lp = []
        for row in rows:
            keyval = {}
            zipitem = zip(cols, row)
            for prop, val in zipitem:
                keyval[prop] = val
            lp.append(keyval)
        return lp


dbExecutor = dbExecutorClass()
