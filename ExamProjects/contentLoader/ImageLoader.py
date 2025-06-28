from sys import argv
import os
from time import sleep
import requests

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from PyQt6.QtWidgets import (
QApplication, QMainWindow, QWidget,
QVBoxLayout,
QLabel, QPushButton, QLineEdit, QListWidget,
QMessageBox)


class ImageLoaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Loader")
        self.setFixedSize(500, 200)
        self.setWindowIcon(QIcon("./icon.ico"))
        
        self.setStyleSheet("QLabel {color: #222222; font-weight: bold;} QPushButton {color: #222222; font-weight: bold;}")
        self.widget = QWidget()
        
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)            
        
        self.listTitle = QLabel("Список сохраненых изображений")
        
        self.savedList = QListWidget()
        
        self.linkEntry = QLineEdit()
        self.linkEntry.setPlaceholderText("Введите ссылку для скачивания, например: https://<site>/<path>/<image.png>")
        
        self.downloadButton = QPushButton("Начать скачивание")
        self.downloadButton.clicked.connect(self.startDownload)

        self.layout.addWidget(self.listTitle, stretch=1, alignment=Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.savedList)
        self.layout.addWidget(self.linkEntry)
        self.layout.addWidget(self.downloadButton)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def startDownload(self) -> None:
        self.switchInterfaceMode()
        if "http" in self.linkEntry.text() and "://" in self.linkEntry.text() and self.downloadFile():
            self.savedList.addItem(self.linkEntry.text())
            self.switchInterfaceMode()
            self.linkEntry.clear()
            QMessageBox.information(None, 
                                    "Скачивание завершено",
                                    "Файл был сохранен, и находится в директории storage",
                                    QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.warning(None, 
                                "Невалидные значения",
                                "Проверьте ссылку и повторите попытку",
                                QMessageBox.StandardButton.Ok)
            self.switchInterfaceMode()

    def downloadFile(self) -> bool:
        try:
            res = requests.get(self.linkEntry.text())
            filename = self.linkEntry.text().split("/")[len(self.linkEntry.text().split("/")) - 1]
            
            if res.status_code == 200 and res.headers["Content-Type"].split("/")[0] == "image":
                with open(f"./storage/{filename}", "wb") as file:
                    for chunk in res.iter_content(chunk_size=4096): file.write(chunk)
                    return True

            else: return False
        
        except (OSError, requests.ConnectionError, requests.RequestException): return False
    
    def switchInterfaceMode(self):
        if self.linkEntry.isEnabled():
            self.linkEntry.setEnabled(False)
            self.downloadButton.setEnabled(False)
            self.downloadButton.setText("Ожидайте, идет загрузка..")

        else:
            self.linkEntry.setEnabled(True)
            self.downloadButton.setEnabled(True)
            self.downloadButton.setText("Начать скачивание")



def main() -> None:
    if not os.path.exists("./storage"): os.mkdir("storage")
    app = QApplication(argv)
    gui = ImageLoaderApp()
    gui.show()
    app.exec()

if __name__ == '__main__': main()
