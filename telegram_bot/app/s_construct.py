import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)

from pyrogram import Client
import traceback

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.client = None
        self.code_window = None
        self.phone_code_hash = None
        self.setWindowTitle("🚀 S Construct")
        self.resize(400, 300)

        self.api_id_label = QLabel("API ID:")
        self.api_id_input = QLineEdit()

        self.api_hash_label = QLabel("API Hash:")
        self.api_hash_input = QLineEdit()

        self.phone_number_label = QLabel("Phone Number:")
        self.phone_number_input = QLineEdit()

        self.login_button_1 = QPushButton("Создать session для чатов")
        self.login_button_1.clicked.connect(self.login_1)

        self.login_button_2 = QPushButton("Создать session для автоответчика")
        self.login_button_2.clicked.connect(self.login_2)

        layout = QVBoxLayout()
        layout.addWidget(self.api_id_label)
        layout.addWidget(self.api_id_input)
        layout.addWidget(self.api_hash_label)
        layout.addWidget(self.api_hash_input)
        layout.addWidget(self.phone_number_label)
        layout.addWidget(self.phone_number_input)
        layout.addWidget(self.login_button_1)
        layout.addWidget(self.login_button_2)
        self.setLayout(layout)

    def login_1(self):
        api_id = self.api_id_input.text()
        api_hash = self.api_hash_input.text()
        phone_number = (self.phone_number_input.text().replace(" ", "").replace("-", "")
                                                        .replace(")", "").replace("(",""))

        if '+' not in phone_number:
            phone_number = '+' + phone_number

        if not api_id or not api_hash or not phone_number:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        try:
            self.client = Client(f"{str(api_id)}_chat",
                                 api_id=api_id, api_hash=api_hash, phone_number=phone_number,
                                 device_model='iphone 12 pro',
                                 app_version='15.3.0',
                                 system_version="24.04",
                                 lang_code="ru")
            self.client.connect()

            code = self.client.send_code(phone_number)
            print(code)

            self.phone_code_hash = code.phone_code_hash  # Получить phone_code_hash
            print(self.phone_code_hash)
            # client.disconnect()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to connect: {traceback.format_exc()}")
            return

        self.code_window = CodeWindow(client=self.client, phone_number=phone_number,
                                      phone_code_hash=self.phone_code_hash)
        print('Switch to sms code window')
        self.code_window.show()
        # self.close()

    def login_2(self):
        api_id = self.api_id_input.text()
        api_hash = self.api_hash_input.text()
        phone_number = (self.phone_number_input.text().replace(" ", "").replace("-", "")
                        .replace(")", "").replace("(", ""))

        if '+' not in phone_number:
            phone_number = '+' + phone_number

        if not api_id or not api_hash or not phone_number:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        try:
            self.client = Client(f"{str(api_id)}_auto_answering",
                                 api_id=api_id, api_hash=api_hash, phone_number=phone_number,
                                 device_model='iphone 12 pro',
                                 app_version='15.3.0',
                                 system_version="24.04",
                                 lang_code="ru")
            self.client.connect()

            code = self.client.send_code(phone_number)
            print(code)

            self.phone_code_hash = code.phone_code_hash  # Получить phone_code_hash
            print(self.phone_code_hash)
            # client.disconnect()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to connect: {traceback.format_exc()}")
            return

        self.code_window = CodeWindow(client=self.client, phone_number=phone_number,
                                      phone_code_hash=self.phone_code_hash)
        print('Switch to sms code window')
        self.code_window.show()
        # self.close()


class CodeWindow(QWidget):
    def __init__(self, client, phone_number, phone_code_hash):
        super().__init__()

        self.client = client
        self.phone_number = phone_number
        self.phone_code_hash = phone_code_hash

        self.setWindowTitle("Enter Code")
        self.resize(300, 150)

        self.code_label = QLabel(f"Enter code sent to {phone_number}:")
        self.code_input = QLineEdit()
        self.verify_button = QPushButton("Verify")
        self.verify_button.clicked.connect(self.verify)

        layout = QVBoxLayout()
        layout.addWidget(self.code_label)
        layout.addWidget(self.code_input)
        layout.addWidget(self.verify_button)
        self.setLayout(layout)

    def verify(self):
        code = self.code_input.text()

        if not code:
            QMessageBox.warning(self, "Error", "Please enter the code.")
            return

        try:
            # self.client.connect()
            print('Trying to verify code...')

            self.client.sign_in(phone_number=self.phone_number, phone_code_hash=self.phone_code_hash, phone_code=code)
            print('Code successfully verified!')

            self.client.disconnect()
            print('Disconnected!')

            QMessageBox.information(self, "Success", "Session created successfully!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to verify: {traceback.format_exc()}")
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
