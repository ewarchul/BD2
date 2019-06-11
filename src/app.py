from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtWidgets import *#QTableView, QApplication
#from PyQt5 import QtCore #, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sqlite3
import sys
import re
from report_app import *

login = ""

def clearLayout(layout):
    for i in range(layout.count()): layout.itemAt(i).widget().close()
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
            query_residual = 'poziom_dostepu = \'{}\' and imie = \'{}\' and nazwisko = \'{}\' and id_pracownika = \'{}\' and stanowisko = \'{}\' '.format(self.filter_acclvl.text(), self.filter_worker_name.text(), self.filter_worker_surname.text(), self.filter_worker_id.text(), self.filter_worker_job.text())
            key_val = re.sub('X', ' and ','X'.join(re.findall('\w+ = \'\S+\'' ,query_residual)))
            if(len(key_val)):
                query.prepare('select * from pracownik where ' + key_val)
            else:
                query.prepare('select * from pracownik')
        elif cur_txt == 'osoba_uprawniona':
            query_residual = 'wymagany_poziom_dostepu = \'{}\' and numer_osoby = \'{}\' and imie = \'{}\' and nazwisko = \'{}\' and rodzaj_uprawnienia = \'{}\' and data_dodania = \'{}\' '.format(self.filter_wymagany_acclvl.text(), self.filter_id.text(), self.filter_imie.text(), 
                    self.filter_nazwisko.text(), self.filter_rodzaj_uprawnienia.text(), self.filter_data_dodania.text())
            key_val = re.sub('X', ' and ','X'.join(re.findall('\w+ = \'\S+\'' ,query_residual)))
            if(len(key_val)):
                query.prepare('select * from osoba_uprawniona where ' + key_val)
            else:
                query.prepare('select * from osoba_uprawniona')
        elif cur_txt == 'osoba_fizyczna':
            query_residual = 'id_podmiotu = \'{}\' and imie = \'{}\' and nazwisko = \'{}\' and pesel = \'{}\' '.format(self.filter_id.text(), self.filter_imie.text(), self.filter_nazwisko.text(), self.filter_pesel.text())
            key_val = re.sub('X', ' and ','X'.join(re.findall('\w+ = \'\S+\'' ,query_residual)))
            if(len(key_val)):
                query.prepare('select * from osoba_fizyczna where ' + key_val)
            else:
                query.prepare('select * from osoba_fizyczna')
        elif cur_txt == 'organizacja':
            query_residual = 'id_podmiotu = \'{}\' and nip = \'{}\' and nazwa = \'{}\' and regon = \'{}\' '.format(self.filter_id.text(), self.filter_nip.text(), self.filter_nazwa.text(), self.filter_regon.text())
            key_val = re.sub('X', ' and ','X'.join(re.findall('\w+ = \'\S+\'', query_residual)))
            if(len(key_val)):
                query.prepare('select * from organizacja where ' + key_val)
            else:
                query.prepare('select * from organizacja')
        elif cur_txt == 'umowa':
            query_residual = 'id_umowy = \'{}\' and nazwa_umowy = \'{}\' and podmiot_zewnetrzny_id_podmiotu = \'{}\' and rodzaj_umowy = \'{}\' and data_utworzenia = \'{}\' and wymagany_poziom_dostepu = \'{}\''.format(self.filter_idu.text(), self.filter_nu.text(), self.filter_pz.text(), self.filter_rz.text(), self.filter_du.text(), self.filter_wpd.text())
            key_val = re.sub('X', ' and ','X'.join(re.findall('\w+ = \'\S+\'', query_residual)))
            if(len(key_val)):
                query.prepare('select * from umowa where ' + key_val)
            else:
                query.prepare('select * from umowa')
        elif cur_txt == 'dzial':
            query.prepare('select * from dzial;')
        query.exec()
        model = QSqlQueryModel()
        model.setQuery(query)
        tableview = QTableView(self)
        tableview.setModel(model)
        tableview.resizeColumnsToContents()
        tableview.move(300, 100)
        tableview.resize(600, 200)
        tableview.show()
    def build_ui(self, text):
        cur_txt = text
        model = QSqlQueryModel()
        clearLayout(self.hbox)
        if cur_txt == 'pracownik':
            self.filter_check = QCheckBox("Aktwny?",self)
            self.filter_check.move(250, 350)
            self.filter_check.show()
            self.filter_acclvl = QLineEdit(self)
            self.filter_acclvl.setPlaceholderText('Poziom dostępu')
            self.filter_acclvl.move(80, 150)
            self.filter_worker_name = QLineEdit(self)
            self.filter_worker_name.setPlaceholderText('Imię')
            self.filter_worker_name.move(80, 200)
            self.filter_worker_id = QLineEdit(self)
            self.filter_worker_id.setPlaceholderText('Numer ID')
            self.filter_worker_id.move(80, 250)
            self.filter_worker_surname = QLineEdit(self)
            self.filter_worker_surname.setPlaceholderText('Nazwisko')
            self.filter_worker_surname.move(80, 300)
            self.filter_worker_job = QLineEdit(self)
            self.filter_worker_job.setPlaceholderText('Stanowisko')
            self.filter_worker_job.move(80, 350)
            self.hbox.addWidget(self.filter_check)
            self.hbox.addWidget(self.filter_worker_job)
            self.hbox.addWidget(self.filter_worker_id)
            self.hbox.addWidget(self.filter_acclvl)
            self.hbox.addWidget(self.filter_worker_name)
            self.hbox.addWidget(self.filter_worker_surname)
        elif cur_txt == 'osoba_uprawniona':
            self.filter_id = QLineEdit(self)
            self.filter_imie = QLineEdit(self)
            self.filter_nazwisko = QLineEdit(self)
            self.filter_id_umowy = QLineEdit(self)
            self.filter_rodzaj_uprawnienia = QLineEdit(self)
            self.filter_data_dodania = QLineEdit(self)
            self.filter_wymagany_acclvl = QLineEdit(self)
            self.filter_id.move(80, 150)
            self.filter_imie.move(80, 200)
            self.filter_nazwisko.move(80, 250)
            self.filter_id_umowy.move(80, 300)
            self.filter_rodzaj_uprawnienia.move(80, 350)
            self.filter_data_dodania.move(80, 400)
            self.filter_wymagany_acclvl.move(80, 450)
            self.filter_id.setPlaceholderText('Numer ID')
            self.filter_imie.setPlaceholderText('Imię')
            self.filter_nazwisko.setPlaceholderText('nazwisko')
            self.filter_id_umowy.setPlaceholderText('ID umowy')
            self.filter_rodzaj_uprawnienia.setPlaceholderText('Rodzaj uprawnienia')
            self.filter_data_dodania.setPlaceholderText('Data dodania')
            self.filter_wymagany_acclvl.setPlaceholderText('Wymagany poziom dostępu')
            self.hbox.addWidget(self.filter_wymagany_acclvl)
            self.hbox.addWidget(self.filter_id)
            self.hbox.addWidget(self.filter_imie)
            self.hbox.addWidget(self.filter_data_dodania)
            self.hbox.addWidget(self.filter_nazwisko)
            self.hbox.addWidget(self.filter_rodzaj_uprawnienia)
        elif cur_txt == 'osoba_fizyczna':
            self.filter_id = QLineEdit(self)
            self.filter_imie = QLineEdit(self)
            self.filter_nazwisko = QLineEdit(self)
            self.filter_pesel = QLineEdit(self)
            self.filter_id.move(80, 150)
            self.filter_imie.move(80, 200)
            self.filter_nazwisko.move(80, 250)
            self.filter_pesel.move(80, 300)
            self.filter_id.setPlaceholderText('Numer ID')
            self.filter_imie.setPlaceholderText('Imię')
            self.filter_nazwisko.setPlaceholderText('Nazwisko')
            self.filter_pesel.setPlaceholderText('PESEL')
            self.hbox.addWidget(self.filter_id)
            self.hbox.addWidget(self.filter_imie)
            self.hbox.addWidget(self.filter_nazwisko)
            self.hbox.addWidget(self.filter_pesel)
        elif cur_txt == 'organizacja':
            self.filter_id = QLineEdit(self)
            self.filter_nip = QLineEdit(self)
            self.filter_nazwa = QLineEdit(self)
            self.filter_regon = QLineEdit(self)
            self.filter_id.move(80, 150)
            self.filter_nip.move(80, 200)
            self.filter_nazwa.move(80, 250)
            self.filter_regon.move(80, 300)
            self.filter_id.setPlaceholderText('Numer ID')
            self.filter_nip.setPlaceholderText('NIP')
            self.filter_nazwa.setPlaceholderText('Nazwa')
            self.filter_regon.setPlaceholderText('REGON')
            self.hbox.addWidget(self.filter_id)
            self.hbox.addWidget(self.filter_nip)
            self.hbox.addWidget(self.filter_nazwa)
            self.hbox.addWidget(self.filter_regon)
        elif cur_txt == 'umowa':
            self.filter_idu = QLineEdit(self)
            self.filter_nu = QLineEdit(self)
            self.filter_pz = QLineEdit(self)
            self.filter_rz = QLineEdit(self)
            self.filter_du = QLineEdit(self)
            self.filter_wpd = QLineEdit(self)
            self.filter_idu.move(80, 150) 
            self.filter_nu.move(80, 200) 
            self.filter_pz.move(80, 250) 
            self.filter_rz.move(80, 300) 
            self.filter_du.move(80, 350) 
            self.filter_wpd.move(80, 400) 
            self.filter_idu.setPlaceholderText('ID umowy')
            self.filter_nu.setPlaceholderText('Nazwa umowy') 
            self.filter_pz.setPlaceholderText('ID pod. zew.')
            self.filter_rz.setPlaceholderText('Rodzaj umowy') 
            self.filter_du.setPlaceholderText('Data utworzenia') 
            self.filter_wpd.setPlaceholderText('Wymagany poz. dost.') 
            self.hbox.addWidget(self.filter_idu)
            self.hbox.addWidget(self.filter_nu)
            self.hbox.addWidget(self.filter_pz)
            self.hbox.addWidget(self.filter_rz)
            self.hbox.addWidget(self.filter_du)
            self.hbox.addWidget(self.filter_wpd)
        self.setLayout(self.hbox)
        self.cur_txt = cur_txt
        query_btn = QPushButton('Wykonaj zapytanie', self)
        query_btn.setStyleSheet('QPushButton {background-color: red}')
        query_btn.move(100, 400)
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
        self.hbox = QHBoxLayout()
        combo = QComboBox(self)
        combo.addItem("dzial")
        combo.addItem("pracownik")
        combo.addItem("organizacja")
        combo.addItem("osoba_fizyczna")
        combo.addItem("osoba_uprawniona")
        combo.addItem("umowa")
        combo.move(80, 100)
        combo.activated[str].connect(self.build_ui)
        self.current_text = str(combo.currentText())
class AddWindow(QWidget):
    @pyqtSlot()
    def make_query(self):
        cur_txt = self.cur_txt
        db = QSqlDatabase.addDatabase('QSQLITE')
        print(cur_txt)
        db.setDatabaseName('mydbx')
        db.open()
        query = QSqlQuery(db)
        if cur_txt == 'pracownik':
            query_residual = ' id_dzialu = \'{}\' and poziom_dostepu = \'{}\' and imie = \'{}\' and nazwisko = \'{}\' and id_pracownika = \'{}\' and stanowisko = \'{}\' '.format(self.filter_worker_idd.text(), self.filter_acclvl.text(), self.filter_worker_name.text(), self.filter_worker_surname.text(), self.filter_worker_id.text(), self.filter_worker_job.text())
            keys = re.sub(',and', '',','.join(re.findall('\w+ ', query_residual)))
            values = ','.join(re.findall('\'.*?\'', query_residual))
            query.prepare('insert into pracownik ('+ keys + ') values (' + values + ')')
        elif cur_txt == 'osoba_uprawniona':
            query_residual = 'wymagany_poziom_dostepu = \'{}\' and numer_osoby = \'{}\' and imie = \'{}\' and nazwisko = \'{}\' and rodzaj_uprawnienia = \'{}\' and data_dodania = \'{}\' '.format(self.filter_wymagany_acclvl.text(), self.filter_id.text(), self.filter_imie.text(), 
                    self.filter_nazwisko.text(), self.filter_rodzaj_uprawnienia.text(), self.filter_data_dodania.text())
            keys = re.sub(',and', '',','.join(re.findall('\w+ ', query_residual)))
            values = ','.join(re.findall('\'.*?\'', query_residual))
            query.prepare('insert into osoba_uprawniona ('+ keys + ') values (' + values + ')')
        elif cur_txt == 'osoba_fizyczna':
            query_residual = 'id_podmiotu = \'{}\' and imie = \'{}\' and nazwisko = \'{}\' and pesel = \'{}\' '.format(self.filter_id.text(), self.filter_imie.text(), self.filter_nazwisko.text(), self.filter_pesel.text())
            keys = re.sub(',and', '',','.join(re.findall('\w+ ', query_residual)))
            values = ','.join(re.findall('\'.*?\'', query_residual))
            query.prepare('insert into osoba_fizyczna ('+ keys + ') values (' + values + ')')
        elif cur_txt == 'organizacja':
            query_residual = 'id_podmiotu = \'{}\' and nip = \'{}\' and nazwa = \'{}\' and regon = \'{}\' '.format(self.filter_id.text(), self.filter_nip.text(), self.filter_nazwa.text(), self.filter_regon.text())
            keys = re.sub(',and', '',','.join(re.findall('\w+ ', query_residual)))
            values = ','.join(re.findall('\'.*?\'', query_residual))
            query.prepare('insert into organizacja ('+ keys + ') values (' + values + ')')
        elif cur_txt == 'umowa':
            keys = re.sub(',and', '',','.join(re.findall('\w+ ', query_residual)))
            values = ','.join(re.findall('\'.*?\'', query_residual))
            query.prepare('insert into organizacja ('+ keys + ') values (' + values + ')')

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
        tableview.resize(600, 200)
        tableview.show()
    def build_ui(self, text):
        cur_txt = text
        model = QSqlQueryModel()
        clearLayout(self.hbox)
        if cur_txt == 'pracownik':
            self.filter_check = QCheckBox("Aktwny?",self)
            self.filter_check.move(250, 350)
            self.filter_check.show()
            self.filter_acclvl = QLineEdit(self)
            self.filter_acclvl.setPlaceholderText('Poziom dostępu')
            self.filter_acclvl.move(80, 150)
            self.filter_worker_name = QLineEdit(self)
            self.filter_worker_name.setPlaceholderText('Imię')
            self.filter_worker_name.move(80, 200)
            self.filter_worker_id = QLineEdit(self)
            self.filter_worker_id.setPlaceholderText('Numer ID')
            self.filter_worker_id.move(80, 250)
            self.filter_worker_surname = QLineEdit(self)
            self.filter_worker_surname.setPlaceholderText('Nazwisko')
            self.filter_worker_surname.move(80, 300)
            self.filter_worker_job = QLineEdit(self)
            self.filter_worker_job.setPlaceholderText('Stanowisko')
            self.filter_worker_job.move(80, 350)
            self.filter_worker_idd = QLineEdit(self)
            self.filter_worker_idd.setPlaceholderText('ID działu')
            self.filter_worker_idd.move(80, 400) 
            self.hbox.addWidget(self.filter_check)
            self.hbox.addWidget(self.filter_worker_job)
            self.hbox.addWidget(self.filter_worker_id)
            self.hbox.addWidget(self.filter_acclvl)
            self.hbox.addWidget(self.filter_worker_idd)
            self.hbox.addWidget(self.filter_worker_name)
            self.hbox.addWidget(self.filter_worker_surname)
        elif cur_txt == 'osoba_uprawniona':
            self.filter_id = QLineEdit(self)
            self.filter_imie = QLineEdit(self)
            self.filter_nazwisko = QLineEdit(self)
            self.filter_id_umowy = QLineEdit(self)
            self.filter_rodzaj_uprawnienia = QLineEdit(self)
            self.filter_data_dodania = QLineEdit(self)
            self.filter_wymagany_acclvl = QLineEdit(self)
            self.filter_id.move(80, 150)
            self.filter_imie.move(80, 200)
            self.filter_nazwisko.move(80, 250)
            self.filter_id_umowy.move(80, 300)
            self.filter_rodzaj_uprawnienia.move(80, 350)
            self.filter_data_dodania.move(80, 400)
            self.filter_wymagany_acclvl.move(80, 450)
            self.filter_id.setPlaceholderText('Numer ID')
            self.filter_imie.setPlaceholderText('Imię')
            self.filter_nazwisko.setPlaceholderText('nazwisko')
            self.filter_id_umowy.setPlaceholderText('ID umowy')
            self.filter_rodzaj_uprawnienia.setPlaceholderText('Rodzaj uprawnienia')
            self.filter_data_dodania.setPlaceholderText('Data dodania')
            self.filter_wymagany_acclvl.setPlaceholderText('Wymagany poziom dostępu')
            self.hbox.addWidget(self.filter_wymagany_acclvl)
            self.hbox.addWidget(self.filter_id)
            self.hbox.addWidget(self.filter_imie)
            self.hbox.addWidget(self.filter_data_dodania)
            self.hbox.addWidget(self.filter_nazwisko)
            self.hbox.addWidget(self.filter_rodzaj_uprawnienia)
        elif cur_txt == 'osoba_fizyczna':
            self.filter_id = QLineEdit(self)
            self.filter_imie = QLineEdit(self)
            self.filter_nazwisko = QLineEdit(self)
            self.filter_pesel = QLineEdit(self)
            self.filter_id.move(80, 150)
            self.filter_imie.move(80, 200)
            self.filter_nazwisko.move(80, 250)
            self.filter_pesel.move(80, 300)
            self.filter_id.setPlaceholderText('Numer ID')
            self.filter_imie.setPlaceholderText('Imię')
            self.filter_nazwisko.setPlaceholderText('Nazwisko')
            self.filter_pesel.setPlaceholderText('PESEL')
            self.hbox.addWidget(self.filter_id)
            self.hbox.addWidget(self.filter_imie)
            self.hbox.addWidget(self.filter_nazwisko)
            self.hbox.addWidget(self.filter_pesel)
        elif cur_txt == 'organizacja':
            self.filter_id = QLineEdit(self)
            self.filter_nip = QLineEdit(self)
            self.filter_nazwa = QLineEdit(self)
            self.filter_regon = QLineEdit(self)
            self.filter_id.move(80, 150)
            self.filter_nip.move(80, 200)
            self.filter_nazwa.move(80, 250)
            self.filter_regon.move(80, 300)
            self.filter_id.setPlaceholderText('Numer ID')
            self.filter_nip.setPlaceholderText('NIP')
            self.filter_nazwa.setPlaceholderText('Nazwa')
            self.filter_regon.setPlaceholderText('REGON')
            self.hbox.addWidget(self.filter_id)
            self.hbox.addWidget(self.filter_nip)
            self.hbox.addWidget(self.filter_nazwa)
            self.hbox.addWidget(self.filter_regon)
        elif cur_txt == 'umowa':
            self.filter.setPlaceholderText('Wymagany poziom dostępu')
        self.setLayout(self.hbox)
        self.cur_txt = cur_txt
        query_btn = QPushButton('Wykonaj zapytanie', self)
        query_btn.setStyleSheet('QPushButton {background-color: red}')
        query_btn.move(100, 400)
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
        self.hbox = QHBoxLayout()
        combo = QComboBox(self)
        combo.addItem("dzial")
        combo.addItem("pracownik")
        combo.addItem("organizacja")
        combo.addItem("osoba_fizyczna")
        combo.addItem("osoba_uprawniona")
        combo.addItem("umowa")
        combo.move(80, 100)
        combo.activated[str].connect(self.build_ui)
        self.current_text = str(combo.currentText())
class DeleteWindow(QWidget):
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
        add_btn = QPushButton('Dodanie', self)
        add_btn.setStyleSheet('QPushButton {background-color: red}')
        add_btn.move(80, 350)
        add_btn.clicked.connect(self.add_click)
        edit_btn = QPushButton('Edycja', self)
        edit_btn.setStyleSheet('QPushButton {background-color: green}')
        edit_btn.move(80, 400)
        edit_btn.clicked.connect(self.edit_click)
        delete_btn = QPushButton('Usunięcie', self)
        delete_btn.setStyleSheet('QPushButton {background-color: blue}')
        delete_btn.move(80, 450)
        delete_btn.clicked.connect(self.delete_click)
        report_btn = QPushButton('Raport', self)
        report_btn.setStyleSheet('QPushButton {background-color: purple}')
        report_btn.move(80, 500)
        report_btn.clicked.connect(self.rep_click)
    @pyqtSlot()
    def view_click(self):
        self.viewWin = ViewWindow()
        self.viewWin.show()
    def add_click(self):
        self.addWin = AddWindow()
        self.addWin.show()
    def edit_click(self):
        self.editWin = EditWindow()
        self.editWin.show()
    def delete_click(self):
        self.delWin = DeleteWindow()
        self.delWin.show()
    @pyqtSlot()
    def rep_click(self):
        self.repWin = ReportWindow(login)
        self.repWin.show()
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
        global login
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
