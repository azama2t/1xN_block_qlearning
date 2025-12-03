from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
)
from PyQt5.QtCore import Qt
from env import LineEnv


class MainWindow(QMainWindow):
    """
    Простой интерфейс:
    - линия из N клеток
    - подсветка агента и цели
    - поле ввода количества эпизодов
    - кнопки "Запустить" и "Сбросить"
    Пока без реальной логики обучения и движения.
    """

    def __init__(self, env: LineEnv, parent=None):
        super().__init__(parent)
        self.env = env

        self.current_episode = 0

        self.setWindowTitle("RL демо - линия 0..9 (болванка UI)")
        self._init_ui()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        # Поле из клеток
        self.cells_layout = QHBoxLayout()
        self.cells = []

        for i in range(self.env.length):
            lbl = QLabel(" ")
            lbl.setFixedSize(40, 40)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("border: 1px solid black;")
            self.cells.append(lbl)
            self.cells_layout.addWidget(lbl)

        main_layout.addLayout(self.cells_layout)

        # Панель управления
        controls_layout = QHBoxLayout()

        self.episodes_input = QLineEdit()
        self.episodes_input.setPlaceholderText("кол-во эпизодов (пока не используется)")
        self.episodes_input.setFixedWidth(220)

        self.run_button = QPushButton("Запустить")
        self.run_button.clicked.connect(self.on_run_clicked)

        self.reset_button = QPushButton("Сбросить")
        self.reset_button.clicked.connect(self.on_reset_clicked)

        controls_layout.addWidget(self.episodes_input)
        controls_layout.addWidget(self.run_button)
        controls_layout.addWidget(self.reset_button)

        main_layout.addLayout(controls_layout)

        # Информация
        self.info_label = QLabel("UI загружен. Логика обучения пока не подключена.")
        self.info_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.info_label)

        # Первый рендер поля
        self.update_cells()

    def update_cells(self):
        """Обновление визуала поля с учетом env.state и env.goal_state."""
        for i, lbl in enumerate(self.cells):
            if i == self.env.state:
                lbl.setStyleSheet(
                    "border: 1px solid black; background-color: lightgreen;"
                )
                lbl.setText("A")  # агент
            elif i == self.env.goal_state:
                lbl.setStyleSheet(
                    "border: 1px solid black; background-color: lightblue;"
                )
                lbl.setText("G")  # цель
            else:
                lbl.setStyleSheet("border: 1px solid black;")
                lbl.setText(" ")

        self.info_label.setText(
            f"Эпизод: {self.current_episode} | "
            f"Позиция агента: {self.env.state} | "
            f"Цель: {self.env.goal_state} | "
            f"Логика обучения еще не реализована."
        )

    def on_reset_clicked(self):
        """Сбросить состояние среды и перерисовать поле."""
        self.env.reset()
        self.current_episode = 0
        self.update_cells()

    def on_run_clicked(self):
        """
        Пока что просто увеличиваем номер эпизода и обновляем текст.
        Логика шагов и обучения будет добавлена позже.
        """
        text = self.episodes_input.text().strip()
        if text:
            try:
                episodes = int(text)
            except ValueError:
                episodes = 1
        else:
            episodes = 1

        self.current_episode += 1
        self.info_label.setText(
            f"Нажат 'Запустить'. Запрошено эпизодов: {episodes}. "
            f"Эпизод (счетчик кликов): {self.current_episode}. "
            f"Логика обучения и шагов будет добавлена позже."
        )
        # Поле пока статично, но обновим его на всякий случай
        self.update_cells()
