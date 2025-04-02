import random
import math
from config.algorithm_config import e, etr, tr, ecr

def handle_elites(population_with_fitness_score):
    next_generation_pool = []  # Gelecek nesil havuzu
    pre_tournament_pool = []  # Turnuva havuzu
    parent_pool = [] # Parent havuzu

    # Elit bireyleri seç (en yüksek fitness'a sahip ilk 'elite_count' birey)
    elites = population_with_fitness_score[:e]
    
    # Elit bireyleri etr olasılığına göre yeni nesil havuzuna ekle
    for elite in elites:
        if random.random() <= etr:
            next_generation_pool.append(elite)  # Elit birey doğrudan yeni nesle geçer
            
        else:
        # Elit birey ecr oranına göre parent_pool veya pre_tournament_pool'a gider
            if random.random() <= ecr:
                parent_pool.append(elite)  # Elit birey parent havuzuna eklenir
            else:
                pre_tournament_pool.append(elite)  # Elit birey turnuva öncesi havuza eklenir

    # Geriye kalan bireyleri pre turnuva havuzuna ekle
    pre_tournament_pool += population_with_fitness_score[e:]
    
    return next_generation_pool, pre_tournament_pool, parent_pool


def distribute_to_pools(pre_tournament_pool, parent_pool):
    tournament_pool = []

    for individual in pre_tournament_pool:
        if random.random() < tr:
            tournament_pool.append(individual)  # Turnuvaya katılır
        else:
            parent_pool.append(individual)  # Doğrudan parent havuzuna geçer

    return tournament_pool, parent_pool


def append_parents_from_tournament_pool(tournament_pool, parent_pool):

    while len(tournament_pool) > 1:
        # Turnuva havuzundan rastgele iki birey seç
        individual1, individual2 = random.sample(tournament_pool, 2)

        # Daha yüksek fitness değerine sahip bireyi parent havuzuna ekle
        winner = individual1 if individual1[1] > individual2[1] else individual2
        parent_pool.append(winner)

        # Seçilen bireyleri turnuva havuzundan çıkar
        tournament_pool.remove(individual1)
        tournament_pool.remove(individual2)

    # Eğer havuzda tek birey kaldıysa, bu bireyi doğrudan parent havuzuna ekle
    if len(tournament_pool) == 1:
        parent_pool.append(tournament_pool[0])
    return parent_pool



