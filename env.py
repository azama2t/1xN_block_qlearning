from const import start_state

class LineEnv:
    """
    Линия из N клеток
    """

    def __init__(self, length: int = 10):
        self.length = length
        self.start_state = start_state # начал позиция
        self.goal_state = length - 1 # цель
        self.state = self.start_state  # текущее состояние
        self.max_steps = length * 3  # максимум шагов за эпизод
        self.steps_taken = 0 # сделанные шаги

    def step(self, action: int) -> (int, float, bool): # pyright: ignore[reportInvalidTypeForm]
        """
        Действие:
        0 - влево, 1 - вправо
        return: state, reward, done
        return: новое состояние, награду, конец/нет
        """
        if action == 0:  # влево
            if self.state > 0:
                self.state -= 1
        elif action == 1:  # вправо
            if self.state < self.goal_state:
                self.state += 1

        self.steps_taken += 1

        # Проверка на достижение цели
        done = self.state == self.goal_state or self.steps_taken >= self.max_steps

        # Награда
        if self.state == self.goal_state:
            reward = 10.0  # достигли цели
        else:
            reward = -1.0  # штраф за каждый шаг

        return self.state, reward, done

    def reset(self) -> int:
        """Агент в начальное состояние"""
        self.state = self.start_state
        self.steps_taken = 0
        return self.state
