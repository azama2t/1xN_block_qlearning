import sys
from PyQt5.QtWidgets import QApplication
from env import LineEnv
from ui import MainWindow


def main():
    app = QApplication(sys.argv)

    env = LineEnv(length=50)
    window = MainWindow(env)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
