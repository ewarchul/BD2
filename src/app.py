from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import *#QTableView, QApplication
from PyQt5 import QtCore#, QtGui
from PyQt5.QtGui import *
import sys


def createDB():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('sports.db')
    if not db.open():
        QMessageBox.critical(None, ("Cannot open database"),
                                   ("Unable to establish a database connection.\n"
                                                 "This example needs SQLite support. Please read "
                                                 "the Qt SQL driver documentation for information "
                                                 "how to build it.\n\n"
                                                 "Click Cancel to exit."),
                                   QMessageBox.Cancel)
    return False

    query = QtSql.QSqlQuery()
    query.exec_("create table sportsmen(id int primary key, "
                "firstname varchar(20), lastname varchar(20))")
    query.exec_("insert into sportsmen values(101, 'Roger', 'Federer')")
    query.exec_("insert into sportsmen values(102, 'Christiano', 'Ronaldo')")
    query.exec_("insert into sportsmen values(103, 'Ussain', 'Bolt')")
    query.exec_("insert into sportsmen values(104, 'Sachin', 'Tendulkar')")
    query.exec_("insert into sportsmen values(105, 'Saina', 'Nehwal')")
    return True


def createView(title, model):
   view = QTableView()
   view.setModel(model)
   view.setWindowTitle(title)
   return view
def initializeModel(model):
   model.setTable('sportsmen')
   model.setEditStrategy(QSqlTableModel.OnFieldChange)
   model.select()
   model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
   model.setHeaderData(1, QtCore.Qt.Horizontal, "First name")
   model.setHeaderData(2, QtCore.Qt.Horizontal, "Last name")
def findrow(i):
    delrow = i.row()


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Logowanie do systemu'
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 500
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
        #self.db = QLineEdit(self)
        btn = QPushButton('Zaloguj', self)
        btn.setStyleSheet('QPushButton {background-color: red}')
        btn.move(100, 300)
        btn = QPushButton('Wyłącz aplikację', self)
        btn.setStyleSheet('QPushButton {background-color: red}')
        btn.move(100, 350)
        btn = QPushButton('Pomoc', self)
        btn.setStyleSheet('QPushButton {background-color: red}')
        btn.move(100, 400)
        #btn.clicked.connect(self.SQL)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
       
    ex = App()
    sys.exit(app.exec_())

    


