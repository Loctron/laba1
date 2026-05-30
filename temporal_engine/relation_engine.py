class RelationEngine:

    @staticmethod
    def get_bounds(p):

        # Получение временных границ процесса
        return (
            p.start_min,
            p.end_max
        )

    @staticmethod
    def detect_relation(a, b):
        # Определение отношения между двумя процессами

        a_s, a_e = RelationEngine.get_bounds(a)
        b_s, b_e = RelationEngine.get_bounds(b)

        # Последовательность с паузой
        if a_e < b_s:
            return "rts"

        # Последовательность без паузы
        if a_e == b_s:
            return "rtsn"

        # Вложение с совпадением начала
        if a_s == b_s and a_e < b_e:
            return "rtel"

        # Вложение с совпадением конца
        if a_s > b_s and a_e == b_e:
            return "rter"

        # Полное вложение
        if (
                a_s > b_s and
                a_e < b_e
        ):
            return "rte"

        # Пересечение интервалов
        if (
                a_s < b_s < a_e < b_e
        ):

            return "rtes"

        if (
                b_s < a_s < b_e < a_e
        ):

            return "rtes"

        # Несравнимые процессы
        return "rtU"