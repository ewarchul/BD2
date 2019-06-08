from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtWidgets import *#QTableView, QApplication
#from PyQt5 import QtCore #, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sqlite3
import sys

class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pomoc")
        self.width = 300
        self.height = 150
        self.setFixedSize(self.width, self.height)
        self.layout = QVBoxLayout()
        self.label = QLabel("Kontakt: pomocny@pomocnik.ru")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
class ViewWindow(QWidget):
    @pyqtSlot()
    def make_query(self):
        cur_txt = self.cur_txt 
        db = QSqlDatabase.addDatabase('QSQLITE') 
        print(cur_txt)
        db.setDatabaseName('mydbx')
        db.open()
        query = QSqlQuery(db)
        if cur_txt == 'pracownik':
            query.prepare('select * from pracownik where poziom_dostepu={};'.format(self.filter.text())) 
        elif cur_txt == 'podmiot_zewnetrzny':
            query.prepare('select * from {} where {}')
        elif cur_txt == 'osoba_uprawniona':
            query.prepare('select * from {} where {}')
        elif cur_txt == 'umowa':
            query.prepare('select * from {} where {}')
        elif cur_txt == 'dzial':
            query.prepare('select * from dzial;') 
        query.exec()
        model = QSqlQueryModel()
        model.setQuery(query)
        tableview = QTableView(self)
        tableview.setModel(model)
        tableview.resizeColumnsToContents()
        tableview.move(300, 100)
        tableview.show()
    def build_ui(self, text):
        cur_txt = text
        self.filter = QLineEdit(self)
        model = QSqlQueryModel()
        if cur_txt == 'pracownik':
            self.filter.setPlaceholderText('Poziom dostępu')
        elif cur_txt == 'podmiot_zewnetrzny':
            self.filter.setPlaceholderText('REGON')
        elif cur_txt == 'osoba_uprawniona':
            self.filter.setPlaceholderText('Rodzaj uprawnienia')
        elif cur_txt == 'umowa':
            self.filter.setPlaceholderText('Wymagany poziom dostępu')
        self.filter.move(80, 150)
        self.filter.show()
        self.cur_txt = cur_txt
        query_btn = QPushButton('Wykonaj zapytanie', self)
        query_btn.setStyleSheet('QPushButton {background-color: red}')
        query_btn.move(100, 350)
        query_btn.clicked.connect(self.make_query)
        query_btn.show()
    def __init__(self):
        super().__init__()
        self.title = 'Przegląd danych'
        self.top = 100
        self.left = 100
        self.width = 1000
        self.height = 1000
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)
        combo = QComboBox(self)
        combo.addItem("dzial")
        combo.addItem("pracownik")
        combo.addItem("podmiot_zewnetrzny")
        combo.addItem("osoba_uprawniona")
        combo.addItem("umowa")
        combo.move(80, 100)
        combo.activated[str].connect(self.build_ui)
        self.current_text = str(combo.currentText())
class EditwWindow(QWidget):
        pass
class DeleteWindow(QWidget):
        pass
class ReportWindow(QWidget):
        pass
class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Menu użytkownika'
        self.top = 100
        self.left = 100
        self.width = 650
        self.height = 650
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)
        self.logo = QLabel(self)
        pixmap = QPixmap('logo.jpg')
        self.logo.setPixmap(pixmap)
        self.logo.resize(650, 650)

        view_btn = QPushButton('Przegląd', self)
        view_btn.setStyleSheet('QPushButton {background-color: orange}')
        view_btn.move(80, 300)
        view_btn.clicked.connect(self.view_click)

        edit_btn = QPushButton('Edycja', self)
        edit_btn.setStyleSheet('QPushButton {background-color: green}')
        edit_btn.move(80, 350)

        delete_btn = QPushButton('Usunięcie', self)
        delete_btn.setStyleSheet('QPushButton {background-color: blue}')
        delete_btn.move(80, 400)

        report_btn = QPushButton('Raport', self)
        report_btn.setStyleSheet('QPushButton {background-color: purple}')
        report_btn.move(80, 450)
    @pyqtSlot()
    def view_click(self):
        self.viewWin = ViewWindow()
        self.viewWin.show()
class App(QWidget):
    @pyqtSlot()
    def exit_click(self):
        exit()
    @pyqtSlot()
    def help_click(self):
        self.w = HelpWindow()
        self.w.show()
    @pyqtSlot()
    def log_click(self):
        login = self.user.text()
        password = self.pw.text()
        acc_lvl = 5
        if(not len(password)):
            QMessageBox.about(self, 'Komunikat', 'Niewłaściwa nazwa użytkownika lub hasło!')
        else:
            try:
                connection = sqlite3.connect('sports.db') 
                QMessageBox.about(self, 'Komunikat', 'Połączono z bazą danych.\nTwoje dane są następujące:\npoziom dostępu: {}\nnazwa konta: {}'.format(acc_lvl, login))
                self.menu = MenuWindow()
                self.menu.show()
                self.hide()
            except:
                QMessageBox.about(self, 'Komunikat', 'Nie udało się połączyć z bazą danych.')

    def __init__(self):
        super().__init__()
        self.title = 'Logowanie do systemu'
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 500
        self.setFixedSize(self.width, self.height)
        self.Log()
    def Log(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)
        self.logo = QLabel(self)
        pixmap = QPixmap('logo.jpg')
        self.logo.setPixmap(pixmap)
        self.logo.resize(500, 500)
        self.user = QLineEdit(self)
        self.user.setPlaceholderText('Nazwa użytkownika')
        self.user.move(100, 150)
        self.pw = QLineEdit(self)
        self.pw.setPlaceholderText('Hasło')
        self.pw.setEchoMode(QLineEdit.Password)
        self.pw.move(100, 200)
        log_btn = QPushButton('Zaloguj', self)
        log_btn.setStyleSheet('QPushButton {background-color: red}')
        log_btn.move(100, 300)
        log_btn.clicked.connect(self.log_click)
        exit_btn = QPushButton('Wyłącz aplikację', self)
        exit_btn.setStyleSheet('QPushButton {background-color: red}')
        exit_btn.move(100, 350)
        exit_btn.clicked.connect(self.exit_click)
        help_btn = QPushButton('Pomoc', self)
        help_btn.setStyleSheet('QPushButton {background-color: red}')
        help_btn.move(100, 400)
        help_btn.clicked.connect(self.help_click)
        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

    


