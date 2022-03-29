from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
from lbcapi import api
from db.db import dbExecutor
import json
import os.path
import time
from PyQt5.QtCore import pyqtSignal, QObject, QMutex, pyqtSlot, Qt


class MyDialogs(QtWidgets.QDialog, QtCore.QObject):
    def __init__(self):
        self.dbExecutor = dbExecutor
        QtWidgets.QDialog.__init__(self)
        QtCore.QObject.__init__(self)

    def load_sell_bots(self):
        rows = self.dbExecutor.db_get_table('bot_sets')
        for i in rows:
            if str(i[5]) == 'ONLINE_SELL':
                self.ad_id_2.addItem(
                    str(i[1]) + ' ' + str(i[7]) + ' ' + str(i[6]))


class profiles_data_load(QtCore.QThread):
    on_startLoad = pyqtSignal(str)
    on_finishLoad = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.reload = 0

    def run(self):
        # db = dbExecutor
        local_profiles = dbExecutor.get_local_profiles()
        try:
            text_proc = '.'
            for i in range(len(local_profiles)):
                api_key = local_profiles[i]['api_key']
                api_secret = local_profiles[i]['api_secret']
                api_conn = api.hmac(api_key, api_secret)
                filepath = 'db/profile_data/' + \
                    local_profiles[i]['profile_name'] + '.json'
                if os.path.exists(filepath) == False or self.reload == 1:
                    print(str(i)+' getting profile datas refresh')
                    data = api.get_profile_ads(api_conn)
                    with open(filepath, 'w') as json_file:
                        json.dump(data, json_file)
                self.on_startLoad.emit(text_proc)
                text_proc += text_proc
            text_finish = 'done'
            self.on_finishLoad.emit(text_finish)
        except:
            print('fails')


def ShowMessage(text, type=''):
    msg = QMessageBox()
    msg.setText(text)
    if type == 'Critical':
        msg.setIcon(QMessageBox.Critical)
    x = msg.exec_()


class AddProfile(MyDialogs):
    def __init__(self, load_profiles_list=0):
        MyDialogs.__init__(self)
        self.dbExecutor = dbExecutor
        self.setupUi()

    def setupUi(self):
        add_profile_dialog = self
        add_profile_dialog.setObjectName("add_profile_dialog")
        add_profile_dialog.resize(567, 136)
        add_profile_dialog.setMinimumSize(QtCore.QSize(567, 136))
        add_profile_dialog.setMaximumSize(QtCore.QSize(567, 136))
        self.profile_name = QtWidgets.QTextEdit(add_profile_dialog)
        self.profile_name.setGeometry(QtCore.QRect(130, 20, 241, 21))
        self.profile_name.setObjectName("profile_name")
        self.pushButton = QtWidgets.QPushButton(add_profile_dialog)
        self.pushButton.setGeometry(QtCore.QRect(390, 10, 141, 32))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(add_profile_dialog)
        self.label.setGeometry(QtCore.QRect(30, 20, 101, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(add_profile_dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 101, 16))
        self.label_2.setObjectName("label_2")
        self.api_key = QtWidgets.QTextEdit(add_profile_dialog)
        self.api_key.setGeometry(QtCore.QRect(130, 50, 401, 21))
        self.api_key.setObjectName("api_key")

        self.api_secret = QtWidgets.QTextEdit(add_profile_dialog)
        self.api_secret.setGeometry(QtCore.QRect(130, 80, 401, 41))
        self.api_secret.setObjectName("api_secret")
        self.label_3 = QtWidgets.QLabel(add_profile_dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 80, 101, 16))
        self.label_3.setObjectName("label_3")
        self.retranslateUi(add_profile_dialog)
        QtCore.QMetaObject.connectSlotsByName(add_profile_dialog)

    def retranslateUi(self, add_profile_dialog):
        _translate = QtCore.QCoreApplication.translate
        add_profile_dialog.setWindowTitle(_translate(
            "add_profile_dialog", "Add Localbitcoins profile"))
        self.pushButton.setText(_translate("add_profile_dialog", "Add"))
        self.label.setText(_translate("add_profile_dialog", "Profile name"))
        self.label_2.setText(_translate("add_profile_dialog", "API Key"))
        self.label_3.setText(_translate("add_profile_dialog", "API Secret"))

        self.pushButton.clicked.connect(self.add_profile_w)

        self.exec_()

    def add_profile_w(self):
        profile_name = self.profile_name.toPlainText()
        api_key = self.api_key.toPlainText()
        api_secret = self.api_secret.toPlainText()
        conn = api.hmac(api_key, api_secret)
        try:
            profile_info = conn.call('GET', '/api/myself/').json()
            if profile_name == profile_info['data']['username']:
                self.dbExecutor.add_profile(profile_name, api_key, api_secret)
                ShowMessage(
                    'You have added your Localbitcoins profile')
                self.close()
            else:
                ShowMessage('Keys are ok, but wrong profile name', 'Critical')
        except:
            ShowMessage('Wrong data, or no connection', 'Critical')


class AddBot(MyDialogs):
    def __init__(self, MainWindow):
        MyDialogs.__init__(self)
        self.MainWindow = MainWindow
        self.setupUi()

    def setupUi(self):
        AddBot = self
        AddBot.setObjectName("AddBot")
        AddBot.resize(321, 206)
        self.profile = QtWidgets.QComboBox(AddBot)
        self.profile.setGeometry(QtCore.QRect(150, 40, 161, 32))
        self.profile.setObjectName("profile")
        self.profile.addItem("")
        self.bot_type = QtWidgets.QComboBox(AddBot)
        self.bot_type.setGeometry(QtCore.QRect(150, 80, 161, 32))
        self.bot_type.setObjectName("bot_type")
        self.bot_type.addItem("")
        self.bot_type.addItem("")
        self.bot_type.addItem("")
        self.ad_id = QtWidgets.QComboBox(AddBot)
        self.ad_id.setGeometry(QtCore.QRect(150, 120, 161, 32))
        self.ad_id.setObjectName("ad_id")
        self.label = QtWidgets.QLabel(AddBot)
        self.label.setGeometry(QtCore.QRect(20, 47, 131, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(AddBot)
        self.label_2.setGeometry(QtCore.QRect(40, 90, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(AddBot)
        self.label_3.setGeometry(QtCore.QRect(40, 130, 81, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(AddBot)
        self.label_4.setGeometry(QtCore.QRect(10, 170, 141, 16))
        self.label_4.setObjectName("label_4")
        self.ad_id_2 = QtWidgets.QComboBox(AddBot)
        self.ad_id_2.setEnabled(False)
        self.ad_id_2.setGeometry(QtCore.QRect(150, 160, 161, 32))
        self.ad_id_2.setObjectName("ad_id_2")
        self.pushButton = QtWidgets.QPushButton(AddBot)
        self.pushButton.setGeometry(QtCore.QRect(20, 10, 121, 31))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(AddBot)

        QtCore.QMetaObject.connectSlotsByName(AddBot)

    def retranslateUi(self, AddBot):
        _translate = QtCore.QCoreApplication.translate
        AddBot.setWindowTitle(_translate("AddBot", "Add Bot"))
        self.bot_type.setItemText(0, _translate("AddBot", "sell_ad_position"))
        self.bot_type.setItemText(1, _translate("AddBot", "buy_ad_position"))
        self.bot_type.setItemText(2, _translate("AddBot", "buy_ad_margin"))
        self.label.setText(_translate("AddBot", "Localbitcoins profile"))
        self.label_2.setText(_translate("AddBot", "Bot type"))
        self.label_3.setText(_translate("AddBot", "Ad"))
        self.label_4.setText(_translate("AddBot", "Sell Bot (buy_ad_margin)"))
        self.pushButton.setText(_translate("AddBot", "Add bot"))
        self.load_profiles_combo()

        self.load_ads()
        self.load_ad_ids()

        self.profile.currentTextChanged.connect(self.load_ads)
        self.bot_type.currentTextChanged.connect(self.load_ad_ids)
        self.ad_id.currentTextChanged.connect(self.refresh_ad_ids)
        self.pushButton.clicked.connect(self.add_bot)
        if self.ad_id.itemText(0) == '':
            self.pushButton.setDisabled(True)
        self.exec_()

    def load_profiles_combo(self):
        self.profile.clear()
        rows = self.dbExecutor.db_get_table('local_profiles')
        for i in rows:
            self.profile.addItem(i[1])

    def load_ads(self):
        self.current_prof = str(self.profile.currentText())
        key_secret = [self.dbExecutor.db_get_cell('local_profiles', 'api_key',
                                                  'profile_name', self.current_prof), self.dbExecutor.db_get_cell('local_profiles', 'api_secret',
                                                                                                                  'profile_name', self.current_prof)]
        self.conn = api.hmac(key_secret[0], key_secret[1])
        try:
            filepath = 'db/profile_data/' + \
                self.current_prof + '.json'
            with open(filepath, 'r') as f:
                self.ads = json.load(f)
        except:
            self.ads = api.get_profile_ads(self.conn)
        self.load_ad_ids()

    def load_ad_ids(self):
        self.current_bot_type = str(self.bot_type.currentText())
        self.bot_set = {}
        if self.current_bot_type == 'sell_ad_position':
            self.ad_id.clear()
            self.ad_id_2.setEnabled(False)
            for i in self.ads['data']['ad_list']:
                if i['data']['trade_type'] == 'ONLINE_SELL':
                    self.bot_set['trade_type'] = 'ONLINE_SELL'
                    self.ad_id.addItem(
                        str(i['data']['ad_id']) + ' ' + str(i['data']['currency']) + ' ' + str(i['data']['online_provider']))
        if self.current_bot_type == 'buy_ad_position':
            self.ad_id.clear()
            self.ad_id_2.setEnabled(False)
            for i in self.ads['data']['ad_list']:
                if i['data']['trade_type'] == 'ONLINE_BUY':
                    self.bot_set['trade_type'] = 'ONLINE_BUY'
                    self.ad_id.addItem(
                        str(i['data']['ad_id']) + ' ' + str(i['data']['currency']) + ' ' + str(i['data']['online_provider']))

        if self.current_bot_type == 'buy_ad_margin':
            self.ad_id.clear()
            self.ad_id_2.setEnabled(True)
            for i in self.ads['data']['ad_list']:
                if i['data']['trade_type'] == 'ONLINE_BUY':
                    self.bot_set['trade_type'] = 'ONLINE_BUY'
                    self.ad_id.addItem(
                        str(i['data']['ad_id']) + ' ' + str(i['data']['currency']) + ' ' + str(i['data']['online_provider']))
            self.ad_id_2.clear()
            rows = self.dbExecutor.db_get_table('bot_sets')
            for i in rows:
                if str(i[5]) == 'ONLINE_SELL':
                    self.ad_id_2.addItem(
                        str(i[1]) + ' ' + str(i[7]) + ' ' + str(i[6]))

    def refresh_ad_ids(self):
        self.ad = self.ad_id.currentText().split(' ')
        if self.ad_id.itemText(0) != '':
            self.pushButton.setDisabled(False)
        else:
            self.pushButton.setDisabled(True)

    def add_bot(self, sref_bot_id=None):
        for i in self.ads['data']['ad_list']:
            if i['data']['ad_id'] == int(self.ad[0]):
                self.bot_set['price'] = i['data']['temp_price']
                self.bot_set['min_amount'] = i['data']['min_amount']
                self.bot_set['max_amount'] = i['data']['max_amount']

        self.sell_ad_ref = self.ad_id_2.currentText().split(' ')
        self.bot_set['sell_ad_ref'] = str(self.sell_ad_ref[0])

        self.bot_set = {
            'bot_id': str(str(self.current_prof) + '_' + str(self.bot_set['trade_type']) + '_' + str(self.ad[0])),
            'profile_name': self.current_prof,
            'bot_type': self.current_bot_type,
            'ad_id':  self.ad[0],
            'trade_type': self.bot_set['trade_type'],
            'currency': self.ad[1],
            'online_provider': self.ad[2],
            'method_url': '',
            'price': self.bot_set['price'],
            'min_amount': self.bot_set['min_amount'],
            'max_amount': self.bot_set['max_amount'],
            'sell_ad_ref': self.bot_set['sell_ad_ref']
        }

        if self.bot_set['trade_type'] == 'ONLINE_SELL':
            trade_type_path = 'buy-bitcoins-online'
        elif self.bot_set['trade_type'] == 'ONLINE_BUY':
            trade_type_path = 'sell-bitcoins-online'
        # try:
        payment_methods = api.payment_methods(self.conn)
        pList = {}
        i = 0
        for key in payment_methods['data']['methods']:
            pList[i] = {'count': i, 'name': key,
                        'code': payment_methods['data']['methods'][key]['code']}
            if pList[i]['code'] == self.bot_set['online_provider']:
                method_name = pList[i]['name']
        i += 1
        # except:
        # print('could not get payment_methods')

        method_url = '/' + str(trade_type_path) + '/' + \
            str(self.bot_set['currency'].lower()) + \
            '/' + str(method_name) + '/.json'
        self.bot_set['method_url'] = method_url
        # try:
        if sref_bot_id != None:
            self.dbExecutor.write_bot_single_set(
                sref_bot_id, 'sell_ad_ref', self.bot_set['bot_id'])
        try:
            self.dbExecutor.add_bot_set(self.bot_set)
            ShowMessage('Bot set has been added!')
        except:
            ShowMessage('This bot set already exists!', 'Critical')
        self.close()


class AddBot_sref(AddBot):
    def __init__(self, margin_bot_id, parent=None):
        self.margin_bot_id = margin_bot_id
        AddBot.__init__(self, parent)

    def retranslateUi(self, AddBot):

        _translate = QtCore.QCoreApplication.translate
        AddBot.setWindowTitle(_translate(
            "AddBot", "Add Sell bot for buy_ad_margin"))
        self.bot_type.setItemText(0, _translate("AddBot", "sell_ad_position"))

        self.bot_type.removeItem(1)
        self.bot_type.removeItem(1)
        self.bot_type.setDisabled(True)

        self.label.setText(_translate("AddBot", "Localbitcoins profile"))
        self.label_2.setText(_translate("AddBot", "Bot type"))
        self.label_3.setText(_translate("AddBot", "Ad"))
        self.label_4.setText(_translate("AddBot", "Sell Bot (buy_ad_margin)"))
        self.label_4.hide()
        self.ad_id_2.hide()
        self.pushButton.setText(_translate("AddBot", "Add bot"))

        self.load_profiles_combo()
        self.load_ads()
        self.load_ad_ids()

        self.profile.currentTextChanged.connect(self.load_ads)
        self.bot_type.currentTextChanged.connect(self.load_ad_ids)
        self.ad_id.currentTextChanged.connect(self.refresh_ad_ids)
        self.pushButton.clicked.connect(
            lambda: self.add_bot(self.margin_bot_id))
        self.exec_()


class ChooseBot_sref(MyDialogs):
    def __init__(self, bot_set, parent=None):
        self.bot_set = bot_set
        MyDialogs.__init__(self)
        self.retranslateUi()

    def retranslateUi(self):
        MyDialogs = self
        MyDialogs.setObjectName("choose_sref")
        self.resize(321, 100)
        _translate = QtCore.QCoreApplication.translate
        MyDialogs.setWindowTitle(_translate(
            "AddBot", "Add Sell bot for buy_ad_margin"))
        self.label_4 = QtWidgets.QLabel(MyDialogs)
        self.label_4.setGeometry(QtCore.QRect(10, 170, 141, 16))
        self.label_4.setObjectName("label_4")
        self.ad_id_2 = QtWidgets.QComboBox(MyDialogs)

        self.ad_id_2.setGeometry(QtCore.QRect(150, 30, 161, 32))
        self.ad_id_2.setObjectName("ad_id_2")
        self.pushButton = QtWidgets.QPushButton(MyDialogs)
        self.pushButton.setGeometry(QtCore.QRect(20, 30, 121, 31))
        self.pushButton.setObjectName("pushButton")

        self.pushButton.setText(_translate("AddBot", "Attach"))
        self.load_sell_bots()
        bot_id = self.ad_id_2.currentText().split()
        bot_id = bot_id[0]
        self.pushButton.clicked.connect(lambda: self.attach_sref(bot_id))
        self.exec_()

    def attach_sref(self, bot_id):
        self.dbExecutor.write_bot_single_set(
            self.bot_set['bot_id'], 'sell_ad_ref', bot_id)
        ShowMessage('Bot has been attached!')
        self.close()
