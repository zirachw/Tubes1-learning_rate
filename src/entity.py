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