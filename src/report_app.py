import sqlite3
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtWidgets import *#QTableView, QApplication
class ReportWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.col1 = 0
        self.col2 = 300
        self.col3 = 600
        self.text_width = 300

        self.title = 'Raport'
        self.top = 100
        self.left = 100
        self.width = 650
        self.height = 950
        self.setBaseSize(self.width, self.height)
        self.setGeometry(self.top, self.left, self.height, self.width)
        self.logo = QLabel(self)

#SELECT 1
        self.label_SELECT_1 = QLabel(self)
        self.label_SELECT_1.setText("Filtr 1")
        self.label_SELECT_1.move(self.col1, 0)
        self.label_SELECT_1.show()

        self.text_ID_UMOWY = QLineEdit(self)
        self.text_ID_UMOWY.setPlaceholderText('ID UMOWY np. 23')
        self.text_ID_UMOWY.move(self.col1, 50)
        self.text_ID_UMOWY.setFixedWidth(self.text_width)
        self.text_ID_UMOWY.show()

        self.text_CZY_KOBIETA = QLineEdit(self)
        self.text_CZY_KOBIETA.setPlaceholderText('CZY KOBIETA? np.: false')
        self.text_CZY_KOBIETA.move(self.col1, 100)
        self.text_CZY_KOBIETA.setFixedWidth(self.text_width)
        self.text_CZY_KOBIETA.show()

        self.text_DATA_DODANIA = QLineEdit(self)
        self.text_DATA_DODANIA.setPlaceholderText('DATA DODANIA np. 1994-01-01')
        self.text_DATA_DODANIA.move(self.col1, 150)
        self.text_DATA_DODANIA.setFixedWidth(self.text_width)
        self.text_DATA_DODANIA.show()

        generate_1_btn = QPushButton('Generuj raport', self)
        generate_1_btn.move(0, 400)
        generate_1_btn.clicked.connect(self.generate_1_click)

# SELECT 2
        self.label_SELECT_2 = QLabel(self)
        self.label_SELECT_2.setText("Filtr 2")
        self.label_SELECT_2.move(self.col2, 0)
        self.label_SELECT_2.show()

        self.text_ID_PODMIOTU = QLineEdit(self)
        self.text_ID_PODMIOTU.setPlaceholderText('ID PODMIOTU np.: 1234')
        self.text_ID_PODMIOTU.move(self.col2, 50)
        self.text_ID_PODMIOTU.setFixedWidth(self.text_width)
        self.text_ID_PODMIOTU.show()

        self.text_MINIMALNA_ILOSC_POZYCJI_UMOWY = QLineEdit(self)
        self.text_MINIMALNA_ILOSC_POZYCJI_UMOWY.setPlaceholderText('MIN. IL. POZ. UMOWY np.: 11')
        self.text_MINIMALNA_ILOSC_POZYCJI_UMOWY.move(self.col2, 100)
        self.text_MINIMALNA_ILOSC_POZYCJI_UMOWY.setFixedWidth(self.text_width)
        self.text_MINIMALNA_ILOSC_POZYCJI_UMOWY.show()

        self.text_DATA_OD = QLineEdit(self)
        self.text_DATA_OD.setPlaceholderText('DATA DO np.: 1800-01-01')
        self.text_DATA_OD.move(self.col2, 150)
        self.text_DATA_OD.setFixedWidth(self.text_width)
        self.text_DATA_OD.show()

        self.text_DATA_DO = QLineEdit(self)
        self.text_DATA_DO.setPlaceholderText('DATA DO np.: 2019-01-01')
        self.text_DATA_DO.move(self.col2, 200)
        self.text_DATA_DO.setFixedWidth(self.text_width)
        self.text_DATA_DO.show()

        generate_2_btn = QPushButton('Generuj raport', self)
        generate_2_btn.move(self.col2, 400)
        generate_2_btn.clicked.connect(self.generate_2_click)

# SELECT 3
        self.label_SELECT_3 = QLabel(self)
        self.label_SELECT_3.setText("Filtr 3")
        self.label_SELECT_3.move(self.col3, 0)
        self.label_SELECT_3.show()

        self.text_ROK = QLineEdit(self)
        self.text_ROK.setPlaceholderText('DATA DO np.: 2001')
        self.text_ROK.move(self.col3, 50)
        self.text_ROK.setFixedWidth(self.text_width)
        self.text_ROK.show()

        generate_3_btn = QPushButton('Generuj raport', self)
        generate_3_btn.move(self.col3, 400)
        generate_3_btn.clicked.connect(self.generate_3_click)

    @pyqtSlot()
    def generate_1_click(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('mydbx')
        db.open()
        query = QSqlQuery(db)

        txt = """
        SELECT
            imie, nazwisko
        FROM
            osoba_fizyczna
        WHERE
            id_podmiotu=(SELECT podmiot_zewnetrzny_id_podmiotu FROM umowa WHERE id_umowy="""+self.text_ID_UMOWY.text()+""")
            AND (
                ("""+self.text_CZY_KOBIETA.text()+""" AND substr(imie, -1) == 'a')
                OR (NOT """+self.text_CZY_KOBIETA.text()+""" AND substr(imie, -1) <> 'a')
            )
        UNION ALL
        
        
        SELECT
            imie, nazwisko
        FROM
            osoba_uprawniona
        WHERE
            id_umowy="""+self.text_ID_UMOWY.text()+"""
            AND wymagany_poziom_dostepu <= (SELECT wymagany_poziom_dostepu FROM umowa WHERE id_umowy="""+self.text_ID_UMOWY.text()+""")
            AND data_dodania >= """+self.text_DATA_DODANIA.text()+"""
            AND (
                    ("""+self.text_CZY_KOBIETA.text()+""" AND substr(imie, -1) == 'a')
                    OR (NOT """+self.text_CZY_KOBIETA.text()+""" AND substr(imie, -1) <> 'a')
                )
"""
        query.prepare(txt)
        query.exec()
        model = QSqlQueryModel()
        model.setQuery(query)
        tableview = QTableView(self)
        tableview.setGeometry(500, 0, self.width, 400)
        tableview.setModel(model)
        tableview.resizeColumnsToContents()
        tableview.move(0, 500)
        tableview.show()
        db.close()

        text = "\n\n"
        m = tableview.model()
        for i in range(m.columnCount()):
            for j in range(m.rowCount()):
                text += m.index(i, j).data() + " "
            text += "\n"

        print(text)

        text_file = open("raport.txt", "w")
        text_file.write(text)
        text_file.close()

    @pyqtSlot()
    def generate_2_click(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('mydbx')
        db.open()
        query = QSqlQuery(db)

        txt = """
            SELECT 
                count(*) as liczba_pozycji_umowy, u.id_umowy, u.nazwa_umowy, u.data_utworzenia
            FROM 
                pozycja p
            JOIN
                umowa u ON p.id_umowy = u.id_umowy
            WHERE 
                u.podmiot_zewnetrzny_id_podmiotu = """+self.text_ID_PODMIOTU.text()+"""
                AND u.data_utworzenia >= """+self.text_DATA_OD.text()+"""
	            AND u.data_utworzenia <= """+self.text_DATA_DO.text()+"""
            GROUP BY 
                u.id_umowy
            HAVING 
                liczba_pozycji_umowy >= """+self.text_MINIMALNA_ILOSC_POZYCJI_UMOWY.text()+"""
            ORDER BY
                nazwa_umowy
            """
        query.prepare(txt)
        query.exec()
        model = QSqlQueryModel()
        model.setQuery(query)
        tableview = QTableView(self)
        tableview.setGeometry(500, 0, self.width, 400)
        tableview.setModel(model)
        tableview.resizeColumnsToContents()
        tableview.move(0, 500)
        tableview.show()
        db.close()
    @pyqtSlot()
    def generate_3_click(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('mydbx')
        db.open()
        query = QSqlQuery(db)

        txt = """
            SELECT 
                count(*), o.* 
            FROM 
                osoba_uprawniona up
            JOIN
                umowa u ON u.id_umowy = up.id_umowy
            JOIN
                organizacja o ON o.id_podmiotu = u.podmiot_zewnetrzny_id_podmiotu
            WHERE 
                u.data_utworzenia >= """+self.text_ROK.text()+""" || '-01-01'
                AND u.data_utworzenia <= """+self.text_ROK.text()+""" || '-12-31'
            GROUP BY 
                o.id_podmiotu
                """
        query.prepare(txt)
        query.exec()
        model = QSqlQueryModel()
        model.setQuery(query)
        tableview = QTableView(self)
        tableview.setGeometry(500, 0, self.width, 400)
        tableview.setModel(model)
        tableview.resizeColumnsToContents()
        tableview.move(0, 500)
        tableview.show()
        db.close()