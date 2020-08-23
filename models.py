from app import db

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    start = db.Column(db.String())
    end = db.Column(db.String())
    duration = db.Column(db.String())

    def __init__(self, name, start, end, duration):
        assert name, "name of task not specified"
        self.name = name
        self.start = start
        self.end = end

        if start and not end:
            self.end = add_time(start, duration)

        if duration:
            self.duration = duration
        else:
            start_hour, start_min = map(int, start.split(':'))
            end_hour, end_min = map(int, end.split(':'))

            assert end_hour >= start_hour, end + '>' + start
            if end_hour == start_hour:
                assert end_min > start_min, end + '>' + start
            if end_min < start_min:
                duration_min = end_min + 60 - start_min
                duration_hour = end_hour - 1 - start_hour
            else:
                duration_min = end_min - start_min
                duration_hour = end_hour - start_hour
            self.duration = str(duration_hour) + ':' + "{0:0=2d}".format(duration_min)

    def __repr__(self):
        return '<id {}>'.format(self.id)

def add_time(start, duration):
    start_hour, start_min = map(int, start.split(':'))
    dur_hrs, dur_mins = map(int, duration.split(':'))
    if start_min + dur_mins >= 60:
        end_min = start_min + dur_mins - 60
        end_hour = start_hour + dur_hrs + 1
    else:
        end_min = start_min + dur_mins
        end_hour = start_hour + dur_hrs
    return str(end_hour) + ':' + "{0:0=2d}".format(end_min)

if __name__ == '__main__':
    # testing
    test = Task('test', '9:00', None, '2:00')
    print(test.end)


# class Day:
#     def __init__(self):
#         self.tasks = []
#         self.fixed_tasks = []
#
#     def set_start_end(self, start, end):
#         self.start = start
#         self.end = end
#
#     def add_task(self, task):
#         if not task.start:
#             self.tasks.append(task)
#         else:
#             self.fixed_tasks.append(task)
#
#     def sort_fixed_tasks(self):
#         self.fixed_tasks.sort(key=lambda task: task.start)
#
#     def fixed_tasks_overlap(self):
#         if len(self.fixed_tasks) < 2:
#             return False
#         prev_end = self.fixed_tasks[0].end
#         for task in self.fixed_tasks[1:]:
#             if prev_end > task.start:
#                 return True
#             prev_end = task.end
#
#     def plan(self):
#         self.sort_fixed_tasks()
#         assert not self.fixed_tasks_overlap(), 'fixed tasks overlap'
#
#     def has_lunch(self):
#         for task in self.fixed_tasks:
#             if task.name == 'lunch':
#                 return True
#         return False
