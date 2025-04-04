import random
from config.algorithm_config import shifts_per_day, population_size, max_doctors_per_shift
import config.globals as g


def create_initial_population(doctors, daysInMonth):
    population = []

    temp_list_12 = [
        doctor.code
        for doctor in doctors
        if g.code_to_duration.get(doctor.code) == "12"
        for _ in range(doctor.shift_count)
    ]

    temp_list_24 = [
        doctor.code
        for doctor in doctors
        if g.code_to_duration.get(doctor.code) == "24"
        for _ in range(doctor.shift_count // 2)
    ]

    for _ in range(population_size):
        schedule = [[[] for _ in range(shifts_per_day)] for _ in range(daysInMonth)]

        random.shuffle(temp_list_12)
        random.shuffle(temp_list_24)

        for index, doctor_code in enumerate(temp_list_24):
            day = index % daysInMonth
            schedule[day][0].append(doctor_code)
            schedule[day][1].append(doctor_code)

        for index, doctor_code in enumerate(temp_list_12):
            day = (index // shifts_per_day) % daysInMonth
            shift_type = index % shifts_per_day
            schedule[day][shift_type].append(doctor_code)

        population.append(schedule)

    return population

