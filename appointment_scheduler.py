def is_time_overlap(time1, time2):
    return max(time1[0], time2[0]) < min(time1[1], time2[1])

def schedule_appointments(doctors, patients, rooms):
    doctor_schedule = {doc['name']: [] for doc in doctors}
    room_schedule = {room: [] for room in rooms}
    appointments = []

    def backtrack(patient_index):
        if patient_index == len(patients):
            return True

        patient = patients[patient_index]
        preferred_doctor = patient['preferred_doctor']
        preferred_time = patient['preferred_time']
        doctor = next(doc for doc in doctors if doc['name'] == preferred_doctor)

        for available_time in doctor['available_hours']:
            if not is_time_overlap(preferred_time, available_time):
                continue

            if any(is_time_overlap(preferred_time, appt['time']) for appt in doctor_schedule[doctor['name']]):
                continue

            for room in rooms:
                if any(is_time_overlap(preferred_time, appt['time']) for appt in room_schedule[room]):
                    continue

                appointment = {
                    'doctor': doctor['name'],
                    'patient': patient['name'],
                    'time': preferred_time,
                    'room': room,
                }
                doctor_schedule[doctor['name']].append(appointment)
                room_schedule[room].append(appointment)
                appointments.append(appointment)

                if backtrack(patient_index + 1):
                    return True

                doctor_schedule[doctor['name']].remove(appointment)
                room_schedule[room].remove(appointment)
                appointments.pop()

        return False

    if not backtrack(0):
        print("No valid schedule found.")
        return None

    return appointments

doctors = [
    {'name': 'Dr. A', 'available_hours': [(9, 12), (14, 17)]},
    {'name': 'Dr. B', 'available_hours': [(13, 17)]},
    {'name': 'Dr. C', 'available_hours': [(9, 13)]},
]

patients = [
    {'name': 'Patient 1', 'preferred_doctor': 'Dr. A', 'preferred_time': (10, 11)},
    {'name': 'Patient 2', 'preferred_doctor': 'Dr. B', 'preferred_time': (13, 14)},
    {'name': 'Patient 3', 'preferred_doctor': 'Dr. A', 'preferred_time': (14, 15)},
    {'name': 'Patient 4', 'preferred_doctor': 'Dr. C', 'preferred_time': (9, 10)},
]

rooms = [1, 2]

appointments = schedule_appointments(doctors, patients, rooms)

if appointments:
    print("Scheduled Appointments:")
    for appt in appointments:
        print(appt)
