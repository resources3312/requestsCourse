from sys import argv
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QFormLayout, QLabel, QPushButton)
from PyQt6.QtGui import QIcon



class ApplicationGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Информация HTTP клиента")
        self.setFixedSize(500, 375)
        self.setWindowIcon(QIcon("./icon.ico"))
        
        self.headers: dict[str] = {
                                   "ip_addr": "IP адрес",
                                   "user_agent": "Агент пользователя",
                                   "port": "Исходный порт",
                                   "method": "Метод запроса",
                                   "encoding": "Сжатие",
                                   "mime": "MIME тип",
                                   "via": "Промежуточные узлы",
                                   "forwarded": "Исходный адрес"
                                   }

        self.widget = QWidget()
        self.widget.setStyleSheet("QLabel {color: #111111; font-weight: bold;} QPushButton {color: #111111; font-weight: bold;}")
        
        self.informationForm = QFormLayout()
        self.informationForm.setHorizontalSpacing(145)
        self.informationForm.setVerticalSpacing(25) 

        self.showInformationForm()
        
        self.updateButton = QPushButton("Обновить")
        self.updateButton.clicked.connect(self.updateInformationForm)
        self.informationForm.addRow(self.updateButton)
        
        self.widget.setLayout(self.informationForm)
        self.setCentralWidget(self.widget)
    
    def getClientData(self) -> dict:
        return requests.get("https://ifconfig.me/all.json").json()
    
    def showInformationForm(self) -> None:
        [self.informationForm.addRow(self.headers[key], QLabel(value)) for key, value in self.getClientData().items()]
    
    def updateInformationForm(self) -> None:
        values = list(self.getClientData().values())
        [self.informationForm.itemAt(values.index(value), QFormLayout.ItemRole.FieldRole).widget().setText(value) for value in values]



def main() -> None:
    app = QApplication(argv)
    gui = ApplicationGUI()
    gui.show()
    app.exec()

if __name__ == '__main__': main()
