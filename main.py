from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3
import mysql.connector


class DatabaseConnection:
    def __init__(self, host="localhost", user="root", password="tsmfan101Z", database="keyboards"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        connect = mysql.connector.connect(host=self.host, user=self.user,
                                          password=self.password, database=self.database)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Group Buy Order Tracker")
        self.setMinimumSize(1000, 800)

        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Keyboard", self)
        # add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        # about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_action)
        # search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "PRODUCT", "SHIP DATE", "URL"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
# main_window.load_data()
sys.exit(app.exec())
