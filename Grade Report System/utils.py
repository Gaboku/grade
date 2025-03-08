from PySide6.QtWidgets import QApplication

def center(window):
    qr = window.frameGeometry()
    cp = QApplication.primaryScreen().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())
