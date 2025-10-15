import json
from .entity import Course, Room, Student

class Parse:
    def __init__(self, filePath:str):
        self.filePath = filePath

    def changeFilePath(self, newFilePath: str):
        self.filePath = newFilePath

    def loadJson(self) -> any:
        f = open(self.filePath)
        return json.load(f)

    def parseCourse(self, data) -> list[Course] :
        courseList = data['kelas_mata_kuliah']

        courseOut = []
        for courseData in courseList:
            code = courseData['kode']
            studentCount = courseData['jumlah_mahasiswa']
            sks = courseData['sks']
            courseOut.append(Course(code, studentCount, sks))
        
        return courseOut

    def parseRoom(self, data) -> list[Room]:
        roomList = data['ruangan']

        roomOut = []
        for roomData in roomList:
            code = roomData['kode']
            quota = roomData['kuota']
            roomOut.append(Room(code,quota))
        
        return roomOut

    def parseStudent(self, data) -> list[Student]:
        studentList = data['mahasiswa']

        studentOut = []
        for studentData in studentList:
            nim = studentData['nim']
            courseList = studentData['daftar_mk']
            studentOut.append(Student(nim, courseList))
        
        return studentOut

    def parseAll(self, data) -> {list[Course], list[Room], list[Student]}:
        courses = self.parseCourse(data)
        rooms = self.parseRoom(data)
        students = self.parseStudent(data)

        return courses, rooms, students