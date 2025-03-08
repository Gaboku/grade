from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QListWidget, QListWidgetItem
from utils import center
from pymongo import MongoClient

class ClassroomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Classroom")
        self.setGeometry(0, 0, 600, 400)
        center(self)

        self.client = MongoClient("mongodb+srv://Gaboku:7oNQ15FbmFhpMGqI@gradereportcluster.onbdj.mongodb.net/")
        self.db = self.client["grade_report_system"]
        self.subjects_collection = self.db["subjects"]

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("My Subjects and Sections", self)
        layout.addWidget(self.title_label)

        self.subjects_list = QListWidget(self)
        layout.addWidget(self.subjects_list)

        self.load_subjects()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_subjects(self):
        subjects = self.subjects_collection.find()
        for subject in subjects:
            item = QListWidgetItem(f"{subject['name']} - {subject['section']}")
            self.subjects_list.addItem(item)
