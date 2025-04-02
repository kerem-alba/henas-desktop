from genetic_algorithm.initial_population import create_initial_population
from genetic_algorithm.fitness.fitness_methods import calculate_fitness
from genetic_algorithm.selection.parent_selection_methods import handle_elites, distribute_to_pools, append_parents_from_tournament_pool
from genetic_algorithm.selection.crossover_methods import pair_parents, generate_next_generation_with_pmx
from genetic_algorithm.mutation.mutation_methods import apply_mutation
from config.algorithm_config import max_generations, doctor_swap_rate, doctor_slide_rate, shift_swap_rate, day_swap_rate
import json

def run_genetic_algorithm(doctors, doctor_mapping):
    with open("data/leaves.json", "r") as file:
        leaves_data = json.load(file)
    leave_dict = {
        leave["code"]: {
            "optional_leaves": leave["optional_leaves"],
            "mandatory_leaves": leave["mandatory_leaves"]
        } for leave in leaves_data["leaves"]
    }

    # Başlangıç popülasyonunu oluştur
    population = create_initial_population(doctors)
    population_with_fitness_score = [
                (schedule, calculate_fitness(schedule, doctors, doctor_mapping, leave_dict,log=False)) 
                for schedule in population]

    for generation in range(max_generations):

        doc_rate, slide_rate, shift_rate, day_rate = get_swap_rates(generation)

        # Fitness'lara göre sırala
        population_with_fitness_score.sort(key=lambda x: x[1], reverse=True)

        # Her nesilde fitness skorlarını yazdır
        print(f"\n--- Generation {generation + 1} Fitness Scores ---")
        for i, (schedule, fitness) in enumerate(population_with_fitness_score, start=1):
            print(f"Individual {i}: Fitness = {fitness}")

        # Elitleri seç ve turnuva havuzunu oluştur
        next_generation_pool, pre_tournament_pool, parent_pool = handle_elites(population_with_fitness_score)
        tournament_pool, parent_pool = distribute_to_pools(pre_tournament_pool, parent_pool)
        parent_pool = append_parents_from_tournament_pool(tournament_pool, parent_pool)

        # Çaprazlama
        pairs = pair_parents(parent_pool, next_generation_pool)
        next_generation_pool = generate_next_generation_with_pmx(pairs, next_generation_pool)
        
        # Mutasyon uygula
        mutated_next_generation_pool = apply_mutation(next_generation_pool, doc_rate, slide_rate, shift_rate, day_rate)

        # Yeni nesil fitness hesaplaması
        next_generation_with_fitness = [
            (child_schedule, calculate_fitness(child_schedule, doctors, doctor_mapping, leave_dict, log=False))
            for (child_schedule, _) in mutated_next_generation_pool
        ]

        population_with_fitness_score = next_generation_with_fitness


        # 1000 fitness kontrolü
        if any(fitness == 1000 for _, fitness in next_generation_with_fitness):
            break

        # Loglama
        with open("generation_log.txt", "a") as log_file:
            log_file.write(f"Generation {generation + 1}:\n")
            for i, (sched, fit) in enumerate(sorted(next_generation_with_fitness, key=lambda x: x[1], reverse=True), start=1):
                log_file.write(f"  Schedule {i}: Fitness = {fit}\n")
            log_file.write("\n")

    # Nihai popülasyonu güncelle
    population = [schedule for (schedule, _) in next_generation_with_fitness]

    # Nihai schedule'ları düzenle ve yazdır
    for i in range(len(population)):
        population[i] = sort_doctors_in_shifts(population[i])

    with open("generation_log.txt", "a") as log_file:
        log_file.write("\n=== Final Schedules ===\n")
        for idx, schedule in enumerate(population, start=1):
            log_file.write(f"\nIndividual {idx} Final Schedule:\n")
            for day_index, day in enumerate(schedule, start=1):
                log_file.write(f"  Day {day_index}: {day}\n")
            final_score = calculate_fitness(schedule, doctors, doctor_mapping, leave_dict, log=True)
            log_file.write(f"  Final Score: {final_score}\n")


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
