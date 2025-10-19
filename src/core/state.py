import random
from copy import deepcopy
from typing import Dict, List, Optional
from .entity import Course, Room, Student, CourseMeeting, Time


class State:

    DAYS = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
    MIN_HOUR = 7
    MAX_HOUR = 18  # last start time = 17, end time = 18

    def __init__(self, courses: List[Course], rooms: List[Room], students: List[Student]):

        self.courses = courses
        self.rooms = rooms
        self.students = students

        # Main state: list of all course meetings (Course, Time, Room)
        self.course_meetings: List[CourseMeeting] = []

        # List of all valid operations: (op_type, idx, target, duration)
        self.successors: List[tuple] = []

        # Lookup structure: schedule[room_code][day][hour] = List[Course]
        self.schedule: Dict[str, Dict[int, Dict[int, List[Course]]]] = {}
        self._initialize_schedule_structure()

        self._cached_objective: Optional[float] = None

    def _initialize_schedule_structure(self):

        for room in self.rooms:
            self.schedule[room.code] = {}
            for day in range(5):
                self.schedule[room.code][day] = {}
                for hour in range(self.MIN_HOUR, self.MAX_HOUR + 1):
                    self.schedule[room.code][day][hour] = []

    def _random_partition(self, n: int) -> List[int]:

        if n == 1:
            return [1]

        num_chunks = random.randint(1, n)
        if num_chunks == 1:
            return [n]

        cuts = sorted(random.sample(range(1, n), num_chunks - 1))
        chunks = []
        prev = 0
        for cut in cuts:
            chunks.append(cut - prev)
            prev = cut
        chunks.append(n - prev)

        return chunks

    def initial_state(self):

        self.course_meetings.clear()
        self._cached_objective = None

        for course in self.courses:
            chunks = self._random_partition(course.SKS)

            for chunk_size in chunks:
                room = random.choice(self.rooms)
                day = random.randint(0, 4)
                max_start = self.MAX_HOUR - chunk_size
                start_hour = random.randint(self.MIN_HOUR, max_start)

                for offset in range(chunk_size):
                    hour = start_hour + offset
                    time = Time(start=(day, hour), end=(day, hour + 1))
                    meeting = CourseMeeting(course, time, room)
                    self.course_meetings.append(meeting)

                    self.schedule[room.code][day][hour].append(course)

        self.get_all_successors()

    def _swap_meetings(self, idx1: int, idx2: int, duration: int):
        for offset in range(duration):
            m1 = self.course_meetings[idx1 + offset]
            m2 = self.course_meetings[idx2 + offset]

            self.schedule[m1.room.code][m1.time.start[0]][m1.time.start[1]].remove(m1.course)
            self.schedule[m2.room.code][m2.time.start[0]][m2.time.start[1]].remove(m2.course)

            m1.time, m2.time = m2.time, m1.time
            m1.room, m2.room = m2.room, m1.room

            self.schedule[m1.room.code][m1.time.start[0]][m1.time.start[1]].append(m1.course)
            self.schedule[m2.room.code][m2.time.start[0]][m2.time.start[1]].append(m2.course)

    def _move_meetings(self, idx: int, new_room: Room, new_day: int, new_start_hour: int, duration: int):
        for offset in range(duration):
            meeting = self.course_meetings[idx + offset]

            old_room_code = meeting.room.code
            old_day, old_hour = meeting.time.start
            self.schedule[old_room_code][old_day][old_hour].remove(meeting.course)

            new_hour = new_start_hour + offset
            meeting.room = new_room
            meeting.time = Time(start=(new_day, new_hour), end=(new_day, new_hour + 1))

            self.schedule[new_room.code][new_day][new_hour].append(meeting.course)

    def check_consecutive(self, meeting_idx: int) -> int:

        if meeting_idx >= len(self.course_meetings):
            return 0

        base_meeting = self.course_meetings[meeting_idx]
        course = base_meeting.course
        room = base_meeting.room
        day, start_hour = base_meeting.time.start

        consecutive_count = 1

        for offset in range(1, len(self.course_meetings) - meeting_idx):
            next_idx = meeting_idx + offset
            next_meeting = self.course_meetings[next_idx]

            if (next_meeting.course.code == course.code and
                next_meeting.room.code == room.code and
                next_meeting.time.start == (day, start_hour + consecutive_count)):
                consecutive_count += 1
            else:
                break

        return consecutive_count

    def _is_slot_available(self, room_code: str, day: int, start_hour: int, duration: int) -> bool:

        for hour in range(start_hour, start_hour + duration):
            if hour > self.MAX_HOUR:
                return False
            if len(self.schedule[room_code][day][hour]) > 0:
                return False

        return True

    def execute_operation(self, operation: tuple):

        op_type, idx, target, duration = operation

        if op_type == 'swap':
            self._swap_meetings(idx, target, duration)
        else:
            room, day, hour = target
            self._move_meetings(idx, room, day, hour, duration)

        self._cached_objective = None
        self.get_all_successors()

    def get_all_successors(self):

        self.successors.clear()

        if not self.course_meetings:
            return

        for i in range(len(self.course_meetings)):
            consecutive_count = self.check_consecutive(i)

            for duration in range(1, consecutive_count + 1):

                # Swap operations
                for j in range(len(self.course_meetings)):
                    if i != j:
                        target_consecutive = self.check_consecutive(j)
                        if target_consecutive >= duration:
                            self.successors.append(('swap', i, j, duration))

                # Move operations
                for room in self.rooms:
                    for day in range(5):
                        for hour in range(self.MIN_HOUR, self.MAX_HOUR + 1):
                            if self._is_slot_available(room.code, day, hour, duration):
                                self.successors.append(('move', i, (room, day, hour), duration))

    def get_random_neighbor(self) -> tuple:
        
        if not self.successors:
            raise ValueError("No valid operations")

        operation = random.choice(self.successors)
        self.successors.remove(operation)
        return operation
    
    def calculate_objective(self) -> float:

        if self._cached_objective is not None:
            return self._cached_objective

        student_conflicts_penalty = 0
        for student in self.students:
            student_meetings = [m for m in self.course_meetings
                               if m.course.code in student.courses]

            for i in range(len(student_meetings)):
                for j in range(i + 1, len(student_meetings)):
                    m1, m2 = student_meetings[i], student_meetings[j]

                    if m1.time.start[0] == m2.time.start[0]:
                        start1, end1 = m1.time.start[1], m1.time.end[1]
                        start2, end2 = m2.time.start[1], m2.time.end[1]

                        overlap_start = max(start1, start2)
                        overlap_end = min(end1, end2)

                        if overlap_start < overlap_end:
                            student_conflicts_penalty += (overlap_end - overlap_start)

        room_conflicts_penalty = 0
        priority_weights = {1: 1.75, 2: 1.5, 3: 1.25}

        for room_code in self.schedule:
            for day in self.schedule[room_code]:
                for hour in self.schedule[room_code][day]:
                    courses_at_slot = self.schedule[room_code][day][hour]

                    if len(courses_at_slot) > 1:
                        for student in self.students:
                            student_penalty = 0
                            for course in courses_at_slot:
                                if course.code in student.courses:
                                    idx = student.courses.index(course.code)
                                    priority = student.priorities[idx]
                                    weight = priority_weights.get(priority, 1)
                                    student_penalty += weight

                            room_conflicts_penalty += student_penalty

        capacity_overflow_penalty = 0
        for meeting in self.course_meetings:
            if meeting.course.studentCount > meeting.room.capacity:
                overflow = meeting.course.studentCount - meeting.room.capacity
                capacity_overflow_penalty += overflow * meeting.duration

        penalty = student_conflicts_penalty + room_conflicts_penalty + capacity_overflow_penalty

        self._cached_objective = penalty

        return penalty

    def copy(self) -> 'State':
        new_state = deepcopy(self)
        return new_state

    def visualize(self, room_code: Optional[str] = None):
        rooms_to_show = [room_code] if room_code else [r.code for r in self.rooms]

        for room in rooms_to_show:
            print(f"\nKode ruang: {room}")
            print(f"{'Jam':<5}", end='')
            for day_name in self.DAYS:
                print(f"{day_name:<15}", end='')
            print()

            for hour in range(self.MIN_HOUR, self.MAX_HOUR + 1):
                print(f"{hour:<5}", end='')
                for day in range(5):
                    courses = self.schedule[room][day][hour]
                    if courses:
                        codes = [c.code.split('_')[0] for c in courses]
                        display = ','.join(codes)
                        print(f"{display:<15}", end='')
                    else:
                        print(f"{'':15}", end='')
                print()

    def output_visualize_table(self, room_code: Optional[str] = None) -> List[Dict]:
        rooms_to_show = [room_code] if room_code else [r.code for r in self.rooms]

        table_data = []

        for room in rooms_to_show:
            table_data.append({
                'type': 'header',
                'room': room
            })
            
            for hour in range(self.MIN_HOUR, self.MAX_HOUR + 1):
                row = {'hour': hour}
                for day_idx, day_name in enumerate(self.DAYS):
                    courses = self.schedule[room][day_idx][hour]
                    if courses:
                        codes = [c.code.split('_')[0] for c in courses]
                        row[day_name] = ','.join(codes)
                    else:
                        row[day_name] = ''
                table_data.append(row)
        return table_data

    def __repr__(self):
        return f"State({len(self.course_meetings)} meetings, obj={self.calculate_objective():.2f})"