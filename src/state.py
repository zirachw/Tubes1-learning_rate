import random
from typing import Dict, List, Optional, Tuple
from .entity import Course, Room, Student, CourseMeeting, ScheduleSlot

class State:

    DAYS = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
    MIN_HOUR = 7
    MAX_HOUR = 17

    def __init__(self, courses: List[Course], rooms: List[Room], students: List[Student],
                 objective: str = 'student_conflicts'):

        self.courses = courses
        self.rooms = rooms
        self.students = students
        self.objective = objective

        self.all_meetings: List[CourseMeeting] = self._create_all_meetings()

        # Schedule: schedule[room_code][day][hour] = List[CourseMeeting] (can have overlaps)
        self.schedule: Dict[str, Dict[int, Dict[int, List[CourseMeeting]]]] = {}
        self._initialize_schedule_structure()

        # Mapping for quick lookup: meeting -> (room, day, hour)
        self.meeting_locations: Dict[CourseMeeting, Tuple[str, int, int]] = {}
        self._cached_objective: Optional[float] = None

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
    
    def _create_all_meetings(self) -> List[CourseMeeting]:
        """
        Create meetings by randomly partitioning each course's SKS into chunks.

        Example for 4 SKS: could be [4], [3,1], [2,2], [1,3], [2,1,1], [1,2,1], [1,1,2], [1,1,1,1], etc.
        """

        meetings = []
        for course in self.courses:
            chunks = self._random_partition(course.SKS)

            for i, duration in enumerate(chunks):
                meetings.append(CourseMeeting(course, i, duration))

        return meetings

    def _initialize_schedule_structure(self):
        for room in self.rooms:
            self.schedule[room.code] = {}
            for day in range(5):
                self.schedule[room.code][day] = {}
                for hour in range(self.MIN_HOUR, self.MAX_HOUR + 1):
                    self.schedule[room.code][day][hour] = []

    def initialize_random(self):
        self.meeting_locations.clear()
        self._cached_objective = None

        for meeting in self.all_meetings:
            room = random.choice(self.rooms)
            day = random.randint(0, 4)
            start_hour = random.randint(self.MIN_HOUR, self.MAX_HOUR)

            self._place_meeting(meeting, room.code, day, start_hour)

    def _place_meeting(self, meeting: CourseMeeting, room_code: str, day: int, start_hour: int):
        """Place a meeting in the schedule (appends to list, allows overlaps)."""

        for hour in range(start_hour, start_hour + meeting.duration):
            if hour <= self.MAX_HOUR:
                self.schedule[room_code][day][hour].append(meeting)

        self.meeting_locations[meeting] = (room_code, day, start_hour)
        self._cached_objective = None

    def _remove_meeting(self, meeting: CourseMeeting):
        """Remove a meeting from the schedule (removes from list)."""

        if meeting not in self.meeting_locations:
            return

        room_code, day, start_hour = self.meeting_locations[meeting]

        for hour in range(start_hour, start_hour + meeting.duration):
            if hour <= self.MAX_HOUR:
                if meeting in self.schedule[room_code][day][hour]:
                    self.schedule[room_code][day][hour].remove(meeting)

        del self.meeting_locations[meeting]
        self._cached_objective = None

    def swap_meetings(self, meeting1: CourseMeeting, meeting2: CourseMeeting):

        room1, day1, hour1 = self.meeting_locations[meeting1]
        room2, day2, hour2 = self.meeting_locations[meeting2]

        self._remove_meeting(meeting1)
        self._remove_meeting(meeting2)

        self._place_meeting(meeting1, room2, day2, hour2)
        self._place_meeting(meeting2, room1, day1, hour1)
    
    def move_meeting_to_empty_slot(self, meeting: CourseMeeting,
                                    target_room_code: str, target_day: int, target_hour: int) -> bool:

        self._remove_meeting(meeting)
        self._place_meeting(meeting, target_room_code, target_day, target_hour)

        return True

    def get_random_neighbor(self) -> 'State':
        """
        Generate a random neighbor state using one of the allowed moves:
        1. Swap two meetings
        2. Move a meeting to an empty slot

        Returns a new State object.
        """

        neighbor = self.copy()
        neighbor_type = random.choice(['swap', 'move'])

        meeting = random.choice(neighbor.all_meetings)

        if neighbor_type == 'swap':
            same_duration_meetings = [m for m in neighbor.all_meetings
                                      if m != meeting and m.duration == meeting.duration]

            if same_duration_meetings:
                # Swap succeeded
                meeting2 = random.choice(same_duration_meetings)
                neighbor.swap_meetings(meeting, meeting2)
                return neighbor

            # Swap failed, try MOVE
            empty_slots = []
            for room in neighbor.rooms:
                for day in range(5):
                    for hour in range(self.MIN_HOUR, self.MAX_HOUR + 1):
                        if neighbor._is_slot_available(room.code, day, hour, meeting.duration):
                            empty_slots.append((room.code, day, hour))

            if empty_slots:
                target_room, target_day, target_hour = random.choice(empty_slots)
                neighbor.move_meeting_to_empty_slot(meeting, target_room, target_day, target_hour)
                return neighbor

        elif neighbor_type == 'move':
            empty_slots = []
            for room in neighbor.rooms:
                for day in range(5):
                    for hour in range(self.MIN_HOUR, self.MAX_HOUR + 1):
                        if neighbor._is_slot_available(room.code, day, hour, meeting.duration):
                            empty_slots.append((room.code, day, hour))

            if empty_slots:
                # Move succeeded
                target_room, target_day, target_hour = random.choice(empty_slots)
                neighbor.move_meeting_to_empty_slot(meeting, target_room, target_day, target_hour)
                return neighbor

            # Move failed, try SWAP
            same_duration_meetings = [m for m in neighbor.all_meetings
                                      if m != meeting and m.duration == meeting.duration]
            if same_duration_meetings:
                meeting2 = random.choice(same_duration_meetings)
                neighbor.swap_meetings(meeting, meeting2)
                return neighbor

        else:
            # Both moves failed
            raise ValueError(f"Cannot generate neighbor for meeting {meeting}: no valid moves available")

    def get_all_scheduled_slots(self) -> List[ScheduleSlot]:

        slots = []
        processed = set()

        for meeting, (room_code, day, start_hour) in self.meeting_locations.items():
            if meeting not in processed:
                room = next(r for r in self.rooms if r.code == room_code)
                slots.append(ScheduleSlot(meeting, room, day, start_hour))
                processed.add(meeting)

        return slots
    
    def calculate_objective(self) -> float:

        if self._cached_objective is not None:
            return self._cached_objective

        penalty = 0.0

        if self.objective == 'student_conflicts':
            slots = self.get_all_scheduled_slots()

            for student in self.students:
                student_slots = [slot for slot in slots if slot.meeting.course.code in student.courses]

                for i in range(len(student_slots)):
                    for j in range(i + 1, len(student_slots)):

                        if student_slots[i].overlaps_with(student_slots[j]):
                            overlap_start = max(student_slots[i].start_hour, student_slots[j].start_hour)
                            overlap_end = min(student_slots[i].get_end_hour(), student_slots[j].get_end_hour())
                            penalty += (overlap_end - overlap_start)

        elif self.objective == 'room_conflicts':
            priority_weights = {1: 1.75, 2: 1.5, 3: 1.25}
            slots = self.get_all_scheduled_slots()

            for i in range(len(slots)):
                for j in range(i + 1, len(slots)):
                    slot_i, slot_j = slots[i], slots[j]

                    if slot_i.room.code == slot_j.room.code and slot_i.overlaps_with(slot_j):
                        overlap_start = max(slot_i.start_hour, slot_j.start_hour)
                        overlap_end = min(slot_i.get_end_hour(), slot_j.get_end_hour())
                        overlap_hours = overlap_end - overlap_start

                        for student in self.students:
                            student_penalty = 0

                            if slot_i.meeting.course.code in student.courses:
                                idx = student.courses.index(slot_i.meeting.course.code)
                                priority = idx + 1 if idx < len(student.courses) else 999
                                weight = priority_weights.get(priority, 1.0)
                                student_penalty += weight

                            if slot_j.meeting.course.code in student.courses:
                                idx = student.courses.index(slot_j.meeting.course.code)
                                priority = idx + 1 if idx < len(student.courses) else 999
                                weight = priority_weights.get(priority, 1.0)
                                student_penalty += weight

                            penalty += overlap_hours * student_penalty

        elif self.objective == 'capacity_overflow':
            slots = self.get_all_scheduled_slots()

            for slot in slots:
                student_count = slot.meeting.course.studentCount
                room_capacity = slot.room.capacity

                if student_count > room_capacity:
                    overflow = student_count - room_capacity
                    penalty += overflow * slot.meeting.duration

        self._cached_objective = penalty
        return penalty

    def copy(self) -> 'State':
        new_state = State(self.courses, self.rooms, self.students, self.objective)
        new_state.all_meetings = self.all_meetings.copy()

        new_state.schedule = {}
        for room_code, days_dict in self.schedule.items():
            new_state.schedule[room_code] = {}
            for day, hours_dict in days_dict.items():
                new_state.schedule[room_code][day] = hours_dict.copy()

        new_state.meeting_locations = self.meeting_locations.copy()
        new_state._cached_objective = self._cached_objective

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
                    meetings = self.schedule[room][day][hour]
                    if meetings:
                        codes = [m.course.code.split('_')[0] for m in meetings]
                        display = ','.join(codes)
                        print(f"{display:<15}", end='')
                    else:
                        print(f"{'':15}", end='')
                print()

    def __repr__(self):
        return f"State({len(self.all_meetings)} meetings, obj={self.calculate_objective():.2f})"