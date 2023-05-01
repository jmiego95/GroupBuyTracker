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
        connection = mysql.connector.connect(host=self.host, user=self.user,
                                             password=self.password, database=self.database)
        return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Group Buy Order Tracker")
        self.setMinimumSize(1000, 800)

        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Keyboard", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("ID", "NAME", "PRODUCT", "SHIP DATE", "VENDOR"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # TOOLBAR ELEMENTS
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_student_action)

        # STATUS BAR
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # DETECT A CELL CLICK
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(delete_button)

    def load_data(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM keebs")
        result = cursor.fetchall()
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        Application to track your keyboard hobbies
        and group buy orders.
        """
        self.setText(content)


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remove Keyboard")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)

    def delete_student(self):
        # Get selected row index and student id
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE from keebs WHERE id = %s", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Keyboard")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name widget
        self.keyboard_name = QLineEdit()
        self.keyboard_name.setPlaceholderText("Name")
        layout.addWidget(self.keyboard_name)

        # Add combo box of courses
        self.product_type = QComboBox()
        product = ["Keycaps", "Keyboard", "Artisan Caps", " Artisan Cables", "Switches", "Deskmat", "Tools"]
        self.product_type.addItems(product)
        layout.addWidget(self.product_type)

        # Add mobile widget
        self.ship = QLineEdit()
        self.ship.setPlaceholderText("Ship Date")
        layout.addWidget(self.ship)

        self.url = QLineEdit()
        self.url.setPlaceholderText("Vendor URL")
        layout.addWidget(self.url)

        # Add a submit button
        button = QPushButton("Add Product")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.keyboard_name.text()
        product = self.product_type.itemText(self.product_type.currentIndex())
        ship = self.ship.text()
        url = self.url.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO keebs (name, product, ship, url) VALUES (%s, %s, %s, %s)",
                       (name, product, ship, url))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
