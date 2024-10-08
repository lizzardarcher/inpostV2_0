import os
import sys
import random
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

client_parameters = [
    {
        "device_model": "iPhone 12",
        "app_version": "1.0.0",
        "system_version": "iOS 14.4",
        "lang_code": "ru"
    },
    {
        "device_model": "Samsung Galaxy S21",
        "app_version": "2.0.0",
        "system_version": "Android 11",
        "lang_code": "ru"
    },
    {
        "device_model": "POCO X3 Pro",
        "app_version": "1.1.0",
        "system_version": "Android 12",
        "lang_code": "ru"
    },
    {
        "device_model": "MacBook Pro",
        "app_version": "1.2.3",
        "system_version": "macOS Big Sur",
        "lang_code": "ru"
    },
    {
        "device_model": "iPhone 11",
        "app_version": "2.1.0",
        "system_version": "iOS 14.3",
        "lang_code": "ru"
    },
    {
        "device_model": "OnePlus 9",
        "app_version": "3.0.0",
        "system_version": "Android 12",
        "lang_code": "ru"
    },
    {
        "device_model": "iPad Pro",
        "app_version": "1.0.1",
        "system_version": "iPadOS 14.5",
        "lang_code": "ru"
    },
    {
        "device_model": "Sony Xperia",
        "app_version": "4.0.0",
        "system_version": "Android 10",
        "lang_code": "ru"
    },
    {
        "device_model": "iPhone 7 Plus",
        "app_version": "1.3.0",
        "system_version": "iOS 11.1",
        "lang_code": "ru"
    },
    {
        "device_model": "HTC One",
        "app_version": "5.0.0",
        "system_version": "Android 9",
        "lang_code": "ru"
    },
    {
        "device_model": "Nexus 5",
        "app_version": "1.4.1",
        "system_version": "Android 10",
        "lang_code": "ru"
    }
]

# Конфигурационный файл
config_file = "config.ini"


os.system('pip install pyrogram tgcrypto PyQt5')

# Загрузка конфигурации
def load_config():
    config = {}
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            for line in f:
                key, value = line.strip().split("=")
                config[key.strip()] = value.strip()
    else:
        exit(1)
    return config


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.params = random.choice(client_parameters)
        self.client = None
        self.code_window = None
        self.phone_code_hash = None
        self.setWindowTitle("🚀 S Construct")
        self.resize(400, 300)
        self.config = load_config()
        self.param_label_top = QLabel(f'Текущие параметры сессии:')
        self.param_label_1 = QLabel(f'Модель устройства: {self.params["device_model"]}')
        self.param_label_2 = QLabel(f'Версия приложения: {self.params["app_version"]}')
        self.param_label_3 = QLabel(f'Версия системы: {self.params["system_version"]}')
        self.param_label_4 = QLabel(f'Язык: {self.params["lang_code"]}')
        self.api_id = self.config["api_id"]
        self.api_hash = self.config["api_hash"]
        self.phone_number_label = QLabel("Phone Number:")
        self.phone_number_input = QLineEdit()

        self.login_button_1 = QPushButton("Создать session для чатов")
        self.login_button_1.clicked.connect(self.login_1)

        self.login_button_2 = QPushButton("Создать session для автоответчика")
        self.login_button_2.clicked.connect(self.login_2)

        layout = QVBoxLayout()
        layout.addWidget(self.param_label_top)
        layout.addWidget(self.param_label_1)
        layout.addWidget(self.param_label_2)
        layout.addWidget(self.param_label_3)
        layout.addWidget(self.param_label_4)
        layout.addWidget(self.phone_number_label)
        layout.addWidget(self.phone_number_input)
        layout.addWidget(self.login_button_1)
        layout.addWidget(self.login_button_2)
        self.setLayout(layout)

    def login_1(self):
        api_id = self.api_id
        api_hash = self.api_hash
        phone_number = (self.phone_number_input.text().replace(" ", "").replace("-", "")
                        .replace(")", "").replace("(", ""))

        if '+' not in phone_number:
            phone_number = '+' + phone_number

        if not api_id or not api_hash or not phone_number:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        try:
            self.client = Client(f"{str(api_id)}_chat",
                                 api_id=api_id, api_hash=api_hash, phone_number=phone_number,
                                 device_model=self.params['device_model'],
                                 app_version=self.params['app_version'],
                                 system_version=self.params['system_version'],
                                 lang_code=self.params['lang_code'])
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
        api_id = self.api_id
        api_hash = self.api_hash
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
                                 device_model=self.params['device_model'],
                                 app_version=self.params['app_version'],
                                 system_version=self.params['system_version'],
                                 lang_code=self.params['lang_code'])
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
