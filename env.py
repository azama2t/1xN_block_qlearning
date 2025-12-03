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

    def reset(self) -> int:
        """Агент в начальное состояние"""
        self.state = self.start_state
        return self.state
