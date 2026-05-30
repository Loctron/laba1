from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush


class TimelineWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.processes = []
        self.observer_time = 0
        self.max_time = 140

     # Обновление максимального времени шкалы
    def update_max_time(self):
        if not self.processes:
            self.max_time = 100
            return

        self.max_time = max(
            p.end_max
            for p in self.processes
        ) + 10

        self.setMinimumHeight(400)

    # Установка списка процессов
    def set_processes(self, processes):
        self.processes = processes
        self.update_max_time()
        self.update()

    # Установка позиции наблюдателя
    def set_observer_time(self, t):
        self.observer_time = t
        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        self.draw_grid(painter)
        self.draw_processes(painter)
        self.draw_observer(painter)

    # Отрисовка временной сетки
    def draw_grid(self, painter):

        step = self.width() / self.max_time
        painter.setPen(QPen(QColor(230, 230, 230)))

        for i in range(self.max_time):
            x = int(i * step)
            painter.drawLine(x, 0, x, self.height())

    # Отрисовка процессов на шкале времени
    def draw_processes(self, painter):

        scale = self.width() / self.max_time

        for i, p in enumerate(self.processes):

            y = 40 + i * 60

            start = p.start_min * scale
            end = p.end_max * scale

            painter.setBrush(QBrush(QColor(p.color)))
            painter.setPen(QColor("black"))

            painter.drawRect(int(start), y, int(end - start), 30)
            painter.drawText(int(start + 5), y + 20, p.name)

    # Отрисовка линии наблюдателя
    def draw_observer(self, painter):

        x = self.observer_time * (self.width() / self.max_time)

        painter.setPen(QPen(QColor("red"), 2))
        painter.drawLine(int(x), 0, int(x), self.height())
