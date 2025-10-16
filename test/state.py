from src.utils.parse import Parse
from src.core.state import State

print("=" * 80)
print("STATE_V2 CLASS TEST - New Architecture")
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
print("CREATING STATE...")
print("-" * 80)
state = State(courses, rooms, students, objective='student_conflicts')
print(f"[OK] Created state with {len(state.courses)} courses")
print()

print("-" * 80)
print("INITIALIZING RANDOM SCHEDULE...")
print("-" * 80)
state.initial_state()
print(f"[OK] Created {len(state.course_meetings)} course meetings")
print()

print("Meeting breakdown by course:")
course_meetings = {}
for meeting in state.course_meetings:
    code = meeting.course.code
    if code not in course_meetings:
        course_meetings[code] = []
    course_meetings[code].append(meeting)

for code, meetings in course_meetings.items():
    total_hours = sum(m.duration for m in meetings)
    durations = [m.duration for m in meetings]
    print(f"  {code}: {len(meetings)} meetings {durations} = {total_hours}h total")
print()

print("-" * 80)
print("TESTING OBJECTIVE CALCULATION...")
print("-" * 80)
objective_value = state.calculate_objective()
print(f"Objective function: {state.objective}")
print(f"Penalty: {objective_value}")
print(f"Cached objective (2nd call): {state.calculate_objective()}")
print()

print("=" * 80)
print("SCHEDULE VISUALIZATION")
print("=" * 80)
state.visualize()
print()

print("=" * 80)
print("TESTING SUCCESSOR OPERATIONS")
print("=" * 80)

print(f"\nOriginal state objective: {state.calculate_objective()}")
print(f"Number of valid operations: {len(state.successors)}")
print("\nTesting 5 random operations...\n")

for i in range(5):
    try:
        if not state.successors:
            print(f"Operation {i+1}: No more valid operations")
            break

        operation = state.get_random_neighbor()
        print(f"Operation {i+1}: {operation[0]} (removed from list)")

        # Execute on a copy to test
        test_state = state.copy()
        test_state.execute_operation(operation)
        print(f"  Result objective: {test_state.calculate_objective()}")
        print(f"  Remaining operations in original: {len(state.successors)}")
    except ValueError as e:
        print(f"Operation {i+1}: ERROR - {e}")

print()

print("-" * 80)
print("TESTING EXECUTE OPERATION")
print("-" * 80)
state_copy = state.copy()
print(f"Original objective: {state_copy.calculate_objective()}")
print(f"Operations before: {len(state_copy.successors)}")

if state_copy.successors:
    operation = state_copy.successors[0]
    print(f"\nExecuting operation: {operation[0]}")
    state_copy.execute_operation(operation)
    print(f"New objective: {state_copy.calculate_objective()}")
    print(f"Operations after (recomputed): {len(state_copy.successors)}")

print()

print("=" * 80)
print("TEST COMPLETED")
print("=" * 80)
