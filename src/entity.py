class Time:
    def __init__(self, day: str, hour: int):
        self.day = day
        self.hour = hour

class Course:
    def __init__(self, code: str, studentCount: int, SKS: int):
        self.code = code
        self.studentCount = studentCount
        self.SKS = SKS

class Room:
    def __init__(self, code: str, capacity: int):
        self.code = code
        self.capacity = capacity

class Student:
    def __init__(self, NIM: str, courses: list[Course]):
        self.NIM = NIM
        self.courses = courses

class CourseMeeting:
    def __init__(self, course: Course, meeting_index: int, duration: int):
        self.course = course
        self.meeting_index = meeting_index
        self.duration = duration

    def __repr__(self):
        return f"CourseMeeting({self.course.code}, idx={self.meeting_index}, dur={self.duration}h)"

    def __eq__(self, other):
        if not isinstance(other, CourseMeeting):
            return False
        return (self.course.code == other.course.code and
                self.meeting_index == other.meeting_index)

    def __hash__(self):
        return hash((self.course.code, self.meeting_index))

class ScheduleSlot:
    def __init__(self, meeting: CourseMeeting, room: Room, day: int, start_hour: int):
        self.meeting = meeting
        self.room = room
        self.day = day
        self.start_hour = start_hour

    def get_end_hour(self) -> int:
        return self.start_hour + self.meeting.duration

    def overlaps_with(self, other: 'ScheduleSlot') -> bool:
        if self.day != other.day:
            return False

        return not (self.get_end_hour() <= other.start_hour or
                   other.get_end_hour() <= self.start_hour)

    def __repr__(self):
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
        return f"Slot({self.meeting.course.code}, {days[self.day]} {self.start_hour}-{self.get_end_hour()}, {self.room.code})"