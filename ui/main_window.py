from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QSlider,
    QListWidget,
    QMessageBox
)

from PyQt5.QtCore import Qt

from ui.timeline_widget import TimelineWidget
from ui.relations_table import RelationsTable

from temporal_engine.simulation_engine import SimulationEngine
from temporal_engine.relation_engine import RelationEngine
from temporal_engine.temporal_analyzer import TemporalAnalyzer

from models.process_model import ProcessModel
from models.observer_model import ObserverModel

from database.db_manager import DatabaseManager


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Темпоральный процессор"
        )
        self.resize(1400, 850)

        # Инициализация базы данных
        self.db = DatabaseManager()

        # Загрузка процессов
        self.processes = []
        self.load_processes_from_db()

        # Модель наблюдателя времени
        self.observer = ObserverModel(0)

        # Создание интерфейса
        self.setup_ui()
        # Настройка симуляции
        self.setup_simulation()

        # Первичное обновление интерфейса
        self.update_interface(0)

    # ==================================================
    # ЗАГРУЗКА ПРОЦЕССОВ ИЗ БД
    # ==================================================

    def load_processes_from_db(self):

        self.processes.clear()

        rows = self.db.get_processes()

        for row in rows:

            self.processes.append(
                ProcessModel(*row)
            )

    # ==================================================
    # СОЗДАНИЕ ИНТЕРФЕЙСА
    # ==================================================

    def setup_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        main_layout = QHBoxLayout()

        central.setLayout(main_layout)

        # ==========================================
        # ЛЕВАЯ ПАНЕЛЬ
        # ==========================================

        left_panel = QVBoxLayout()

        self.start_btn = QPushButton("Запуск")

        self.stop_btn = QPushButton("Остановка")

        self.reset_btn = QPushButton("Сброс")

        self.find_past_btn = QPushButton(
            "Прошлые процессы"
        )

        self.find_active_btn = QPushButton(
            "Активные процессы"
        )

        self.find_future_btn = QPushButton(
            "Будущие процессы"
        )

        self.time_label = QLabel(
            "Позиция наблюдателя: 0"
        )

        left_panel.addWidget(self.start_btn)
        left_panel.addWidget(self.stop_btn)
        left_panel.addWidget(self.reset_btn)

        left_panel.addSpacing(20)

        left_panel.addSpacing(20)

        left_panel.addWidget(self.find_past_btn)
        left_panel.addWidget(self.find_active_btn)
        left_panel.addWidget(self.find_future_btn)

        left_panel.addSpacing(20)

        left_panel.addWidget(self.time_label)

        # ==========================================
        # ЦЕНТР
        # ==========================================

        center_panel = QVBoxLayout()

        self.timeline = TimelineWidget()

        self.timeline.set_processes(
            self.processes
        )

        self.slider = QSlider(Qt.Orientation.Horizontal)

        self.slider.setMinimum(0)

        self.slider.setMaximum(
            self.timeline.max_time
        )

        center_panel.addWidget(
            self.timeline
        )

        center_panel.addWidget(
            self.slider
        )

        # ==========================================
        # ПРАВАЯ ПАНЕЛЬ
        # ==========================================

        right_panel = QVBoxLayout()

        self.process_list = QListWidget()

        self.state_labels = []

        for process in self.processes:

            self.process_list.addItem(
                process.name
            )

        for process in self.processes:

            label = QLabel()

            self.state_labels.append(
                label
            )

            right_panel.addWidget(
                label
            )

        self.relations_table = RelationsTable()

        self.relations_table.update_relations(
            self.processes,
            RelationEngine
        )

        right_panel.addWidget(
            self.process_list
        )

        right_panel.addWidget(
            self.relations_table
        )

        # ==========================================
        # ДОБАВЛЕНИЕ ПАНЕЛЕЙ
        # ==========================================

        main_layout.addLayout(
            left_panel,
            1
        )

        main_layout.addLayout(
            center_panel,
            5
        )

        main_layout.addLayout(
            right_panel,
            3
        )

        self.right_panel = right_panel

        # ==========================================
        # СОБЫТИЯ
        # ==========================================

        self.slider.valueChanged.connect(
            self.update_interface
        )

        self.find_past_btn.clicked.connect(
            self.show_past_processes
        )

        self.find_active_btn.clicked.connect(
            self.show_active_processes
        )

        self.find_future_btn.clicked.connect(
            self.show_future_processes
        )

    # ==================================================
    # НАСТРОЙКА ИМИТАЦИИ
    # ==================================================

    def setup_simulation(self):

        self.engine = SimulationEngine(
            self.update_interface,
            self.timeline.max_time
        )

        self.start_btn.clicked.connect(
            self.engine.start
        )

        self.stop_btn.clicked.connect(
            self.engine.stop
        )

        self.reset_btn.clicked.connect(
            self.engine.reset
        )

    # ==================================================
    # ОБНОВЛЕНИЕ СПИСКОВ
    # ==================================================

    def refresh_ui(self):

        self.process_list.clear()

        for label in self.state_labels:
            label.deleteLater()

        self.state_labels.clear()

        for process in self.processes:

            self.process_list.addItem(
                process.name
            )

            label = QLabel()

            self.state_labels.append(
                label
            )

            self.right_panel.insertWidget(
                len(self.state_labels) - 1,
                label
            )

        self.timeline.set_processes(
            self.processes
        )

        self.slider.setMaximum(self.timeline.get_max_time())

        self.relations_table.update_relations(
            self.processes,
            RelationEngine
        )

    # ==================================================
    # СОХРАНЕНИЕ ОТНОШЕНИЙ В БД
    # ==================================================

    def save_relations(self):

        if not hasattr(
                self.db,
                "save_relation"
        ):
            return

        if hasattr(
                self.db,
                "clear_relations"
        ):
            self.db.clear_relations()

        for i in range(len(self.processes)):

            for j in range(i + 1,
                           len(self.processes)):

                relation = (
                    RelationEngine.detect_relation(
                        self.processes[i],
                        self.processes[j]
                    )
                )

                self.db.save_relation(
                    self.processes[i].id,
                    self.processes[j].id,
                    relation
                )

    # ==================================================
    # ПРОШЛЫЕ ПРОЦЕССЫ
    # ==================================================

    def show_past_processes(self):

        t = self.observer.get_time()

        result = []

        for p in self.processes:

            if p.end_max < t:
                result.append(p.name)

        QMessageBox.information(
            self,
            "Прошлые процессы",
            "\n".join(result)
            if result
            else "Нет процессов"
        )

    # ==================================================
    # АКТИВНЫЕ ПРОЦЕССЫ
    # ==================================================

    def show_active_processes(self):

        t = self.observer.get_time()

        result = []

        for p in self.processes:

            if p.start_min <= t <= p.end_max:
                result.append(p.name)

        QMessageBox.information(
            self,
            "Активные процессы",
            "\n".join(result)
            if result
            else "Нет процессов"
        )

    # ==================================================
    # БУДУЩИЕ ПРОЦЕССЫ
    # ==================================================

    def show_future_processes(self):

        t = self.observer.get_time()

        result = []

        for p in self.processes:

            if p.start_min > t:
                result.append(p.name)

        QMessageBox.information(
            self,
            "Будущие процессы",
            "\n".join(result)
            if result
            else "Нет процессов"
        )

    # ==================================================
    # ОБНОВЛЕНИЕ ИНТЕРФЕЙСА
    # ==================================================

    def update_interface(self, t):

        # синхронизация только через observer
        self.observer.set_time(t)

        # обновляем timeline
        self.timeline.set_observer_time(t)

        self.slider.blockSignals(True)
        self.slider.setValue(t)
        self.slider.blockSignals(False)

        self.time_label.setText(f"Позиция наблюдателя: {t}")

        for i, process in enumerate(self.processes):

            state = TemporalAnalyzer.analyze(process, t)
            process.current_state = state

            if i < len(self.state_labels):
                self.state_labels[i].setText(f"{process.name}: {state}")

        self.relations_table.update_relations(
            self.processes,
            RelationEngine
        )

        self.save_relations()