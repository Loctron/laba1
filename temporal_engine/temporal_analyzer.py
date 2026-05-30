class TemporalAnalyzer:

    @staticmethod
    # Анализ состояния процесса относительно наблюдателя
    def analyze(process, observer_time):

        if process.temporal_type == "нечёткий":

            if observer_time < process.start_min:
                return "будущий"

            if observer_time > process.end_max:
                return "прошлый"

            return "неопределённый"

        if process.temporal_type == "точечный":

            if observer_time < process.start_min:
                return "будущий"

            if observer_time > process.start_min:
                return "прошлый"

            return "происходит"

        if observer_time < process.start_min:
            return "будущий"

        if observer_time > process.end_max:
            return "прошлый"

        return "происходит"