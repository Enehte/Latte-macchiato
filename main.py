import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton
from PyQt5.QtWidgets import QDialog
# from PyQt5 import uic
import sqlite3
from PyQt5.QtCore import Qt
from addui import Ui_Dialog
from mainui import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('main.ui', self)
        self.setupUi(self)
        self.params = {}
        self.headers = ['ID', 'Название сорта', 'Степень обжарки', 'Цена', 
                        'Описание вкуса', 'Объем упаковки', 'Молотый(1)/в зернах(2)']
        self.con = sqlite3.connect('data/coffee.sqlite')
        cur = self.con.cursor()
        self.result = cur.execute("SELECT * FROM main").fetchall()
        self.table(self.result)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.change)
    
    def add(self):
        dialog = Dialog()
        dialog.exec_()
        # print(dialog.add())
        dt = dialog.add()
        
        cur = self.con.cursor()
        req = f"""INSERT OR IGNORE INTO main (id, title, roastid, price, description, volume, form) 
                  VALUES(1, {dt[0]}, {dt[1]}, {dt[2]}, {dt[3]}, {dt[4]}, {dt[5]})"""
        print()
        self.result = cur.execute(req)
        self.table(self.result)

    def change(self):
        self.lineEdit.text()
        a = self.tableWidget.currentItem().text()
        cur = self.con.cursor()
        if self.tableWidget.currentColumn() == 1:
            req = f"""UPDATE main SET {self.lineEdit.text()} WHERE title={a}"""
            self.result = cur.execute(req)
            self.table(self.result)
    
    def table(self, result):
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(self.headers)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

class Dialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        # uic.loadUi('addui.ui', self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add)
    
    def add(self):
        data = [self.lineEdit.text(), int(self.lineEdit_2.text()), int(self.lineEdit_3.text()),
                self.lineEdit_4.text(), int(self.lineEdit_5.text()), int(self.lineEdit_6.text())]
        # print(data)
        self.close()
        return data


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())