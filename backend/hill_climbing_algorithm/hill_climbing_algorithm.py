import copy
from genetic_algorithm.initial_population import create_initial_population
from genetic_algorithm.fitness.fitness_methods import calculate_fitness
from config.algorithm_config import (
    doctor_swap_rate,
    doctor_slide_rate,
    shift_swap_rate,
    day_swap_rate,
)
from genetic_algorithm.mutation.mutation_methods import mutate_schedule
from services.database_service import get_shift_areas, add_schedule, add_fitness_score, get_schedule_data_by_id
import config.globals as g

def run_hill_climbing(doctors, schedule_data_id):
    g.shift_areas_data = get_shift_areas()
    schedule_data = get_schedule_data_by_id(schedule_data_id)
    daysInMonth = schedule_data.get("days_in_month")
    first_day = schedule_data.get("first_day", "Pazartesi") 
    g.week_start_day = g.week_days_map.get(first_day, 1)  
    max_generations = g.MAX_GENERATIONS

    population = create_initial_population(doctors, daysInMonth)
    for generation in range(max_generations):
        doc_rate, slide_rate, shift_rate, day_rate = get_swap_rates(generation)

        for idx in range(len(population)):
            original = population[idx]
            original_fitness = calculate_fitness(original, doctors, schedule_data_id=None, log=False)
            mutated = mutate_schedule(
                copy.deepcopy(original), doc_rate, slide_rate, shift_rate, day_rate
            )
            mutated_fitness = calculate_fitness(mutated, doctors, schedule_data_id=None, log=False)
            if mutated_fitness > original_fitness:
                population[idx] = mutated
                # with open("generation_log.txt", "a") as log_file:
                #     log_file.write(f"Generation {generation + 1}:\n")
                #     log_file.write(f"  Individual {idx + 1}:\n")
                #     for day_index, day in enumerate(mutated, start=1):
                #         log_file.write(f"    Day {day_index}: {day}\n")
                #     log_file.write(
                #         f"  Fitness Improved from {original_fitness} to {mutated_fitness}\n"
                #     )
            # else:
            #     with open("generation_log.txt", "a") as log_file:
            #         log_file.write(f"Generation {generation + 1}:\n")
            #         log_file.write(f"  Individual {idx + 1}:\n")
            #         log_file.write(f"  Fitness Remained at {original_fitness}\n")

    return process_population(population, doctors, schedule_data_id)


def process_population(population, doctors, schedule_data_id):
    processed_population = []

    for idx in range(len(population)):
        # Schedule'ı işle
        population[idx] = sort_doctors_in_shifts(population[idx])
        # Schedule'ı veritabanına kaydet
        schedule_id = add_schedule(schedule_data_id, population[idx])
        # Fitness puanını hesapla
        fitness_score = calculate_fitness(population[idx], doctors, schedule_id, log=True)
        add_fitness_score(schedule_id, fitness_score)
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
    if generation < 1000:
        return doctor_swap_rate, doctor_slide_rate, shift_swap_rate, day_swap_rate
    elif generation < 2000:
        return 0.4, 0.4, 0.1, 0.1
    else:
        return 0.8, 0.2, 0, 0


def sort_doctors_in_shifts(schedule):
    for day in schedule:
        for shift in day:
            shift.sort()
    return schedule
