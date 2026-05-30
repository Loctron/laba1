import sys
import os

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


def load_styles(app):

    path = os.path.join(os.path.dirname(__file__), "ui/styles.qss")

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())
    else:
        print("styles.qss not found:", path)


def main():

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Создание Qt-приложения
    app = QApplication(sys.argv)

    load_styles(app)

    # Создание главного окна
    window = MainWindow()
    window.show()

    # Запуск event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()