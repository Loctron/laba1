class ObserverModel:

    def __init__(self, t=0):
        self._time = t

    def set_time(self, t):
        self._time = t

    def get_time(self):
        return self._time