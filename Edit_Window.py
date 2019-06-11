from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtWidgets import *#QTableView, QApplication
#from PyQt5 import QtCore #, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sqlite3
import sys
import re

def clearLayout(layout):
    for i in range(layout.count()): layout.itemAt(i).widget().close()

class EditWindow(QWidget):
    @pyqtSlot()
    def make_query(self):
        cur_txt = self.cur_txt
        db = QSqlDatabase.addDatabase('QSQLITE')
        print(cur_txt)
        db.setDatabaseName('mydb')
        db.open()
        query = QSqlQuery(db)
        if cur_txt == 'pracownik':
            query_residual = 'id_pracownika = \'{}\' and poziom_dostepu = \'{}\' and imie = \'{}\' and nazwisko = \'{}\' and stanowisko = \'{}\' '.format(
                self.id_pracownik.text(), '', '', '', '')
            key_val = re.sub('X', ' and ', 'X'.join(re.findall('\w+ = \'\S+\'', query_residual)))
            if (len(key_val)):
                query.prepare('select * from pracownik where ' + key_val)
            else:
                query.prepare('select * from pracownik')
        elif cur_txt == 'osoba_uprawniona':
            query_residual = 'numer_osoby = \'{}\' and wymagany_poziom_dostepu = \'{}\' and imie = \'{}\' and nazwisko = \'{}\' and rodzaj_uprawnienia = \'{}\' and data_dodania = \'{}\' '.format(
                self.id_os_upraw.text(), '', '', '', '', '')
            key_val = re.sub('X', ' and ', 'X'.join(re.findall('\w+ = \'\S+\'', query_residual)))
            if (len(key_val)):
                query.prepare('select * from osoba_uprawniona where ' + key_val)
            else:
                query.prepare('select * from osoba_uprawniona')
        elif cur_txt == 'osoba_fizyczna':
            query_residual = 'id_podmiotu = \'{}\' and imie = \'{}\' and nazwisko = \'{}\' and pesel = \'{}\' '.format(
                self.id_os_fiz.text(), '', '', '')
            key_val = re.sub('X', ' and ', 'X'.join(re.findall('\w+ = \'\S+\'', query_residual)))
            if (len(key_val)):
                query.prepare('select * from osoba_fizyczna where ' + key_val)
            else:
                query.prepare('select * from osoba_fizyczna')
        elif cur_txt == 'organizacja':
            query_residual = 'id_podmiotu = \'{}\' and nip = \'{}\' and nazwa = \'{}\' and regon = \'{}\' '.format(
                self.id_organizacja.text(), '', '', '')
            key_val = re.sub('X', ' and ', 'X'.join(re.findall('\w+ = \'\S+\'', query_residual)))
            if (len(key_val)):
                query.prepare('select * from organizacja where ' + key_val)
            else:
                query.prepare('select * from organizacja')

        elif cur_txt == 'umowa':
            query.prepare('select * from {} where {}')
        try:
            query.exec()
        except:
            QMessageBox.about(self, 'Komunikat', 'Baza zwraca jakis błąd')

        model = QSqlQueryModel()
        model.setQuery(query)
        tableview = QTableView(self)
        tableview.setModel(model)
        tableview.resizeColumnsToContents()
        tableview.move(300, 100)
        tableview.resize(600, 200)
        tableview.show()


        self.make_add_query()

    def build_ui(self, text):
        cur_txt = text
        clearLayout(self.hbox)
        if cur_txt == 'pracownik':

            self.filter_worker_label1 = QLabel('wybierz pracownika do edycji')
            self.filter_worker_label1.move(50, 50)
            self.hbox.addWidget(self.filter_worker_label1)

            self.id_pracownik = QLineEdit(self)
            self.id_pracownik.setPlaceholderText('ID pracownika')
            self.id_pracownik.move(80, 150)
            self.hbox.addWidget(self.id_pracownik)

            self.filter_worker_label2 = QLabel('wpisz dane do zmiany')
            self.filter_worker_label2.move(130, 50)
            self.filter_check_edit = QCheckBox("Aktwny?", self)
            self.filter_check_edit.move(350, 350)
            self.filter_check_edit.show()
            self.filter_acclvl_edit = QLineEdit(self)
            self.filter_acclvl_edit.setPlaceholderText('Poziom dostępu')
            self.filter_acclvl_edit.move(160, 150)
            self.filter_worker_name_edit = QLineEdit(self)
            self.filter_worker_name_edit.setPlaceholderText('Imię')
            self.filter_worker_name_edit.move(160, 200)
            self.filter_worker_id_edit = QLineEdit(self)
            self.filter_worker_id_edit.setPlaceholderText('Numer ID')
            self.filter_worker_id_edit.move(160, 250)
            self.filter_worker_surname_edit = QLineEdit(self)
            self.filter_worker_surname_edit.setPlaceholderText('Nazwisko')
            self.filter_worker_surname_edit.move(160, 300)
            self.filter_worker_job_edit = QLineEdit(self)
            self.filter_worker_job_edit.setPlaceholderText('Stanowisko')
            self.filter_worker_job_edit.move(160, 350)

            self.hbox.addWidget(self.filter_worker_label2)
            self.hbox.addWidget(self.filter_worker_label2)
            self.hbox.addWidget(self.filter_check_edit)
            self.hbox.addWidget(self.filter_worker_job_edit)
            self.hbox.addWidget(self.filter_worker_id_edit)
            self.hbox.addWidget(self.filter_acclvl_edit)
            self.hbox.addWidget(self.filter_worker_name_edit)
            self.hbox.addWidget(self.filter_worker_surname_edit)

        elif cur_txt == 'osoba_uprawniona':

            self.filter_worker_label1 = QLabel('wybierz osobę uprawniona do edycji')
            self.filter_worker_label1.move(50, 50)
            self.hbox.addWidget(self.filter_worker_label1)

            self.id_os_upraw = QLineEdit(self)
            self.id_os_upraw.setPlaceholderText('ID osoby uprawnionej')
            self.id_os_upraw.move(80, 150)
            self.hbox.addWidget(self.id_os_upraw)

            self.filter_label2 = QLabel('wpisz dane do zmiany')
            self.filter_label2.move(130, 50)
            self.filter_id_edit = QLineEdit(self)
            self.filter_imie_edit = QLineEdit(self)
            self.filter_nazwisko_edit = QLineEdit(self)
            self.filter_id_umowy_edit = QLineEdit(self)
            self.filter_rodzaj_uprawnienia_edit = QLineEdit(self)
            self.filter_data_dodania_edit = QLineEdit(self)
            self.filter_wymagany_acclvl_edit = QLineEdit(self)
            self.filter_id_edit.move(160, 150)
            self.filter_imie_edit.move(160, 200)
            self.filter_nazwisko_edit.move(160, 250)
            self.filter_id_umowy_edit.move(160, 300)
            self.filter_rodzaj_uprawnienia_edit.move(160, 350)
            self.filter_data_dodania_edit.move(160, 400)
            self.filter_wymagany_acclvl_edit.move(160, 450)
            self.filter_id_edit.setPlaceholderText('Numer ID')
            self.filter_imie_edit.setPlaceholderText('Imię')
            self.filter_nazwisko_edit.setPlaceholderText('nazwisko')
            self.filter_id_umowy_edit.setPlaceholderText('ID umowy')
            self.filter_rodzaj_uprawnienia_edit.setPlaceholderText('Rodzaj uprawnienia')
            self.filter_data_dodania_edit.setPlaceholderText('Data dodania')
            self.filter_wymagany_acclvl_edit.setPlaceholderText('Wymagany poziom dostępu')
            self.hbox.addWidget(self.filter_label2)
            self.hbox.addWidget(self.filter_wymagany_acclvl_edit)
            self.hbox.addWidget(self.filter_id_edit)
            self.hbox.addWidget(self.filter_imie_edit)
            self.hbox.addWidget(self.filter_data_dodania_edit)
            self.hbox.addWidget(self.filter_nazwisko_edit)
            self.hbox.addWidget(self.filter_rodzaj_uprawnienia_edit)

        elif cur_txt == 'osoba_fizyczna':
            self.filter_worker_label1 = QLabel('wybierz osobę fizyczną do edycji')
            self.filter_worker_label1.move(50, 50)
            self.hbox.addWidget(self.filter_worker_label1)

            self.id_os_fiz = QLineEdit(self)
            self.id_os_fiz.setPlaceholderText('ID osoby fizycznej')
            self.id_os_fiz.move(80, 150)
            self.hbox.addWidget(self.id_os_fiz)

            self.filter_label2 = QLabel('wpisz dane do zmiany')
            self.filter_label2.move(130, 50)
            self.filter_id_edit = QLineEdit(self)
            self.filter_imie_edit = QLineEdit(self)
            self.filter_nazwisko_edit = QLineEdit(self)
            self.filter_pesel_edit = QLineEdit(self)
            self.filter_id_edit.move(160, 150)
            self.filter_imie_edit.move(160, 200)
            self.filter_nazwisko_edit.move(160, 250)
            self.filter_pesel_edit.move(160, 300)
            self.filter_id_edit.setPlaceholderText('Numer ID')
            self.filter_imie_edit.setPlaceholderText('Imię')
            self.filter_nazwisko_edit.setPlaceholderText('Nazwisko')
            self.filter_pesel_edit.setPlaceholderText('PESEL')
            self.hbox.addWidget(self.filter_label2)
            self.hbox.addWidget(self.filter_id_edit)
            self.hbox.addWidget(self.filter_imie_edit)
            self.hbox.addWidget(self.filter_nazwisko_edit)
            self.hbox.addWidget(self.filter_pesel_edit)
        elif cur_txt == 'organizacja':
            self.filter_worker_label1 = QLabel('wybierz organizację do edycji')
            self.filter_worker_label1.move(50, 50)
            self.hbox.addWidget(self.filter_worker_label1)

            self.id_organizacja = QLineEdit(self)
            self.id_organizacja.setPlaceholderText('ID organizacji')
            self.id_organizacja.move(80, 150)
            self.hbox.addWidget(self.id_organizacja)

            self.filter_label2 = QLabel('wpisz dane do edycji')
            self.filter_label2.move(50, 50)
            self.hbox.addWidget(self.filter_label2)
            self.filter_id_edit = QLineEdit(self)
            self.filter_nip_edit = QLineEdit(self)
            self.filter_nazwa_edit = QLineEdit(self)
            self.filter_regon_edit = QLineEdit(self)
            self.filter_id_edit.move(160, 150)
            self.filter_nip_edit.move(160, 200)
            self.filter_nazwa_edit.move(160, 250)
            self.filter_regon_edit.move(160, 300)
            self.filter_id_edit.setPlaceholderText('Numer ID')
            self.filter_nip_edit.setPlaceholderText('NIP')
            self.filter_nazwa_edit.setPlaceholderText('Nazwa')
            self.filter_regon_edit.setPlaceholderText('REGON')
            self.hbox.addWidget(self.filter_id_edit)
            self.hbox.addWidget(self.filter_nip_edit)
            self.hbox.addWidget(self.filter_nazwa_edit)
            self.hbox.addWidget(self.filter_regon_edit)
        elif cur_txt == 'umowa':
            self.filter_label1 = QLabel('wybierz umowę do zmiany')
            self.filter_label1.move(130, 50)
            self.hbox.addWidget(self.filter_label1)

            self.id_umowa = QLineEdit(self)
            self.id_umowa.setPlaceholderText('ID umowy')
            self.id_umowa.move(80, 150)
            self.hbox.addWidget(self.id_umowa)

            self.filter_label2 = QLabel('wpisz dane do zmiany')
            self.filter_label2.move(130, 50)
            self.hbox.addWidget(self.filter_label2)
            self.filter_edit = QLineEdit(self)
            self.filter_edit.setPlaceholderText('Wymagany poziom dostępu')
            self.hbox.addWidget(self.filter_edit)

        self.setLayout(self.hbox)
        self.cur_txt = cur_txt

        #self.make_query()

        query_btn = QPushButton('Wykonaj zapytanie', self)
        query_btn.setStyleSheet('QPushButton {background-color: red}')
        query_btn.move(100, 400)
        query_btn.clicked.connect(self.make_query)
        query_btn.show()

        edit_btn = QPushButton('EDYTUJ', self)
        edit_btn.setStyleSheet('QPushButton {background-color: red}')
        edit_btn.move(400, 400)
        edit_btn.clicked.connect(self.edit)
        edit_btn.show()

    def edit(self):
        self.make_remove_query()
        self.make_add_query()

    def make_remove_query(self):
        cur_txt = self.cur_txt
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('mydbx')
        db.open()
        query = QSqlQuery(db)

        if cur_txt == 'pracownik':
            query.prepare('delete from pracownik where ' + self.id_pracownik.text())
        elif cur_txt == 'osoba_uprawniona':
            query.prepare('delete from osoba_uprawniona where ' + self.id_os_upraw.text())
        elif cur_txt == 'osoba_fizyczna':
            query.prepare('delete from osoba_fizyczna where ' + self.id_os_fiz.text())
        elif cur_txt == 'organizacja':
            query.prepare('delete from organizacja where ' + self.id_organizacja.text())
        #elif cur_txt == 'umowa':
            #query.prepare('delete from umowa where ' + self.id_umowa.text())

        query.exec()
        model = QSqlQueryModel()
        model.setQuery(query)

    def make_add_query(self):
        cur_txt = self.cur_txt
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('mydbx')
        db.open()
        query = QSqlQuery(db)

        if cur_txt == 'pracownik':
            query_residual = ' id_dzialu = \'{}\' and poziom_dostepu = \'{}\' and imie = \'{}\' and nazwisko = \'{}\' and id_pracownika = \'{}\' and stanowisko = \'{}\' '.format(self.filter_worker_idd.text(), self.filter_acclvl.text(), self.filter_worker_name.text(), self.filter_worker_surname.text(), self.filter_worker_id.text(), self.filter_worker_job.text())
            keys = re.sub(',and', '',','.join(re.findall('\w+ ', query_residual)))
            values = ','.join(re.findall('\'.*?\'', query_residual))
            id_val = ' '.join(re.findall('id_pracownika = \S+', query_residual))
            conn = sqlite3.connect('mydbx')
            cursor = conn.cursor()
            cursor.execute('select * from pracownik where '+ id_val)
            if(len(cursor.fetchall())):
                QMessageBox.about(self, 'Komunikat', 'Istnieje już pracownik o zadanym numerze ID!')
            else:
                query.prepare('insert into pracownik ('+ keys + ') values (' + values + ')')
                QMessageBox.about(self, 'Komunikat', 'Wpis do bazy danych został dodany pomyślnie.')
        elif cur_txt == 'osoba_uprawniona':
            query_residual = 'wymagany_poziom_dostepu = \'{}\' and numer_osoby = \'{}\' and imie = \'{}\' and nazwisko = \'{}\' and rodzaj_uprawnienia = \'{}\' and data_dodania = \'{}\' '.format(self.filter_wymagany_acclvl.text(), self.filter_id.text(), self.filter_imie.text(),
                    self.filter_nazwisko.text(), self.filter_rodzaj_uprawnienia.text(), self.filter_data_dodania.text())
            keys = re.sub(',and', '',','.join(re.findall('\w+ ', query_residual)))
            values = ','.join(re.findall('\'.*?\'', query_residual))
            id_val = ' '.join(re.findall('number_osoby = \S+', query_residual))
            conn = sqlite3.connect('mydbx')
            cursor = conn.cursor()
            cursor.execute('select * from osoba_uprawniona where '+ id_val)
            if(len(cursor.fetchall())):
                QMessageBox.about(self, 'Komunikat', 'Istnieje już osoba uprawniona o zadanym numerze ID!')
            else:
                query.prepare('insert into osoba_uprawniona ('+ keys + ') values (' + values + ')')
                QMessageBox.about(self, 'Komunikat', 'Wpis do bazy danych został dodany pomyślnie.')
        elif cur_txt == 'osoba_fizyczna':
            query_residual = 'id_podmiotu = \'{}\' and imie = \'{}\' and nazwisko = \'{}\' and pesel = \'{}\' '.format(self.filter_id.text(), self.filter_imie.text(), self.filter_nazwisko.text(), self.filter_pesel.text())
            keys = re.sub(',and', '',','.join(re.findall('\w+ ', query_residual)))
            values = ','.join(re.findall('\'.*?\'', query_residual))
            id_val = ' '.join(re.findall('id_podmiotu = \S+', query_residual))
            conn = sqlite3.connect('mydbx')
            cursor = conn.cursor()
            cursor.execute('select * from osoba_fizyczna where '+ id_val)
            if(len(cursor.fetchall())):
                QMessageBox.about(self, 'Komunikat', 'Istnieje już podmiot zewnętrzny o zadanym numerze ID!')
            else:
                query.prepare('insert into osoba_fizyczna ('+ keys + ') values (' + values + ')')
                QMessageBox.about(self, 'Komunikat', 'Wpis do bazy danych został dodany pomyślnie.')

        elif cur_txt == 'organizacja':
            query_residual = 'id_podmiotu = \'{}\' and nip = \'{}\' and nazwa = \'{}\' and regon = \'{}\' '.format(self.filter_id.text(), self.filter_nip.text(), self.filter_nazwa.text(), self.filter_regon.text())
            keys = re.sub(',and', '',','.join(re.findall('\w+ ', query_residual)))
            values = ','.join(re.findall('\'.*?\'', query_residual))
            id_val = ' '.join(re.findall('id_podmiotu = \S+', query_residual))
            conn = sqlite3.connect('mydbx')
            cursor = conn.cursor()
            cursor.execute('select * from organizacja where '+ id_val)
            if(len(cursor.fetchall())):
                QMessageBox.about(self, 'Komunikat', 'Istnieje już podmiot zewnętrzny o zadanym numerze ID!')
            else:
                query.prepare('insert into organizacja ('+ keys + ') values (' + values + ')')
                QMessageBox.about(self, 'Komunikat', 'Wpis do bazy danych został dodany pomyślnie.')

        elif cur_txt == 'umowa':
            query_residual = 'id_umowy = \'{}\' and nazwa_umowy = \'{}\' and podmiot_zewnetrzny_id_podmiotu = \'{}\' and rodzaj_umowy = \'{}\' and data_utworzenia = \'{}\' and wymagany_poziom_dostepu = \'{}\''.format(self.filter_idu.text(), self.filter_nu.text(), self.filter_pz.text(), self.filter_rz.text(), self.filter_du.text(), self.filter_wpd.text())
            keys = re.sub(',and', '',','.join(re.findall('\w+ ', query_residual)))
            values = ','.join(re.findall('\'.*?\'', query_residual))
            id_val = ' '.join(re.findall('id_umowy = \S+', query_residual))
            conn = sqlite3.connect('mydbx')
            cursor = conn.cursor()
            cursor.execute('select * from umowa where '+ id_val)
            if(len(cursor.fetchall())):
                QMessageBox.about(self, 'Komunikat', 'Istnieje już umowa o zadanym numerze ID!')
            else:
                query.prepare('insert into umowa ('+ keys + ') values (' + values + ')')
                QMessageBox.about(self, 'Komunikat', 'Wpis do bazy danych został dodany pomyślnie.')

        query.exec()
        model = QSqlQueryModel()
        model.setQuery(query)

    def __init__(self):
        super().__init__()
        self.title = 'Edycja Danych'

        self.top = 100
        self.left = 100
        self.width = 1000
        self.height = 1000
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)
        self.hbox = QHBoxLayout()
        combo = QComboBox(self)
        combo.addItem("pracownik")
        combo.addItem("organizacja")
        combo.addItem("osoba_fizyczna")
        combo.addItem("osoba_uprawniona")
        combo.addItem("umowa")
        combo.move(80, 100)
        combo.activated[str].connect(self.build_ui)
        self.current_text = str(combo.currentText())

if __name__ == '__main__':
    app = QApplication([])

    editWin = EditWindow()
    editWin.show()
    app.exec_()