from datetime import datetime, timedelta


class Task:
    # start = datetime class or (hour, minute)
    # duration = minutes
    def __init__(self, prio=None, start=None, end=None, duration=0, type=''):
        self.prio = prio
        if start:
            self.set_start(start)
            if end:
                self.set_end(end)
            else:
                self.end = self.start + timedelta(minutes=duration)
        else:
            self.duration = duration
        self.type = type

    def get_prio(self):
        return self.prio

    def get_duration(self):
        return self.duration

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def set_start(self, start):
        if isinstance(start, datetime):
            self.start = start
        else:
            today = datetime.today()
            self.start = datetime(today.year, today.month, today.day, start[0], start[1])

    def set_end(self, end):
        if isinstance(end, datetime):
            self.end = end
        else:
            today = datetime.today()
            self.end = datetime(today.year, today.month, today.day, end[0], end[1])


if __name__ == '__main__':
    # testing
    test1 = Task(start=(9, 0), duration=120)
    test2 = Task(start=(9, 0), end=(14, 0))
    print(test2.start)
    print(test2.end)
