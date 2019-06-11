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
            query_residual = 'poziom_dostepu = \'{}\' and imie = \'{}\' and nazwisko = \'{}\' and id_pracownika = \'{}\' and stanowisko = \'{}\' '.format(
                self.filter_acclvl.text(), self.filter_worker_name.text(), self.filter_worker_surname.text(),
                self.filter_worker_id.text(), self.filter_worker_job.text())
            key_val = re.sub('X', ' and ', 'X'.join(re.findall('\w+ = \'\S+\'', query_residual)))
            if (len(key_val)):
                query.prepare('select * from pracownik where ' + key_val)
            else:
                query.prepare('select * from pracownik')
        elif cur_txt == 'osoba_uprawniona':
            query_residual = 'wymagany_poziom_dostepu = \'{}\' and numer_osoby = \'{}\' and imie = \'{}\' and nazwisko = \'{}\' and rodzaj_uprawnienia = \'{}\' and data_dodania = \'{}\' '.format(
                self.filter_wymagany_acclvl.text(), self.filter_id.text(), self.filter_imie.text(),
                self.filter_nazwisko.text(), self.filter_rodzaj_uprawnienia.text(), self.filter_data_dodania.text())
            key_val = re.sub('X', ' and ', 'X'.join(re.findall('\w+ = \'\S+\'', query_residual)))
            if (len(key_val)):
                query.prepare('select * from osoba_uprawniona where ' + key_val)
            else:
                query.prepare('select * from osoba_uprawniona')
        elif cur_txt == 'osoba_fizyczna':
            query_residual = 'id_podmiotu = \'{}\' and imie = \'{}\' and nazwisko = \'{}\' and pesel = \'{}\' '.format(
                self.filter_id.text(), self.filter_imie.text(), self.filter_nazwisko.text(), self.filter_pesel.text())
            key_val = re.sub('X', ' and ', 'X'.join(re.findall('\w+ = \'\S+\'', query_residual)))
            if (len(key_val)):
                query.prepare('select * from osoba_fizyczna where ' + key_val)
            else:
                query.prepare('select * from osoba_fizyczna')
        elif cur_txt == 'organizacja':
            query_residual = 'id_podmiotu = \'{}\' and nip = \'{}\' and nazwa = \'{}\' and regon = \'{}\' '.format(
                self.filter_id.text(), self.filter_nip.text(), self.filter_nazwa.text(), self.filter_regon.text())
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

    def build_ui(self, text):
        cur_txt = text
        clearLayout(self.hbox)
        if cur_txt == 'pracownik':
            self.filter_check = QCheckBox("Aktwny?", self)
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
            self.filter_worker_label1 =  QLabel('wybierz pracownika do edycji')
            self.filter_worker_label1.move(50, 50)
            self.hbox.addWidget(self.filter_worker_label1)
            self.hbox.addWidget(self.filter_check)
            self.hbox.addWidget(self.filter_worker_job)
            self.hbox.addWidget(self.filter_worker_id)
            self.hbox.addWidget(self.filter_acclvl)
            self.hbox.addWidget(self.filter_worker_name)
            self.hbox.addWidget(self.filter_worker_surname)

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
            self.hbox.addWidget(self.filter_check_edit)
            self.hbox.addWidget(self.filter_worker_job_edit)
            self.hbox.addWidget(self.filter_worker_id_edit)
            self.hbox.addWidget(self.filter_acclvl_edit)
            self.hbox.addWidget(self.filter_worker_name_edit)
            self.hbox.addWidget(self.filter_worker_surname_edit)

        elif cur_txt == 'osoba_uprawniona':
            self.filter_worker_label1 = QLabel('wybierz usobę uprawniona do edycji')
            self.filter_worker_label1.move(50, 50)
            self.hbox.addWidget(self.filter_worker_label1)
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
            self.filter_worker_label1 = QLabel('wybierz usobę fizyczną do edycji')
            self.filter_worker_label1.move(50, 50)
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
            self.hbox.addWidget(self.filter_worker_label1)
            self.hbox.addWidget(self.filter_id)
            self.hbox.addWidget(self.filter_imie)
            self.hbox.addWidget(self.filter_nazwisko)
            self.hbox.addWidget(self.filter_pesel)

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
            self.filter = QLineEdit(self)
            self.filter.setPlaceholderText('Wymagany poziom dostępu')
            self.hbox.addWidget(self.filter)

            self.filter_label2 = QLabel('wpisz dane do zmiany')
            self.filter_label2.move(130, 50)
            self.hbox.addWidget(self.filter_label2)
            self.filter_edit = QLineEdit(self)
            self.filter_edit.setPlaceholderText('Wymagany poziom dostępu')
            self.hbox.addWidget(self.filter_edit)

        self.setLayout(self.hbox)
        self.cur_txt = cur_txt

        self.make_query()

        query_btn = QPushButton('Wykonaj zapytanie', self)
        query_btn.setStyleSheet('QPushButton {background-color: red}')
        query_btn.move(100, 400)
        query_btn.clicked.connect(self.make_query)
        query_btn.show()

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