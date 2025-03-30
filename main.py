from datetime import datetime

from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox, QHeaderView

import sqlite3


class MyApp(QDialog):
    def __init__(self):
        super(MyApp, self).__init__()
        try:
            uic.loadUi('_internal/ui.ui', self)
            self.setWindowIcon(QIcon('_internal/无标题.ico'))
        except Exception as e:
            QMessageBox.critical(self,"错误",f"{e}", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            self.close()
        try:
            self.comboBox.addItems(['优','良','差'])
        except Exception as e:
            QMessageBox.critical(self,"错误",f"{e}", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            self.close()
        self.tableWidget.setWordWrap(True)
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS scores 
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              time TEXT, 
                              name TEXT, 
                              score TEXT)''')
        self.conn.commit()
        self.Reading()

    def Writing(self):
        score = self.comboBox.currentText()
        name = self.textEdit.toPlainText()
        if name == '':
            name = '没有反馈'
        time = datetime.now().isoformat()
        self.cursor.execute("INSERT INTO scores (time, name, score) VALUES (?,?,?)", (time, name, score))
        self.conn.commit()
        self.textEdit.clear()
        self.Reading()
        # self.close()

    def Reading(self):
        time = self.dateTimeEdit.dateTime().toPyDateTime().isoformat()
        self.cursor.execute("SELECT time, name, score FROM scores WHERE time >= ?", (time,))
        rows = self.cursor.fetchall()
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(3)
        for i, row in enumerate(rows):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(datetime.fromisoformat(row[0]).strftime(r'%Y-%m-%d %H:%M:%S')))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(row[1]))
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()



if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()
