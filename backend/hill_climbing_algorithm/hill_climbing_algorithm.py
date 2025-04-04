import copy
import os
from hill_climbing_algorithm.initial_population import create_initial_population
from hill_climbing_algorithm.fitness.fitness_methods import calculate_fitness
from config.algorithm_config import (
    doctor_swap_rate,
    doctor_slide_rate,
    shift_swap_rate,
    day_swap_rate,
    doctor24_swap_rate,
    doctor24_slide_rate,
)
from hill_climbing_algorithm.mutation.mutation_methods import mutate_schedule
import config.globals as g

db_mode = os.getenv("DB_MODE")

if db_mode == "local":
    from services import database_service_postgres as db
elif db_mode == "desktop":
    from services import database_service_sqlite as db

def run_hill_climbing(doctors, schedule_data_id):
    print("Running hill climbing algorithm...")
    g.shift_areas_data = db.get_shift_areas()
    schedule_data = db.get_schedule_data_by_id(schedule_data_id)

    g.code_to_duration = {
        doc["code"]: doc["shift_duration"]
        for doc in schedule_data["data"]
        if "shift_duration" in doc
    }

    daysInMonth = schedule_data.get("days_in_month")
    first_day = schedule_data.get("first_day", "Pazartesi") 
    g.week_start_day = g.week_days_map.get(first_day, 1)  
    max_generations = g.MAX_GENERATIONS
    population = create_initial_population(doctors, daysInMonth)
    for generation in range(max_generations):
        doc_rate, slide_rate, shift_rate, day_rate,doc24_slide_rate, doc24_swap_rate  = get_swap_rates(generation)
        for idx in range(len(population)):
            original = population[idx]
            original_fitness = calculate_fitness(original, doctors, schedule_data_id=None, log=False)
            mutated = mutate_schedule(
                copy.deepcopy(original), doc_rate, slide_rate, shift_rate, day_rate, doc24_slide_rate, doc24_swap_rate
            )
            mutated_fitness = calculate_fitness(mutated, doctors, schedule_data_id=None, log=False)
            if mutated_fitness > original_fitness:
                population[idx] = mutated

                with open("generation_log.txt", "a") as log_file:
                    log_file.write(f"Generation {generation + 1}:\n")
                    log_file.write(f"  Individual {idx + 1}:\n")
                    for day_index, day in enumerate(mutated, start=1):
                        log_file.write(f"    Day {day_index}: {day}\n")
                    log_file.write(
                        f"  Fitness Improved from {original_fitness} to {mutated_fitness}\n"
                    )
            else:
                with open("generation_log.txt", "a") as log_file:
                    log_file.write(f"Generation {generation + 1}:\n")
                    log_file.write(f"  Individual {idx + 1}:\n")
                    log_file.write(f"  Fitness Remained at {original_fitness}\n")
    return process_population(population, doctors, schedule_data_id)


def process_population(population, doctors, schedule_data_id):
    processed_population = []

    for idx in range(len(population)):
        # Schedule'ı işle
        population[idx] = sort_doctors_in_shifts(population[idx])
        # Schedule'ı veritabanına kaydet
        schedule_id = db.add_schedule(schedule_data_id, population[idx])
        # Fitness puanını hesapla
        fitness_score = calculate_fitness(population[idx], doctors, schedule_id, log=True)
        db.add_fitness_score(schedule_id, fitness_score)
        # Schedule ve fitness puanını birlikte sakla
        processed_population.append((population[idx], fitness_score))
        
    # Log dosyasına yaz
    # with open("generation_log.txt", "a") as log_file:
    #     for idx, (schedule, fitness_score) in enumerate(processed_population):
    #         log_file.write(f"\nIndividual {idx + 1} Final Schedule:\n")
    #         for day_index, day in enumerate(schedule, start=1):
    #             log_file.write(f"  Day {day_index}: {day}\n")
    #         log_file.write(f"  Fitness Score: {fitness_score}\n")

    return processed_population, schedule_id


def get_swap_rates(generation):
    if generation < 10000:
        return doctor_swap_rate, doctor_slide_rate, shift_swap_rate, day_swap_rate, doctor24_swap_rate, doctor24_slide_rate
    else:
        return 0.3, 0.2, 0, 0.1, 0.2, 0.2


def sort_doctors_in_shifts(schedule):
    for day in schedule:
        for shift in day:
            shift.sort()
    return schedule
