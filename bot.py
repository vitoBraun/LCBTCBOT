
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QWidget
from lbcapi import api
import urllib.request
import json
import re

from db import db
import time
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QObject
import csv


class LocalBitcoinsBot():
    def __init__(self, bot_id):
        self.dbEx = db.dbExecutor
        self.bot_id = bot_id

    def run(self):
        self.api_key = self.dbEx.db_get_cell('local_profiles', 'api_key',
                                             'profile_name', r('profile_name'))
        self.api_secret = self.dbEx.db_get_cell('local_profiles', 'api_secret',
                                                'profile_name', r('profile_name'))
        self.ad_list_short = self.adList()
        self.curr_pos = self.find_self_position()

        self.conn = api.hmac(self.api_key,
                             self.api_secret)  # creating connection
        print('--------------'+r('bot_id') + '----------------')
        self.ad_data = api.get_profile_ad(
            self.conn, r('ad_id'))
        print('BOT ad data received')  # getting ad data

        self.price_change()

    def adList(self, method_url=0):
        if method_url == 0:
            method_url = r('method_url')

        path = method_url.replace('.json', '')
        path = path.replace('/', '_')
        path = 'db/ad_lists/' + path + 'json.json'
        try:
            with open(path, 'r') as f:
                ad_list = json.load(f)
                ad_list_res = []
                for i in range(ad_list['data']['ad_count']):
                    if ad_list['data']['ad_list'][i]['data']['min_amount'] != None:
                        if float(ad_list['data']['ad_list'][i]['data']['min_amount']) <= float(r('min_amount')):
                            ad_list_res.append(
                                [ad_list['data']['ad_list'][i]['data']['temp_price'],
                                    ad_list['data']['ad_list'][i]['data']['profile']['username']]
                            )
                if r('trade_type') == 'ONLINE_BUY':
                    i = 0
                    for i in range(len(ad_list_res)-1):
                        if i > 0 and float(ad_list_res[i][0]) < float(ad_list_res[i+1][0]):
                            del ad_list_res[i+1:]
                            break
                        else:
                            i += 1

            out = []
            if len(ad_list_res) < 16:
                amount = len(ad_list_res)
            else:
                amount = 16
            for i in range(amount):
                out.append(
                    [
                        ad_list_res[i][0],
                        ad_list_res[i][1]
                    ]
                )
            with open('db/ad_lists/'+self.bot_id+'.csv', 'w',  encoding='utf8', newline='') as output_file:
                csv_writer = csv.writer(output_file)
                for i in out:
                    csv_writer.writerow(i)
            if len(out) == 0:
                print('AD LIST IS EMPTY')
            return out
        except:
            print('BOT could not open file')
            return False

    def find_self_position(self):
        self_position = 2  # default
        try:
            for i in range(len(self.ad_list_short)):
                if self.ad_list_short[i][1] == r('profile_name'):
                    print('BOT  Our position is found ' + str(i))
                    self_position = i
                    break
            return self_position
        except:
            print('BOT  Error with finding in list')

    def price_formula(self):
        prefix = 'btc_in_usd*'
        if (r('currency') != 'USD'):
            prefix = str('btc_in_usd*USD_in_' +
                         r('currency').upper() + '*')
        return prefix

    # PRICE CHANGE
    def price_change(self):
        if r('onoff') == 1:
            ad_data = self.ad_data
            ad_list = self.ad_list_short
            if len(ad_list) != 0:
                curr_pos = self.curr_pos

                if float(ad_data['min_amount']) != float(r('min_amount')):
                    w('min_amount', float(ad_data['min_amount']))
                if float(ad_data['max_amount']) != float(r('max_amount')):
                    w('max_amount', float(ad_data['max_amount']))

                curr_price = float(ad_data['temp_price'])
                new_pos = int(r('new_pos'))
                ad_list_last = len(ad_list)-1

                if new_pos > ad_list_last and ad_list_last != -1:
                    new_pos = ad_list_last
                    w('new_pos', new_pos)

                min_koeff = float(r('min_koeff'))
                max_koeff = float(r('max_koeff'))

                print('curr_price: ' + str(curr_price))
                print('new_pos: ' + str(new_pos))
                if ad_list != None:
                    if len(ad_list) <= 2:
                        print('ad list contains 1 ad')
                        curr_pos = 0
                        below_user_pos = 0

                    elif len(ad_list) >= 3:
                        if len(ad_list) < (curr_pos + 1):
                            below_user_pos = curr_pos
                        else:
                            below_user_pos = curr_pos + 1
                    if curr_pos == len(ad_list)-1:
                        below_user_pos = curr_pos
                else:
                    print('ad_list is not loaded')

                print('curr_pos: ' + str(curr_pos))
                below_user_price = float(ad_list[below_user_pos][0])
                print('below_user_price: ' + str(below_user_price))
                price_eq = float(re.sub(r'[^0-9.]+', r'',
                                        ad_data['price_equation']))

                if 'btc_in_usd' not in ad_data['price_equation']:
                    price_eq = min_koeff

                aver_price = float(ad_data['temp_price']) / price_eq
                w('price', float(ad_data['temp_price']))

                step = float(1)  # шаг в валюте
                min_price_step = 0.05  # максимальный шаг между циклами пересчета

                # SELL AD POSITION BOT TYPE
                if r('bot_type') == 'sell_ad_position':
                    min_price = min_koeff * aver_price
                    # if r('min_price_onoff') == True:
                    #     if min_price < r('min_price'):
                    #         min_price = r('min_price')
                    #         print('max price set is' + str(r('min_price')))

                    if curr_pos != new_pos:
                        print('curr_pos != new_pos')
                        if curr_pos > new_pos:
                            new_price = float(ad_list[new_pos][0]) - step
                            if new_price < curr_price * (1 - min_price_step):
                                new_price = curr_price * (1 - min_price_step)
                                print(
                                    'new_price < curr_price * (1 - min_price_step)')
                        elif curr_pos < new_pos:
                            new_price = float(ad_list[new_pos][0]) + step
                            if new_price > curr_price * (1 + min_price_step):
                                new_price = curr_price * (1 + min_price_step)
                                print(
                                    'new_price > curr_price * (1 + min_price_step)')

                    else:
                        new_price = below_user_price - step

                    if new_price < min_price:
                        new_price = min_price

                    if r('min_price_onoff') == 1:
                        print('Min price is On')
                        if float(new_price) < float(r('min_price')):
                            new_price = float(r('min_price'))

                # BUY AD POSITION BOT TYPE
                elif r('bot_type') == 'buy_ad_position':
                    max_price = min_koeff * aver_price
                    if int(curr_pos) != int(new_pos):
                        print('curr_pos != new_pos')
                        if curr_pos > new_pos:
                            new_price = float(ad_list[new_pos][0]) + step
                        elif curr_pos < new_pos:
                            new_price = float(ad_list[new_pos][0]) - step
                    if int(curr_pos) == int(new_pos):
                        new_price = below_user_price + step
                        if ad_list[len(ad_list)-1][1] == r('profile_name'):
                            new_price = below_user_price
                    if new_price > max_price:
                        new_price = max_price

                # ## ## ## ## #
                #
                #       BUY AD MARGIN BOT TYPE
                #
                # ##

                elif r('bot_type') == 'buy_ad_margin':
                    sell_bot_id = r('sell_ad_ref')

                    if q('bot_sets', 'onoff', 'bot_id', sell_bot_id) == 0:
                        m_url = q('bot_sets', 'method_url',
                                  'bot_id', sell_bot_id)
                        sref_ad_list = self.adList(m_url)
                        sell_price = float(sref_ad_list[0][0])
                        print(sell_price)
                    else:
                        sell_price = q(
                            'bot_sets', 'price', 'bot_id', sell_bot_id)
                    sell_currency = q(
                        'bot_sets', 'currency', 'bot_id', sell_bot_id)
                    buy_currency = r('currency')
                    exch_curr_rate = api.get_fiat_currency_rates(
                        sell_currency, r('currency'))
                    s(buy_currency+'_'+sell_currency, exch_curr_rate)
                    exch_d = fiat_exc_rate()

                    local_fee = 2
                    fee_total = r('fee_total')
                    margin = r('margin')
                    fee_sum = fee_total + margin + local_fee

                    buy_price = sell_price / exch_d[2]
                    buy_price -= buy_price / 100 * fee_sum
                    new_price = buy_price

                    if float(new_price) > float(ad_list[new_pos][0]):
                        new_price = float(ad_list[new_pos][0]) - step

                    sell_pr = sell_price / exch_d[2]
                    profit = sell_pr / new_price  # 1,14
                    costs = (local_fee + fee_total)/100
                    profit = ((profit - costs) * 100) - 100
                    w('color', profit)

                curr_koeff = new_price / aver_price
                print('curr_koeff: ' + str(curr_koeff))
                print('new_price: ' + str(new_price))

                # Making sure we change the price slowly, by 2% each cycle
                new_price_dif_perc = abs(curr_price / new_price * 100 - 100)
                if new_price_dif_perc > 2:
                    if new_price > curr_price:
                        new_price = curr_price * 1.02
                    elif new_price < curr_price:
                        new_price = curr_price * 0.98

                # Sending new price to localbitcoins only if the price has been changed
                if new_price != curr_price:
                    price_equation = str(
                        self.price_formula()) + str(curr_koeff)
                    api.price_eq(self.conn, r('ad_id'), price_equation)
                    print('New price has been sent')

                # Saving some settings to DB
                w('koeff', curr_koeff)
                w('last_time_upd', time.time())

        # Autoreply
        self.autoreply()

    def autoreply(self):

        if r('autoreply_onoff') == True:
            trades_db = r('trades')
            if '[' not in trades_db:
                print('not in trades_db')
                trades_db = []
            else:
                trades_db = trades_db.replace('[', '')
                trades_db = trades_db.replace(']', '')
                trades_db = trades_db.replace(' ', '')
                if ',' in trades_db:
                    trades_db = trades_db.split(',')
                else:
                    if len(trades_db) > 0:
                        trades_db = [trades_db]

            dashboard = api.get_open_trades(self.conn)
            tr_count = dashboard['data']['contact_count']

            trades_dashboard = []
            for i in range(tr_count):
                if dashboard['data']['contact_list'][i]['data']['advertisement']['id'] == r('ad_id'):
                    trades_dashboard.append(
                        dashboard['data']['contact_list'][i]['data']['contact_id'])

            trades_dashboard_new = []
            for i in range(tr_count):
                if str(trades_dashboard[i]) not in trades_db:
                    trades_dashboard_new.append(trades_dashboard[i])

            trades_db = trades_dashboard

            trades_messaged = []
            if len(trades_dashboard_new) > 0:
                for i in range(len(trades_dashboard_new)):
                    send_mess = api.send_message(
                        self.conn, trades_dashboard_new[i], r('autoreply_msg'))
                    trades_messaged.append(trades_dashboard_new[i])
                for i in range(len(trades_messaged)):
                    trades_db.append(trades_messaged[i])
            w('trades', trades_db)


def localbot(body=None, soul=None):
    if body != None:
        run = body.run
        localbot.dbEx = body.dbEx
        localbot.bot_id = body.bot_id
        return run()
    if soul != None:
        localbot.dbEx = soul.dbEx
        localbot.bot_id = soul.bot_set['bot_id']
        self = soul
        # Хитрые функции

        # read_bot_single_set


def r(x): return localbot.dbEx.read_bot_single_set(localbot.bot_id, x)


# write_bot_single_set

def w(x, y): return localbot.dbEx.write_bot_single_set(
    localbot.bot_id, x, y)

# db_get_cell


def q(t, c, k, v): return localbot.dbEx.db_get_cell(t, c, k, v)

# read_settings_single


def o(x): return localbot.dbEx.read_settings_single(x)

# write_settings_single


def s(x, y): return localbot.dbEx.write_settings_single(x, y)


def fiat_exc_rate():
    sell_bot_id = r('sell_ad_ref')
    sell_price = q(
        'bot_sets', 'price', 'bot_id', sell_bot_id)
    sell_currency = q(
        'bot_sets', 'currency', 'bot_id', sell_bot_id)
    buy_currency = r('currency')
    try:
        exch_curr_rate = api.get_fiat_currency_rates(
            sell_currency, r('currency'))
        s(buy_currency+'_'+sell_currency, exch_curr_rate)
    except:
        buy_currency = r('currency')
        sell_currency = q('bot_sets', 'currency', 'bot_id',
                          self.bot_set['sell_ad_ref'])
        exch_curr_rate = o(str(buy_currency) + '_' + str(sell_currency))
    return [buy_currency, sell_currency, exch_curr_rate]
