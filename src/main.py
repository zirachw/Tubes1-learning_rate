from parse import Parse


def main():
    filePath = "./input/input.json"
    parse = Parse(filePath)
    data = parse.loadJson()
    courses, rooms, students = parse.parseAll(data)

    # Test Print
    print(courses[0].code)
    print(rooms[0].code)
    print(students[0].NIM)
    

if __name__ == "__main__":
    main() 