import random

class QLearningAgent:
    def __init__(self, n_states : int, n_actions : int, alpha=0.1, gamma=0.9, epsilon=0.3):
        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha = alpha      # скорость обучения
        self.gamma = gamma      # дисконтирование
        self.epsilon = epsilon  # вероятность случайного действия

        # q таблица инициализация с нулями
        self.q_table = [[0.0 for k in range(n_actions)] for i in range(n_states)]

    def choose_action(self, state : int) -> int:
        """
        Выбор действия
        0 - влево
        1 - вправо
        """
        

        if random.random() < self.epsilon:
            # добавляем случайность
            action = random.randint(0, self.n_actions - 1)
        else:
            # Если случайность не сработала, выбираем лучшее действие из Q-таблицы
            max_q = max(self.q_table[state])
            action = self.q_table[state].index(max_q)

        return action
    
    def learn(self, state : int, action : int, reward : float, next_state : int, done : bool) -> None:
        """
        сама МАГИЯ
        Обновление Q-таблицы на основе опыта.
        state      - состояние до действия
        action     - выбранное действие (0 или 1)
        reward     - награда за это действие
        next_state - новое состояние после действия
        done       - флаг окончания эпизода
        """
        old_value = self.q_table[state][action]

        if done:
            # эпизод окончен, награда - в данный момент
            target = reward
        else:
            # иначе учитываем то, сколько получим в будущем шаге
            next_max = max(self.q_table[next_state])
            target = reward + self.gamma * next_max

        # двигаем старое значение в сторону target на apha
        new_value = old_value + self.alpha * (target - old_value)
        self.q_table[state][action] = new_value
        
    def decay_epsilon(self, decay_rate : float) -> None:
        """
        Уменьшение epsilon для уменьшения случайных действий со временем
        """
        self.epsilon *= decay_rate