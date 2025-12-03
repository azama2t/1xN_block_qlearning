from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
)
from PyQt5.QtCore import Qt, QTimer
from env import LineEnv
from agent import QLearningAgent


class MainWindow(QMainWindow):
    """
    Интерфейс:
    - линия из N клеток
    - подсветка агента и цели
    - поле ввода количества эпизодов
    - кнопки "Запустить" и "Сбросить"
    Логика обучения: один эпизод с анимацией или много эпизодов быстро.
    """

    def __init__(self, env: LineEnv, parent=None):
        super().__init__(parent)

        self.env = env
        self.agent = QLearningAgent(n_states=env.length, n_actions=2)

        self.current_episode = 0
        self.current_step = 0
        self.last_reward = 0.0
        self.last_action = None

        # таймер для анимированного одиночного эпизода
        self.timer = QTimer(self)
        self.timer.setInterval(500)  # 0.5 секунды между шагами
        self.timer.timeout.connect(self.single_episode_step)

        self.setWindowTitle("RL демо - линия 0..9")
        self._init_ui()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        # Поле из клеток
        self.cells_layout = QHBoxLayout()
        self.cells = []

        for _ in range(self.env.length):
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
        self.episodes_input.setPlaceholderText("кол-во эпизодов (пусто или 1 = один с анимацией)")
        self.episodes_input.setFixedWidth(260)

        self.run_button = QPushButton("Запустить")
        self.run_button.clicked.connect(self.on_run_clicked)

        self.reset_button = QPushButton("Сбросить")
        self.reset_button.clicked.connect(self.on_reset_clicked)

        controls_layout.addWidget(self.episodes_input)
        controls_layout.addWidget(self.run_button)
        controls_layout.addWidget(self.reset_button)

        main_layout.addLayout(controls_layout)

        # Информация
        self.info_label = QLabel("UI загружен. Агент пока не запускался.")
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
            f"Шаг: {self.current_step} | "
            f"Позиция: {self.env.state} | "
            f"Действие: {self.action_to_str(self.last_action)} | "
            f"Награда: {self.last_reward:.2f} | "
            f"epsilon: {self.agent.epsilon:.3f}"
        )

    @staticmethod
    def action_to_str(a):
        if a is None:
            return "-"
        return "L" if a == 0 else "R"

    def on_reset_clicked(self):
        """Сбросить состояние среды и перерисовать поле."""
        if self.timer.isActive():
            self.timer.stop()

        self.env.reset()
        self.current_episode = 0
        self.current_step = 0
        self.last_reward = 0.0
        self.last_action = None
        self.update_cells()

    def on_run_clicked(self):
        """
        Если поле пустое или 1:
            один эпизод с анимацией по таймеру.
        Если >1:
            обучение на N эпизодах без анимации, максимально быстро.
        """
        if self.timer.isActive():
            # если вдруг уже идет анимация, сначала её остановим
            self.timer.stop()

        text = self.episodes_input.text().strip()
        if text:
            try:
                n_episodes = int(text)
            except ValueError:
                n_episodes = 1
        else:
            n_episodes = 1

        if n_episodes <= 1:
            # один эпизод с анимацией
            self.start_single_episode()
        else:
            # много эпизодов быстро, без анимации
            self.train_many_episodes(n_episodes)

    def start_single_episode(self):
        """Подготовка одного эпизода с шагами по таймеру."""
        self.env.reset()
        self.current_step = 0
        self.current_episode += 1
        self.last_reward = 0.0
        self.last_action = None

        self.update_cells()

        self.run_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.timer.start()

    def single_episode_step(self):
        """Один шаг анимированного эпизода."""
        state = self.env.state
        action = self.agent.choose_action(state)
        next_state, reward, done = self.env.step(action)
        self.agent.learn(state, action, reward, next_state, done)

        self.current_step += 1
        self.last_reward = reward
        self.last_action = action

        self.update_cells()

        if done:
            self.timer.stop()
            # немного уменьшаем epsilon после эпизода
            self.agent.decay_epsilon(decay_rate=0.99)
            self.run_button.setEnabled(True)
            self.reset_button.setEnabled(True)

    def train_many_episodes(self, n_episodes: int):
        """Быстрая тренировка без анимации."""
        for _ in range(n_episodes):
            self.current_episode += 1
            state = self.env.reset()
            self.current_step = 0
            done = False

            while not done:
                action = self.agent.choose_action(state)
                next_state, reward, done = self.env.step(action)
                self.agent.learn(state, action, reward, next_state, done)
                state = next_state
                self.current_step += 1

            # после каждого эпизода уменьшаем epsilon
            self.agent.decay_epsilon(decay_rate=0.99)

        self.last_reward = reward
        self.last_action = action
        self.update_cells()
        self.info_label.setText(
            f"Быстрая тренировка: {n_episodes} эпизодов завершено. "
            f"Текущий epsilon: {self.agent.epsilon:.3f}"
        )
