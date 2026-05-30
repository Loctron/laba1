class ProcessModel:

    def __init__(self, process_id, name,
                 start_min, start_max,
                 end_min, end_max,
                 temporal_type,
                 color,
                 description):

        self.id = process_id
        self.name = name

        self.start_min = start_min
        self.start_max = start_max
        self.end_min = end_min
        self.end_max = end_max

        self.temporal_type = temporal_type
        self.color = color
        self.description = description

        self.current_state = "future"

    def average_start(self):
        return (self.start_min + self.start_max) / 2

    def average_end(self):
        return (self.end_min + self.end_max) / 2

    def fuzzy_center(self):
        return (self.start_min + self.start_max +
                self.end_min + self.end_max) / 4