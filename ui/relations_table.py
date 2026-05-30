from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem
)


RELATION_DESCRIPTIONS = {

    "rts":
        "Последовательны с паузой",

    "rtsn":
        "Последовательны без паузы",

    "rtes":
        "Пересекаются",

    "rtel":
        "Вложенные с примыканием к началу",

    "rter":
        "Вложенные с примыканием к окончанию",

    "rte":
        "Вложенные без примыканий",

    "rtU":
        "Несравнимы",

    "эквивалентны":
        "Полностью совпадают"
}


class RelationsTable(QTableWidget):

    def __init__(self):

        super().__init__()

    def update_relations(
            self,
            processes,
            relation_engine
    ):

        size = len(processes)

        self.setRowCount(size)
        self.setColumnCount(size)

        headers = [
            p.name for p in processes
        ]

        self.setHorizontalHeaderLabels(headers)
        self.setVerticalHeaderLabels(headers)

        for row in range(size):

            for col in range(size):

                if row == col:

                    self.setItem(
                        row,
                        col,
                        QTableWidgetItem("-")
                    )

                    continue

                relation = relation_engine.detect_relation(
                    processes[row],
                    processes[col]
                )

                description = RELATION_DESCRIPTIONS[
                    relation
                ]

                item = QTableWidgetItem(
                    f"{relation}\n{description}"
                )

                self.setItem(
                    row,
                    col,
                    item
                )

        self.resizeColumnsToContents()
        self.resizeRowsToContents()