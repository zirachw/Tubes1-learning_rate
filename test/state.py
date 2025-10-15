from src.parse import Parse
from src.state import State

print("=" * 80)
print("STATE CLASS TEST - Class Scheduling Visualization")
print("=" * 80)
print()

print("Loading input data from input/input.json...")
file_path = "./input/input.json"
parser = Parse(file_path)
data = parser.loadJson()
courses, rooms, students = parser.parseAll(data)

print(f"[OK] Loaded {len(courses)} courses")
print(f"[OK] Loaded {len(rooms)} rooms")
print(f"[OK] Loaded {len(students)} students")
print()

print("-" * 80)
print("COURSES:")
print("-" * 80)
for course in courses:
    print(f"  {course.code}: {course.studentCount} students, {course.SKS} SKS")
print()

print("-" * 80)
print("ROOMS:")
print("-" * 80)
for room in rooms:
    print(f"  {room.code}: capacity {room.capacity}")
print()

print("-" * 80)
print("STUDENTS (sample):")
print("-" * 80)
for i, student in enumerate(students[:5]):
    print(f"  {student.NIM}: enrolled in {student.courses}")
    if i == 4 and len(students) > 5:
        print(f"  ... and {len(students) - 5} more students")
print()

print("-" * 80)
print("CREATING STATE...")
print("-" * 80)
state = State(courses, rooms, students, objective='student_conflicts')

print(f"[OK] Created {len(state.all_meetings)} course meetings")
print()

print("Meeting breakdown by course:")
course_meetings = {}
for meeting in state.all_meetings:
    code = meeting.course.code
    if code not in course_meetings:
        course_meetings[code] = []
    course_meetings[code].append(meeting)

for code, meetings in course_meetings.items():
    print(f"  {code}: {len(meetings)} meetings × 1h each = {len(meetings)}h total")
print()

print("-" * 80)
print("INITIALIZING RANDOM SCHEDULE...")
print("-" * 80)
state.initialize_random()
print(f"[OK] Randomly assigned {len(state.meeting_locations)} meetings")
print()

print("Sample scheduled slots:")
slots = state.get_all_scheduled_slots()
for i, slot in enumerate(slots[:5]):
    print(f"  {slot}")
    if i == 4 and len(slots) > 5:
        print(f"  ... and {len(slots) - 5} more slots")
print()

print("=" * 80)
print("SCHEDULE VISUALIZATION")
print("=" * 80)
for room in rooms:
    state.visualize(room.code)
print()

print("=" * 80)
print("TESTING NEIGHBOR GENERATION")
print("=" * 80)

print("\nOriginal state objective:", state.calculate_objective())
print("\nGenerating 3 random neighbors...\n")

for i in range(3):
    neighbor = state.get_random_neighbor()
    print(f"Neighbor {i+1} objective: {neighbor.calculate_objective()}")

print()

print("-" * 80)
print("TESTING SWAP OPERATION")
print("-" * 80)

if len(state.all_meetings) >= 2:
    meeting1 = state.all_meetings[0]
    meeting2 = state.all_meetings[1]

    loc1_before = state.meeting_locations.get(meeting1)
    loc2_before = state.meeting_locations.get(meeting2)

    print(f"\nBefore swap:")
    print(f"  {meeting1.course.code}[{meeting1.meeting_index}] at {loc1_before}")
    print(f"  {meeting2.course.code}[{meeting2.meeting_index}] at {loc2_before}")

    state_copy = state.copy()
    state_copy.swap_meetings(meeting1, meeting2)

    loc1_after = state_copy.meeting_locations.get(meeting1)
    loc2_after = state_copy.meeting_locations.get(meeting2)

    print(f"\nAfter swap:")
    print(f"  {meeting1.course.code}[{meeting1.meeting_index}] at {loc1_after}")
    print(f"  {meeting2.course.code}[{meeting2.meeting_index}] at {loc2_after}")

    print("\n[OK] Swap operation successful!")
print()

print("-" * 80)
print("TESTING MOVE TO EMPTY SLOT OPERATION")
print("-" * 80)

if len(state.all_meetings) >= 1:
    meeting = state.all_meetings[0]
    loc_before = state.meeting_locations.get(meeting)

    print(f"\nBefore move:")
    print(f"  {meeting.course.code}[{meeting.meeting_index}] at {loc_before}")

    state_copy = state.copy()

    moved = False
    for room in rooms:
        for day in range(5):
            for hour in range(7, 17):
                if state_copy.move_meeting_to_empty_slot(meeting, room.code, day, hour):
                    loc_after = state_copy.meeting_locations.get(meeting)
                    print(f"\nAfter move:")
                    print(f"  {meeting.course.code}[{meeting.meeting_index}] at {loc_after}")
                    print("\n[OK] Move operation successful!")
                    moved = True
                    break
            if moved:
                break
        if moved:
            break

    if not moved:
        print("\n[WARNING] Could not find empty slot (schedule might be full)")
print()

print("=" * 80)
print("TEST COMPLETED")
print("=" * 80)