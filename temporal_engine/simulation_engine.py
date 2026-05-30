from PyQt5.QtCore import QTimer


class SimulationEngine:

    def __init__(self, callback, max_time=140):
        # Текущее модельное время
        self.current_time = 0

        # Максимальное время моделирования
        self.max_time = max_time

        # Таймер Qt для дискретного увеличения времени
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)

        # Callback для обновления интерфейса
        self.callback = callback

    # Запуск симуляции
    def start(self):
        self.timer.start(300)

    # Остановка симуляции
    def stop(self):
        self.timer.stop()

    # Сброс времени
    def reset(self):
        self.current_time = 0
        self.callback(self.current_time)

    # Установка времени вручную
    def set_time(self, value):
        self.current_time = value
        self.callback(self.current_time)

    # Шаг моделирования времени
    def update_time(self):

        self.current_time += 1

        if self.current_time > self.max_time:
            self.stop()
            return

        self.callback(self.current_time)