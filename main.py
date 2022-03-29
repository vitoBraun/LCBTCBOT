import sys

from ui import Ui_MainWindow
import sqlite3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCheckBox, QDialog, QMessageBox
from PyQt5.QtGui import QFont

from PyQt5.QtCore import pyqtSignal, QObject, QMutex, pyqtSlot, Qt

import json

import time
import datetime
from pytz import timezone
import pytz

import db.db as db

from lbcapi import api
import bot
from bot import LocalBitcoinsBot
from bot import r, w, q, s, o
from dialogs import MyDialogs, AddProfile, AddBot, AddBot_sref, ChooseBot_sref,  profiles_data_load
import csv
from db.tz import tzones


class BotThread(QtCore.QThread):  # dedicated thread for bot connection and calculations
    connection_Ok = pyqtSignal(str)
    no_connection = pyqtSignal(str)
    bot_loaded = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.flag = 0
        self.dbEx = db.dbExecutor
        self.dbEx.create_settings_table()

    def run(self):
        while self.flag == 1:
            try:
                self.cycle()
            except:
                print(
                    'Some data absense in this cycle, trying next time')

    def stop(self):
        self.flag = 0

    def cycle(self):
        bot_sets = self.dbEx.get_botsets()
        y = len(bot_sets) - 1
        urls = []
        i = 0
        while i <= y:
            if api.internet_on() == True:
                sign = str("Ok")
                self.connection_Ok.emit(sign)
                if bot_sets[i]['method_url'] not in urls:
                    conn = sqlite3.connect(
                        "db/db.db", check_same_thread=False)
                    cursor = conn.cursor()
                    cnn = cursor.execute(
                        "SELECT api_key, api_secret FROM local_profiles WHERE profile_name = '%s'" % bot_sets[i]['profile_name'])
                    cnn = cnn.fetchall()
                    api_key = cnn[0][0]
                    api_secret = cnn[0][1]
                    api_conn = api.hmac(api_key, api_secret)
                    url_str = bot_sets[i]['method_url'].replace(
                        '.json', '')
                    url_str = url_str.replace('/', '_')
                    filepath = 'db/ad_lists/' + url_str + 'json.json'
                    response = api.get_ad_list(
                        api_conn, bot_sets[i]['method_url'])
                    with open(filepath, 'w') as json_file:
                        json.dump(response, json_file)
                    urls.append(bot_sets[i]['method_url'])
                    conn.commit()
                    conn.close()
                bot_id = bot_sets[i]['bot_id']
                from bot import w, q, s, o, r, localbot
                localbot(LocalBitcoinsBot(bot_id), 1)
                self.bot_loaded.emit(1)
                time.sleep(1)
                i += 1
                if i == y:
                    urls = []
            else:
                sign = 'No'
                self.no_connection.emit(sign)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    ## #       # #    # # # #          # #     # # #    # # #
    #   #     #   #      #           #   #     #    #   #    #
    # #       #   #      #           #   #     # # #    # # #
    #   #     #   #      #           # # #     #        #
    ## #       # #       #           #   #     #        #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class BotApp(Ui_MainWindow):
    def __init__(self, MainWindow):
        MainWindow.__init__()
        self.dbEx = db.dbExecutor

        self.botThread = BotThread()
        self.botThread.start()
        self.botThread.flag = 1

        self.botThread.bot_loaded.connect(self.refresh_values)
        self.botThread.no_connection.connect(self.connection_check)
        self.botThread.connection_Ok.connect(self.connection_check)

    def func_to_start_Load_and_shift(self):
        self.refreshBtn.setText("...")
        self.refreshBtn.setDisabled(True)

        # NEW OBJECT profiles_data_load of thread
        self.profiles_data = profiles_data_load()
        self.profiles_data.on_startLoad.connect(self.onStartLoad)
        self.profiles_data.on_finishLoad.connect(self.onFinishSignal)
        self.profiles_data.start()
        self.profiles_data.reload = 1

    def onStartLoad(self, text):
        self.botThread.flag = 0
        self.botThread.terminate()
        self.refreshBtn.setText(text)
        self.profiles_data.reload = 1

    def onFinishSignal(self, text):
        self.botThread.flag = 1
        self.botThread.start()
        self.refreshBtn.setEnabled(True)
        self.refreshBtn.setText('refresh')

    def connection_check(self, sign):
        if sign == 'Ok':
            self.printstate(
                '<font color=green>Connected</font>')
        if sign == "No":
            self.printstate('<font color=red>No connection</font>')

    def run(self):
        self.setupUi(MainWindow)
        self.load_profiles_list()
        self.load_bot_sets_list()
        self.bot_switcher_load()
        bc = self.dbEx.read_settings_single('last_open_bot')
        self.bot_switch.setCurrentIndex(int(bc))
        self.refresh_values()

        # EVENT LISTENERS (CLICK, TEXT/ VALUE CHNAGE, ETC...)
        self.onoff.clicked.connect(self.switch_bot_onoff)
        self.autoreply_onoff.clicked.connect(self.switch_autoreply_onoff)
        self.min_price_onoff.clicked.connect(self.switch_min_price_onoff)
        self.min_price.textChanged.connect(self.min_price_change)
        self.min_koeff.valueChanged.connect(self.min_koeff_change)
        self.listWidget.clicked.connect(self.new_pos_change)
        self.autoreply_msg.textChanged.connect(self.autoreply_msg_change)
        self.add_profile.clicked.connect(self.add_profile_w)
        self.add_bot.clicked.connect(self.add_bot_w)
        self.delete_profile.clicked.connect(self.delete_profile_w)
        self.delete_bot_set.clicked.connect(self.delete_bot_set_w)
        self.refreshBtn.clicked.connect(self.func_to_start_Load_and_shift)
        self.bot_switch.currentTextChanged.connect(self.refresh_values)
        self.sell_ad_ref.clicked.connect(self.find_sell_bot)

        self.domain.currentTextChanged.connect(lambda: self.dbEx.write_settings_single(
            'domain', self.domain.currentText()))

        self.time_zone.clear()
        for i in range(len(tzones)-1):
            self.time_zone.addItem(tzones[i])

        self.time_zone.currentTextChanged.connect(lambda: self.dbEx.write_settings_single(
            'time_zone', self.time_zone.currentText()))

        self.total_fees.valueChanged.connect(lambda: self.dbEx.write_bot_single_set(self.bot_set['bot_id'],
                                                                                    'fee_total', self.total_fees.value()))
        try:
            self.domain.setCurrentText(
                self.dbEx.read_settings_single('domain'))

            self.time_zone.setCurrentText(
                self.dbEx.read_settings_single('time_zone'))
        except:
            pass

    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)

    def bot_switcher_load(self):  # LOAD BOT_SETS LIST INTO COMBOBOX SWITCHER
        self.bot_switch.clear()
        rows = self.dbEx.db_get_table('bot_sets')
        for i in rows:
            item = str(i[1]) + ' ' + str(i[7]) + ' ' + str(i[6])
            if str(i[3]) == 'buy_ad_margin':
                item += ' buy_ad_margin'
            self.bot_switch.addItem(item)

    def refresh_values(self):
        combo0 = False
        if self.bot_switch.currentText() == '':
            self.bot_switch.setCurrentIndex(0)
            if self.bot_switch.currentText() == '':
                combo0 = True

        if combo0 == False:
            bot_id = self.bot_switch.currentText().split()
            bot_id = bot_id[0]

            self.bot_set = self.dbEx.read_bot_set(bot_id)
            self.load_ad_list()

            self.dbEx.write_settings_single(
                'last_open_bot', self.bot_switch.currentIndex())

            # SHOW OR HIDE AUTOREPLY TEXT FIELD DEPENDS ON IT'S STATE ON OR OFF
            self.autoreply_msg.setDisabled(False)
            self.autoreply_onoff.setChecked(True)
            if self.bot_set['autoreply_onoff'] == False:
                self.autoreply_onoff.setChecked(False)
                self.autoreply_msg.setDisabled(True)
                self.autoreply_msg.setText(
                    str(self.bot_set['autoreply_msg']))
            # refresh min_koeff value to label
            self.label_5.setText('Set min koeff')
            self.min_koeff.setValue(self.bot_set['min_koeff'])
            # refresh min_amount value to label
            self.min_amount.setText(str(self.bot_set['min_amount']))
            # refresh current price value to label
            self.curr_price.setText(str(dy(self.bot_set['price'])))
            self.curr_koeff.setText(
                str(round(float(self.bot_set['koeff']), 3)))
            self.curr_diff.hide()

            if self.bot_set['bot_type'] == 'sell_ad_position':
                # SET MIN PRICE SWITCH ON / OFF
                self.min_price.show()
                self.min_price.setDisabled(False)
                self.min_price.setText(str(dy(self.bot_set['min_price'])))
                self.min_price_onoff.show()
                self.label_6.show()
                self.label_9.hide()
                self.total_fees.hide()
                self.min_koeff.setSingleStep(0.01)
                self.sell_ad_ref.hide()
                self.label_10.hide()
                self.curr_margin.hide()

            elif self.bot_set['bot_type'] == 'buy_ad_position':
                self.label_5.setText('Set max koeff')
                self.min_price.hide()
                self.min_price_onoff.hide()
                self.label_6.hide()
                self.label_9.hide()
                self.total_fees.hide()
                self.min_koeff.setSingleStep(0.01)
                self.sell_ad_ref.hide()
                self.label_10.hide()
                self.curr_margin.hide()

            elif self.bot_set['bot_type'] == 'buy_ad_margin':
                self.check_sell_ad_ref_exist()
                self.label_5.setText('Set margin %')
                self.min_price.hide()
                self.min_price_onoff.hide()
                self.label_6.hide()
                self.label_9.show()
                self.total_fees.setSingleStep(0.1)
                self.min_koeff.setSingleStep(0.1)
                self.total_fees.setValue(self.bot_set['fee_total'])
                self.min_koeff.setValue(self.bot_set['margin'])
                self.total_fees.show()
                self.sell_ad_ref.show()

                self.label_10.show()

                self.curr_margin.show()
                try:
                    margi = self.dbEx.read_bot_single_set(
                        bot_id, 'color')
                    if margi == '':
                        margi = 1
                    self.curr_margin.setText(str(margi))
                    self.bot_set['fee_total']
                except:
                    pass
                self.curr_diff.show()
                from bot import w, q, s, o, r, localbot
                localbot(None, self)

                try:
                    bcur = r('currency')
                    scur = q('bot_sets', 'currency', 'bot_id',
                             self.bot_set['sell_ad_ref'])
                    if str(bcur) != str(scur):
                        exch_rt = o(str(bcur) + '_' + str(scur)) + \
                            ' ' + str(bcur) + '/' + str(scur)
                    else:
                        exch_rt = str(bcur) + '/' + str(scur)
                    self.curr_diff.setText(exch_rt)
                except:
                    self.curr_diff.setText('No Data')

            # # refresh last time update to it's label
            tz = self.dbEx.read_settings_single('time_zone')
            native = datetime.datetime.utcfromtimestamp(
                int(self.bot_set['last_time_upd']))
            utc = pytz.utc
            gmt5 = pytz.timezone(tz)
            last_time = utc.localize(native).astimezone(
                gmt5).strftime('%H:%M:%S')
            self.last_time_upd.setText(str(last_time))

            # SET BOT SWITCH ON / OFF
            if self.bot_set['onoff'] == 1:
                self.onoff.setChecked(True)
                self.listWidget.setDisabled(False)
            elif self.bot_set['onoff'] == 0:
                self.onoff.setChecked(False)
                self.listWidget.setDisabled(True)

            if self.bot_set['min_price_onoff'] == 1:
                self.min_price_onoff.setChecked(True)
                self.min_price.setDisabled(False)
            else:
                self.min_price_onoff.setChecked(False)
                self.min_price.setDisabled(True)

            self.autoreply_msg.setText(self.bot_set['autoreply_msg'])
            self.bot_set['autoreply_msg'] = self.autoreply_msg.toPlainText()

    def printstate(self, text):
        self.botstate.setText(text)

    def ShowMessage(self, text, notif=False):
        msg = QMessageBox()
        msg.setText(text)
        if notif == True:
            pass
        else:
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.buttonClicked.connect(self.delete_confirm)
        x = msg.exec_()

    def checkbox_change(self, checkbox_name):
        state = 0
        checkbox_list = {
            'onoff': self.onoff,
            'autoreply_onoff': self.autoreply_onoff,
            'min_price_onoff': self.min_price_onoff
        }
        checkbox = checkbox_list[checkbox_name]
        if checkbox.isChecked() == True:
            print(checkbox_name + ' On')
            state = 1
        elif checkbox.isChecked() == False:
            print(checkbox_name + ' Off')
            state = 0
        self.dbEx.write_bot_single_set(
            self.bot_set['bot_id'], checkbox_name, state)

    def switch_bot_onoff(self):
        self.checkbox_change('onoff')
        if self.onoff.isChecked():
            self.listWidget.setDisabled(0)
        else:
            self.listWidget.setDisabled(1)

    def switch_autoreply_onoff(self):
        self.checkbox_change('autoreply_onoff')
        self.autoreply_msg.setDisabled(True)
        if self.autoreply_onoff.isChecked() == True:
            self.autoreply_msg.setDisabled(False)

    def switch_min_price_onoff(self):
        self.checkbox_change('min_price_onoff')
        if self.bot_set['min_price_onoff'] == 1:
            self.min_price.setDisabled(True)
        else:
            self.min_price.setDisabled(False)

    def min_price_change(self):
        min_price = self.min_price.text()
        if min_price == '':
            print('You can\'t set the price lower 0')
        else:
            min_price = min_price.replace(' ', '')
            self.dbEx.write_bot_single_set(
                self.bot_set['bot_id'], 'min_price', float(min_price))

    def min_koeff_change(self):
        min_koeff = self.min_koeff.value()
        if min_koeff == '':
            print('You can\'t set the koefficient lower 0')
        else:
            if self.bot_set['bot_type'] == 'buy_ad_margin':
                self.dbEx.write_bot_single_set(
                    self.bot_set['bot_id'], 'margin', min_koeff)
            else:
                self.dbEx.write_bot_single_set(
                    self.bot_set['bot_id'], 'min_koeff', min_koeff)

    def load_ad_list(self):
        listW = self.listWidget
        listW.clear()
        choosen_bot_id = self.bot_switch.currentText().split()
        choosen_bot_id = choosen_bot_id[0]
        try:
            with open('db/ad_lists/'+choosen_bot_id+'.csv', 'r') as fp:
                reader = csv.reader(fp, delimiter=',', quotechar='"')
                data_read = [row for row in reader]
                for i in range(len(data_read)):
                    string = str(
                        dy(float(data_read[i][0])) + '      ' + data_read[i][1])
                    listW.addItem(string)
                    if data_read[i][1] == self.bot_set['profile_name']:
                        listW.item(i).setFont(QFont('', 0, QFont.Bold))
                if len(data_read) < 3:
                    listW.setCurrentRow(len(data_read)-1)
                else:
                    listW.setCurrentRow(self.bot_set['new_pos'])
        except:
            listW.addItem('Here is empty')
            pass

    def load_profiles_list(self):
        listW = self.profiles
        listW.clear()
        rows = self.dbEx.db_get_table('local_profiles')
        for i in rows:
            listW.addItem(i[1])
        listW.setCurrentRow(0)

    def load_bot_sets_list(self):
        listW = self.bot_sets
        listW.clear()
        rows = self.dbEx.db_get_table('bot_sets')
        for i in rows:
            item = (str(i[1] + ' ' + i[7]+' '+i[6]))
            if str(i[3]) == 'buy_ad_margin':
                item += ' buy_ad_margin'
            listW.addItem(item)
        listW.setCurrentRow(0)

    def new_pos_change(self):
        self.dbEx.write_bot_single_set(
            self.bot_set['bot_id'], 'new_pos', self.listWidget.currentRow())

    def autoreply_msg_change(self):
        self.dbEx.write_bot_single_set(
            self.bot_set['bot_id'], 'autoreply_msg',  self.autoreply_msg.toPlainText())

    def add_profile_w(self):
        AddProfile()
        self.load_profiles_list()
        self.refresh_values()

    def add_bot_w(self):
        AddBotObj = AddBot(self)
        self.bot_switcher_load()
        self.load_bot_sets_list()
        self.refresh_values()

    def add_bot_w_sref(self, margin_bot_id):
        AddBot_sref(margin_bot_id)
        self.bot_switcher_load()
        self.load_bot_sets_list()
        self.refresh_values()

    def choose_bot_w_sref(self):
        ChooseBot_sref(self.bot_set)
        self.bot_switcher_load()
        self.load_bot_sets_list()
        self.refresh_values()

    def delete_profile_w(self):
        try:
            profile_name = self.profiles.currentItem().text()
            self.profile_to_del = profile_name
            self.ShowMessage('Sure want to delete ' + str(profile_name) + ' ?')
            self.load_profiles_list()
            self.refresh_values()
        except:
            print('Tried to delete nothing')

    def delete_bot_set_w(self):
        try:
            bot_id = self.bot_sets.currentItem().text().split()
            bot_id = bot_id[0]
            self.bot_set_to_del = bot_id
            self.ShowMessage('Sure want to delete ' + str(bot_id) + ' ?')
            self.bot_switcher_load()
            self.load_bot_sets_list()
            self.refresh_values()
        except:
            print('Tried to delete nothing')

    def delete_confirm(self, i):
        if i.text() == 'OK':
            try:
                self.dbEx.delete_bot_set(self.bot_set_to_del)
            except:
                pass
            try:
                self.dbEx.delete_profile(self.profile_to_del)
            except:
                pass

    def change_bot(self, sell_ad_ref=None):
        if self.sref != None:
            if sell_ad_ref == None:
                sell_ad_ref = self.bot_set['sell_ad_ref']
            cnt = self.bot_switch.count()
            for i in range(cnt):
                bid = self.bot_switch.itemText(i).split()
                bid = bid[0]
                if bid == sell_ad_ref:
                    index = i
            self.bot_switch.setCurrentIndex(index)
        else:
            self.find_sell_bot()

    def check_sell_ad_ref_exist(self):
        try:
            x = self.dbEx.read_bot_single_set(
                self.bot_set['sell_ad_ref'], 'bot_id')
            self.sell_ad_ref.setText(
                'Attached to ' + self.bot_set['sell_ad_ref'])
            self.sref = self.bot_set['sell_ad_ref']
        except:
            self.sell_ad_ref.setText(
                'Bot deleted, attach another:...')
            self.sref = None

    def find_sell_bot(self):
        if self.sref == None:
            bot_sets = self.dbEx.get_botsets()
            cnt = len(bot_sets)
            for i in range(cnt):
                if bot_sets[i]['trade_type'] == 'ONLINE_SELL':
                    result = True
                    break
                if i == cnt-1:
                    result = False
                    break
            if result == False:
                self.add_bot_w_sref(self.bot_set['bot_id'])
            else:
                self.choose_bot_w_sref()
        else:
            self.change_bot()


if __name__ == "__main__":
    def dy(x): return '{0:,}'.format(x).replace(',', ' ')
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QTabWidget()
    Bot = BotApp(MainWindow)
    Bot.run()
    MainWindow.show()
    sys.exit(app.exec_())
