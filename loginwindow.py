import sys
from PyQt5 import QtWidgets, QtCore

import ledgar_db
from ledgar_db import *
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

ledgar = Ledgar()

user = ""


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("windows/Login.ui", self)
        self.LoginButton.clicked.connect(self.loginfunction)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signupbutton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        uinfo = UserInformation(username, password)
        loginreturnval = ledgar.Login(uinfo)
        global user
        user = loginreturnval.split()[1]
        if loginreturnval.split()[0] == "Welcome":
            menu = Menu()
            widget.addWidget(menu)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            self.label_warning.setText(loginreturnval)
    def gotocreate(self):
        signup = SignUp()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex()+1)

class SignUp(QDialog):
    def __init__(self):
        super(SignUp, self).__init__()
        loadUi("windows/Signup.ui", self)
        self.SignUpButton.clicked.connect(self.Signupfunction)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password_confirm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.back_to_login_button.clicked.connect(self.backtologinfunction)

    def Signupfunction(self):
        if self.lineEdit_password.text() == self.lineEdit_password_confirm.text():
            username = self.lineEdit_username.text()
            password = self.lineEdit_password.text()
            uinfo = UserInformation(username, password)
            self.label_warning.setText(ledgar.SignIn(uinfo))
        else:
            self.label_warning.setText("Not comfirmed !")
    def backtologinfunction(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Menu(QDialog):
    def __init__(self):
        super(Menu, self).__init__()
        loadUi("windows/menu.ui", self)
        self.button_quit.clicked.connect(self.quitfunction)
        global user
        self.label_warning.setText("User: " + user)
        self.button_show_all_payments.clicked.connect(self.showallpaymentsfunction)
        self.button_add_payment.clicked.connect(self.addPaymentfunction)
        self.button_show_daily_payment.clicked.connect(self.showdailypayment)
    def quitfunction(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def showallpaymentsfunction(self):
        showall = ShowUserPayments()
        widget.addWidget(showall)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(1040)
        widget.setFixedHeight(850)
    def addPaymentfunction(self):
        add = addPayment()
        widget.addWidget(add)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setFixedWidth(540)
        widget.setFixedHeight(788)
    def showdailypayment(self):
        showdaily = totalSpends()
        widget.addWidget(showdaily)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setFixedWidth(480)
        widget.setFixedHeight(620)
class ShowUserPayments(QDialog):
    def __init__(self):
        super(ShowUserPayments, self).__init__()
        loadUi("windows/menu_show_all_payment.ui", self)
        self.button_back.clicked.connect(self.buttonbackfunction)
        global user
        payments = ledgar.ShowPayment(user)
        self.tableWidget.setRowCount(len(payments))
        row = 0
        #self.tableWidget.setTextAlignment(Qt::AlignHCenter)
        if payments[0][1] == "doesn't":
            self.label_warning.setText(payments)
        else:
            for i in payments:
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(i[2]))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(i[0]))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(i[1])))
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(i[3]))
                row = row+1
    def buttonbackfunction(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(480)
        widget.setFixedHeight(620)
    def buttonsavefunction(self):
        pass


class addPayment(QDialog):
    def __init__(self):
        super(addPayment, self).__init__()
        loadUi("windows/add_payment.ui", self)
        self.pushButton_add.clicked.connect(self.addfunction)
        self.pushButton_back.clicked.connect(ShowUserPayments.buttonbackfunction)
        self.foodbutton.clicked.connect(self.foodbuttonclicked)
        self.cleaningbutton.clicked.connect(self.cleaningbuttonclicked)
        self.billbutton.clicked.connect(self.billbuttonclicked)
        self.rentbutton.clicked.connect(self.rentbuttonclicked)
        self.selfcarebutton.clicked.connect(self.selfcarebuttonclicked)
        self.transportbutton.clicked.connect(self.transportbuttonclicked)
        self.snackbutton.clicked.connect(self.snackbuttonclicked)
        self.healthbutton.clicked.connect(self.healthbuttonclicked)
        self.othersbutton.clicked.connect(self.othersbuttonclicked)
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        global user
        self.label_warning.setText("User: " + user)
    def addfunction(self):
        global user
        new_type = self.label_choosed.text()
        new_price = self.lineEdit_price.text()
        new_product = self.lineEdit_comment.text()
        new_date = self.dateEdit.text()
        if len(str(new_price)) != 0:
            if new_type == "OTHERS" and len(str(new_product)) == 0:
                self.label_warning.setText("COMMENT NEEDED")
            else:
                print(new_type)
                print(new_product)
                print(new_price)
                print(new_date)
                ledgar.AddNewPayment(new_product, new_type, new_price, new_date, user)

        else:
            self.label_warning.setText("PRICE NEEDED")

    def foodbuttonclicked(self):
        self.label_choosed.setText("FOOD")
    def cleaningbuttonclicked(self):
        self.label_choosed.setText("CLEANING")
    def billbuttonclicked(self):
        self.label_choosed.setText("BILL")
    def rentbuttonclicked(self):
        self.label_choosed.setText("RENT")
    def selfcarebuttonclicked(self):
        self.label_choosed.setText("SELF CARE")
    def transportbuttonclicked(self):
        self.label_choosed.setText("TRANSPORT")
    def snackbuttonclicked(self):
        self.label_choosed.setText("SNACK")
    def healthbuttonclicked(self):
        self.label_choosed.setText("HEALTH")
    def othersbuttonclicked(self):
        self.label_choosed.setText("OTHERS")

class totalSpends(QDialog):
    def __init__(self):
        super(totalSpends, self).__init__()
        loadUi("windows/totalspends.ui", self)
        self.pushButton_back.clicked.connect(ShowUserPayments.buttonbackfunction)
        self.pushButton_show.clicked.connect(self.buttonshowfunction)
        self.dateEdit.setDate(QtCore.QDate.currentDate())
    def buttonshowfunction(self):
        new_date = self.dateEdit.text()
        daily_spend = ledgar.DailySpend(new_date, user)
        if daily_spend == 0:
            self.label_warning.setText("Has no expenditure")
        else:
            self.label_daily_2.setText(daily_spend+" TL")



app = QApplication(sys.argv)

widget = QtWidgets.QStackedWidget()
mainwindow = Login()

widget.addWidget(mainwindow)

widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()

app.exec_()
