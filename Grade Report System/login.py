from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from utils import center
from pymongo import MongoClient

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(0, 0, 300, 200)
        center(self)

        self.initUI()
        self.client = MongoClient("mongodb+srv://Gaboku:7oNQ15FbmFhpMGqI@gradereportcluster.onbdj.mongodb.net/")
        self.db = self.client["grade_report_system"]
        self.users_collection = self.db["user"]

    def initUI(self):
        layout = QVBoxLayout()

        self.username_label = QLabel("Username:", self)
        layout.addWidget(self.username_label)

        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Password:", self)
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = self.users_collection.find_one({"username": username, "password": password})
        if user:
            print("Login successful")
            self.accept_login()
        else:
            print("Login failed")
            self.username_input.clear()
            self.password_input.clear()

    def accept_login(self):
        from main import ClassroomWindow
        self.classroom_window = ClassroomWindow()
        self.classroom_window.show()
        self.close()
