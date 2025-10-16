class Time:
    def __init__(self, start: tuple[str, int], end: tuple[str, int]):
        self.start = start  # (hari mulai,   jam mulai)
        self.end = end      # (hari selesai, jam selesai)

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

    def __init__(self, course: Course, time: Time, room: Room):
        self.course = course
        self.time = time
        self.room = room

    @property
    def duration(self) -> int:
        return self.time.end[1] - self.time.start[1]