import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QListWidget, QListWidgetItem, QInputDialog
from pymongo import MongoClient
from utils import center
import login

class ClassroomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Classroom")
        self.setGeometry(0, 0, 600, 400)
        center(self)

        mongo_uri = os.getenv("MONGODB_URI")
        if not mongo_uri:
            raise ValueError("MONGODB_URI environment variable not set")
        self.client = MongoClient(mongo_uri)
        self.db = self.client["grade_report_system"]
        self.subjects_collection = self.db["subjects"]

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.title_label = QLabel("My Subjects and Sections", self)
        layout.addWidget(self.title_label)

        self.subjects_list = QListWidget(self)
        layout.addWidget(self.subjects_list)

        self.add_subject_button = QPushButton("Add Subject", self)  # Add button
        self.add_subject_button.clicked.connect(self.add_subject)
        layout.addWidget(self.add_subject_button)

        self.load_subjects()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_subjects(self):
        subjects = self.subjects_collection.find()
        for subject in subjects:
            item = QListWidgetItem(f"{subject['name']} - {subject['section']}")
            self.subjects_list.addItem(item)

    def add_subject(self):
        name, ok_name = QInputDialog.getText(self, "Add Subject", "Enter subject name:")
        if not ok_name or not name.strip():
            return

        section, ok_section = QInputDialog.getText(self, "Add Subject", "Enter section:")
        if not ok_section or not section.strip():
            return

        subject = {"name": name.strip(), "section": section.strip()}
        self.subjects_collection.insert_one(subject)  # Add to database

        # Ensure the new subject is added to the subjects_list
        item = QListWidgetItem(f"{subject['name']} - {subject['section']}")
        self.subjects_list.addItem(item)
        self.subjects_list.repaint()  # Force the list to refresh

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grade Report System")
        self.setGeometry(0, 0, 300, 300)
        center(self)

    def show_classroom(self):
        self.classroom_window = ClassroomWindow()
        self.classroom_window.show()
        self.close()

def window():
    app = QApplication(sys.argv)
    login_window = login.LoginWindow()
    login_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    window()
