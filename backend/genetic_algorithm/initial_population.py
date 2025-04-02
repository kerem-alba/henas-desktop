import random
from config.algorithm_config import shifts_per_day, population_size


def create_initial_population(doctors, daysInMonth):
    population = []

    temp_list = [doctor.code for doctor in doctors for _ in range(doctor.shift_count)]
    random.shuffle(temp_list)

    for _ in range(population_size):
        schedule = [[[] for _ in range(shifts_per_day)] for _ in range(daysInMonth)]

        random.shuffle(temp_list)

        for index, doctor_code in enumerate(temp_list):
            day = (index // shifts_per_day) % daysInMonth
            shift_type = index % shifts_per_day
            schedule[day][shift_type].append(doctor_code)

        population.append(schedule)

    return population
