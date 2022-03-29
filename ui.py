# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'big.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(361, 560)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(361, 560))
        MainWindow.setMaximumSize(QtCore.QSize(361, 16777215))
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setTabPosition(QtWidgets.QTabWidget.North)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        MainWindow.setUsesScrollButtons(True)
        MainWindow.setDocumentMode(False)
        MainWindow.setMovable(False)
        MainWindow.setTabBarAutoHide(False)
        self.controlpanel = QtWidgets.QWidget()
        self.controlpanel.setObjectName("controlpanel")
        self.onoff = QtWidgets.QCheckBox(self.controlpanel)
        self.onoff.setGeometry(QtCore.QRect(20, 0, 71, 20))
        self.onoff.setObjectName("onoff")
        self.listWidget = QtWidgets.QListWidget(self.controlpanel)
        self.listWidget.setGeometry(QtCore.QRect(20, 50, 311, 241))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listWidget.setFont(font)
        self.listWidget.setObjectName("listWidget")
        self.last_time_upd = QtWidgets.QLabel(self.controlpanel)
        self.last_time_upd.setGeometry(QtCore.QRect(260, 0, 58, 16))
        self.last_time_upd.setObjectName("last_time_upd")
        self.curr_price = QtWidgets.QLabel(self.controlpanel)
        self.curr_price.setGeometry(QtCore.QRect(130, 422, 101, 16))
        self.curr_price.setObjectName("curr_price")
        self.label_4 = QtWidgets.QLabel(self.controlpanel)
        self.label_4.setGeometry(QtCore.QRect(20, 420, 80, 16))
        self.label_4.setObjectName("label_4")
        self.min_price = QtWidgets.QLineEdit(self.controlpanel)
        self.min_price.setGeometry(QtCore.QRect(130, 400, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.min_price.setFont(font)
        self.min_price.setFrame(False)
        self.min_price.setObjectName("min_price")
        self.label_3 = QtWidgets.QLabel(self.controlpanel)
        self.label_3.setGeometry(QtCore.QRect(20, 380, 80, 16))
        self.label_3.setObjectName("label_3")
        self.min_amount = QtWidgets.QLabel(self.controlpanel)
        self.min_amount.setGeometry(QtCore.QRect(130, 450, 111, 16))
        self.min_amount.setObjectName("min_amount")
        self.autoreply_onoff = QtWidgets.QCheckBox(self.controlpanel)
        self.autoreply_onoff.setGeometry(QtCore.QRect(250, 440, 83, 20))
        self.autoreply_onoff.setObjectName("autoreply_onoff")
        self.label_6 = QtWidgets.QLabel(self.controlpanel)
        self.label_6.setGeometry(QtCore.QRect(20, 400, 79, 16))
        self.label_6.setObjectName("label_6")
        self.label_5 = QtWidgets.QLabel(self.controlpanel)
        self.label_5.setGeometry(QtCore.QRect(20, 350, 91, 16))
        self.label_5.setObjectName("label_5")
        self.curr_koeff = QtWidgets.QLabel(self.controlpanel)
        self.curr_koeff.setGeometry(QtCore.QRect(130, 380, 101, 16))
        self.curr_koeff.setObjectName("curr_koeff")
        self.label_2 = QtWidgets.QLabel(self.controlpanel)
        self.label_2.setGeometry(QtCore.QRect(20, 448, 71, 16))
        self.label_2.setObjectName("label_2")
        self.min_koeff = QtWidgets.QDoubleSpinBox(self.controlpanel)
        self.min_koeff.setGeometry(QtCore.QRect(130, 350, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.min_koeff.setFont(font)
        self.min_koeff.setFrame(False)
        self.min_koeff.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_koeff.setSingleStep(0.01)
        self.min_koeff.setObjectName("min_koeff")
        self.min_price_onoff = QtWidgets.QCheckBox(self.controlpanel)
        self.min_price_onoff.setGeometry(QtCore.QRect(110, 400, 21, 20))
        self.min_price_onoff.setText("")
        self.min_price_onoff.setObjectName("min_price_onoff")
        self.bot_switch = QtWidgets.QComboBox(self.controlpanel)
        self.bot_switch.setGeometry(QtCore.QRect(10, 20, 331, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.bot_switch.setFont(font)
        self.bot_switch.setObjectName("bot_switch")
        self.autoreply_msg = QtWidgets.QTextEdit(self.controlpanel)
        self.autoreply_msg.setGeometry(QtCore.QRect(20, 470, 321, 51))
        self.autoreply_msg.setObjectName("autoreply_msg")
        self.botstate = QtWidgets.QLabel(self.controlpanel)
        self.botstate.setGeometry(QtCore.QRect(175, 0, 71, 16))
        self.botstate.setObjectName("botstate")
        self.total_fees = QtWidgets.QDoubleSpinBox(self.controlpanel)
        self.total_fees.setGeometry(QtCore.QRect(130, 320, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.total_fees.setFont(font)
        self.total_fees.setFrame(False)
        self.total_fees.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.total_fees.setSingleStep(0.01)
        self.total_fees.setObjectName("total_fees")
        self.label_9 = QtWidgets.QLabel(self.controlpanel)
        self.label_9.setGeometry(QtCore.QRect(20, 320, 111, 16))
        self.label_9.setObjectName("label_9")
        self.curr_margin = QtWidgets.QLabel(self.controlpanel)
        self.curr_margin.setGeometry(QtCore.QRect(130, 400, 61, 16))
        self.curr_margin.setObjectName("curr_margin")
        self.label_10 = QtWidgets.QLabel(self.controlpanel)
        self.label_10.setGeometry(QtCore.QRect(20, 400, 111, 16))
        self.label_10.setObjectName("label_10")
        self.sell_ad_ref = QtWidgets.QPushButton(self.controlpanel)
        self.sell_ad_ref.setGeometry(QtCore.QRect(30, 290, 291, 32))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sell_ad_ref.setFont(font)
        self.sell_ad_ref.setObjectName("sell_ad_ref")
        self.curr_diff = QtWidgets.QLabel(self.controlpanel)
        self.curr_diff.setGeometry(QtCore.QRect(220, 320, 111, 16))
        self.curr_diff.setObjectName("curr_diff")
        self.listWidget.raise_()
        self.last_time_upd.raise_()
        self.curr_price.raise_()
        self.label_4.raise_()
        self.min_price.raise_()
        self.label_3.raise_()
        self.min_amount.raise_()
        self.autoreply_onoff.raise_()
        self.label_6.raise_()
        self.label_5.raise_()
        self.curr_koeff.raise_()
        self.label_2.raise_()
        self.min_koeff.raise_()
        self.min_price_onoff.raise_()
        self.bot_switch.raise_()
        self.autoreply_msg.raise_()
        self.botstate.raise_()
        self.total_fees.raise_()
        self.label_9.raise_()
        self.curr_margin.raise_()
        self.label_10.raise_()
        self.sell_ad_ref.raise_()
        self.onoff.raise_()
        self.curr_diff.raise_()
        MainWindow.addTab(self.controlpanel, "")
        self.settings = QtWidgets.QWidget()
        self.settings.setObjectName("settings")
        self.add_bot = QtWidgets.QPushButton(self.settings)
        self.add_bot.setGeometry(QtCore.QRect(20, 220, 101, 32))
        self.add_bot.setObjectName("add_bot")
        self.add_profile = QtWidgets.QPushButton(self.settings)
        self.add_profile.setGeometry(QtCore.QRect(20, 30, 101, 32))
        self.add_profile.setObjectName("add_profile")
        self.profiles = QtWidgets.QListWidget(self.settings)
        self.profiles.setGeometry(QtCore.QRect(20, 60, 311, 141))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.profiles.setFont(font)
        self.profiles.setObjectName("profiles")
        self.bot_sets = QtWidgets.QListWidget(self.settings)
        self.bot_sets.setGeometry(QtCore.QRect(20, 250, 311, 161))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.bot_sets.setFont(font)
        self.bot_sets.setObjectName("bot_sets")
        self.delete_profile = QtWidgets.QPushButton(self.settings)
        self.delete_profile.setGeometry(QtCore.QRect(270, 30, 61, 32))
        self.delete_profile.setObjectName("delete_profile")
        self.delete_bot_set = QtWidgets.QPushButton(self.settings)
        self.delete_bot_set.setGeometry(QtCore.QRect(270, 220, 61, 32))
        self.delete_bot_set.setObjectName("delete_bot_set")
        self.domain = QtWidgets.QComboBox(self.settings)
        self.domain.setGeometry(QtCore.QRect(70, 420, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.domain.setFont(font)
        self.domain.setObjectName("domain")
        self.domain.addItem("")
        self.domain.addItem("")
        self.domain.addItem("")
        self.time_zone = QtWidgets.QComboBox(self.settings)
        self.time_zone.setGeometry(QtCore.QRect(240, 420, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.time_zone.setFont(font)
        self.time_zone.setObjectName("time_zone")
        self.time_zone.addItem("")
        self.time_zone.addItem("")
        self.label_7 = QtWidgets.QLabel(self.settings)
        self.label_7.setGeometry(QtCore.QRect(20, 430, 61, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.settings)
        self.label_8.setGeometry(QtCore.QRect(170, 430, 71, 16))
        self.label_8.setObjectName("label_8")
        self.refreshBtn = QtWidgets.QPushButton(self.settings)
        self.refreshBtn.setGeometry(QtCore.QRect(120, 30, 71, 32))
        self.refreshBtn.setObjectName("refreshBtn")
        MainWindow.addTab(self.settings, "")

        self.retranslateUi(MainWindow)
        MainWindow.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.onoff, self.listWidget)
        MainWindow.setTabOrder(self.listWidget, self.min_koeff)
        MainWindow.setTabOrder(self.min_koeff, self.bot_switch)
        MainWindow.setTabOrder(self.bot_switch, self.add_profile)
        MainWindow.setTabOrder(self.add_profile, self.min_price)
        MainWindow.setTabOrder(self.min_price, self.autoreply_onoff)
        MainWindow.setTabOrder(self.autoreply_onoff, self.add_bot)
        MainWindow.setTabOrder(self.add_bot, self.min_price_onoff)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "xactivity.online Localbitcoins Bot"))
        self.onoff.setText(_translate("MainWindow", "On/off"))
        self.last_time_upd.setText(_translate("MainWindow", "hh:mm:ss"))
        self.curr_price.setText(_translate("MainWindow", "1500000"))
        self.label_4.setText(_translate("MainWindow", "Current price"))
        self.min_price.setText(_translate("MainWindow", "1000000"))
        self.label_3.setText(_translate("MainWindow", "Current koeff"))
        self.min_amount.setText(_translate("MainWindow", "3000"))
        self.autoreply_onoff.setText(_translate("MainWindow", "Autoreply"))
        self.label_6.setText(_translate("MainWindow", "Set min price"))
        self.label_5.setText(_translate("MainWindow", "Set min koeff"))
        self.curr_koeff.setText(_translate("MainWindow", "1.02"))
        self.label_2.setText(_translate("MainWindow", "Min amount"))
        self.autoreply_msg.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Welcome!</p></body></html>"))
        self.botstate.setText(_translate("MainWindow", "connected"))
        self.label_9.setText(_translate("MainWindow", "Shipment cost %"))
        self.curr_margin.setText(_translate("MainWindow", "1.02"))
        self.label_10.setText(_translate("MainWindow", "Current margin %"))
        self.sell_ad_ref.setText(_translate("MainWindow", "PushButton"))
        self.curr_diff.setText(_translate("MainWindow", "CURR"))
        MainWindow.setTabText(MainWindow.indexOf(self.controlpanel), _translate("MainWindow", "Bot"))
        self.add_bot.setText(_translate("MainWindow", "Add bot"))
        self.add_profile.setText(_translate("MainWindow", "Add profile"))
        self.delete_profile.setText(_translate("MainWindow", "delete"))
        self.delete_bot_set.setText(_translate("MainWindow", "delete"))
        self.domain.setItemText(0, _translate("MainWindow", "com"))
        self.domain.setItemText(1, _translate("MainWindow", "fi"))
        self.domain.setItemText(2, _translate("MainWindow", "net"))
        self.time_zone.setItemText(0, _translate("MainWindow", "+1"))
        self.time_zone.setItemText(1, _translate("MainWindow", "+2"))
        self.label_7.setText(_translate("MainWindow", "Domain"))
        self.label_8.setText(_translate("MainWindow", "Time zone"))
        self.refreshBtn.setText(_translate("MainWindow", "refresh"))
        MainWindow.setTabText(MainWindow.indexOf(self.settings), _translate("MainWindow", "Settings"))
