import sqlite3
import os
import sys


class DatabaseManager:

    def __init__(self):

        # Определение пути к базе данных
        if getattr(sys, 'frozen', False):
            # EXE режим (PyInstaller)
            base_dir = os.path.join(os.environ["APPDATA"], "TemporalProcessor")
        else:
            # режим разработки
            base_dir = os.path.dirname(os.path.abspath(__file__))

        os.makedirs(base_dir, exist_ok=True)

        db_path = os.path.join(base_dir, "temporal.db")

        print("BASE_DIR =", base_dir)
        print("DB_PATH =", db_path)
        print("DIR EXISTS =", os.path.exists(base_dir))
        print("DB EXISTS =", os.path.exists(db_path))

        # Подключение к SQLite базе данных
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

        # Создание таблиц при запуске системы
        self.create_tables()

        # Заполнение тестовыми данными, если база пустая
        self.seed_if_empty()

    def create_tables(self):

        # Таблица процессов (темпоральные интервалы)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS processes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            start_min INTEGER,
            start_max INTEGER,
            end_min INTEGER,
            end_max INTEGER,
            temporal_type TEXT,
            color TEXT,
            description TEXT
        )
        """)

        # Таблица временных отношений между процессами
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS temporal_relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            process1_id INTEGER,
            process2_id INTEGER,
            relation_type TEXT
        )
        """)

        self.connection.commit()

    def save_relation(
            self,
            process1_id,
            process2_id,
            relation_type
    ):
        
        # Сохранение отношения между двумя процессами
        self.cursor.execute("""
        INSERT INTO temporal_relations(
            process1_id,
            process2_id,
            relation_type
        )
        VALUES (?, ?, ?)
        """, (
            process1_id,
            process2_id,
            relation_type
        ))

        self.connection.commit()

    def clear_relations(self):

        # Очистка таблицы отношений
        self.cursor.execute(
            "DELETE FROM temporal_relations"
        )

        self.connection.commit()

    def get_relations(self):

        # Получение всех отношений
        self.cursor.execute("""
        SELECT *
        FROM temporal_relations
        """)

        return self.cursor.fetchall()

    def add_process(self,
                    name,
                    smin,
                    smax,
                    emin,
                    emax,
                    ttype,
                    color,
                    desc):
        
        # Добавление процесса в базу данных
        self.cursor.execute("""
        INSERT INTO processes(
            name,
            start_min,
            start_max,
            end_min,
            end_max,
            temporal_type,
            color,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            smin,
            smax,
            emin,
            emax,
            ttype,
            color,
            desc
        ))

        self.connection.commit()

    def get_processes(self):
        
        # Получение всех процессов
        self.cursor.execute(
            "SELECT * FROM processes"
        )

        return self.cursor.fetchall()

    def seed_if_empty(self):

        # Инициализация тестовых данных при пустой базе
        self.cursor.execute(
            "SELECT COUNT(*) FROM processes"
        )

        count = self.cursor.fetchone()[0]

        if count > 0:
            return

        # Набор тестовых процессов для демонстрации модели времени
        processes = [

            # Базовый процесс
            ("P1", 10, 10, 90, 90,
            "точный", "#ff6666", "Базовый"),

            # rts
            # после P1 с паузой
            ("P2", 95, 95, 120, 120,
            "точный", "#66ccff", "rts"),

            # rtes
            # пересекается с P1
            ("P3", 50, 50, 110, 110,
            "точный", "#66ff99", "rtes"),

            # rtel
            # вложен в P1, начало совпадает
            ("P4", 10, 10, 40, 40,
            "точный", "#ffaa00", "rtel"),

            # rter
            # вложен в P1, конец совпадает
            ("P5", 60, 60, 90, 90,
            "точный", "#cc66ff", "rter")

        ]

        for p in processes:
            self.add_process(*p)