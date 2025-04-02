from config.algorithm_config import ps, shuffle_sequential, cr, population_size
import random

def pair_parents(parent_pool, next_generation_pool):

    pairs = []
    current_size = len(next_generation_pool)  # Şu anki yeni nesil boyutu
    required_children = population_size - current_size  # Gerekli çocuk sayısı

    if required_children <= 0:
        return pairs  # Eşleşmeye gerek yok

    if ps == "random":
        # RANDOM STRATEGY: Rastgele eşleşmeler
        while len(pairs) * 2 < required_children:
            pair = random.sample(parent_pool, 2)  # Rastgele iki ebeveyn seç
            pairs.append(tuple(pair))

    elif ps == "sequential":
        # SEQUENTIAL STRATEGY: Ardışık eşleşmeler
        if shuffle_sequential:
            random.shuffle(parent_pool)  # Parent havuzu karıştırılır
        else:
            parent_pool.sort(key=lambda x: x[1], reverse=True)  # Fitness puanına göre sıralanır

        start_index = 0 
        while len(pairs) * 2 < required_children:
            for i in range(start_index, len(parent_pool) - 1, 2):
                if len(pairs) * 2 >= required_children:
                    break
                pairs.append((parent_pool[i], parent_pool[i + 1]))
        
            # Başlangıç indeksini kaydır
            start_index = (start_index + 1) % 2  # İlk bireyi atlayarak başla

            # Eğer eşleşme yapılacak birey kalmazsa döngüden çık
            if start_index >= len(parent_pool) - 1:
                break

        # Tek birey artarsa, eşleşmeden bırakılabilir
        if len(parent_pool) % 2 == 1 and len(pairs) * 2 < required_children:
            pairs.append((parent_pool[-1], None))  # Son parent eşleşmedi

    else:
        raise ValueError("Invalid pairing strategy. Choose 'random' or 'sequential'.")

    return pairs

def pmx_crossover(parent1, parent2):
    
    schedule1, schedule2 = parent1[0], parent2[0]
    length = len(schedule1)
    # İki kesim noktası rastgele seçilir
    point1, point2 = sorted(random.sample(range(length), 2))

    # Çocuklar başlangıçta ebeveynlerin bir kopyasıdır
    child1 = schedule1[:]
    child2 = schedule2[:]
    # Kesim noktaları arasındaki genleri değiştir
    child1[point1:point2] = schedule2[point1:point2]
    child2[point1:point2] = schedule1[point1:point2]
    # Mapping (eşleştirme) kuralları oluşturulur
    mapping1 = {tuple(map(tuple, schedule2[i])): tuple(map(tuple, schedule1[i])) for i in range(point1, point2)}
    mapping2 = {tuple(map(tuple, schedule1[i])): tuple(map(tuple, schedule2[i])) for i in range(point1, point2)}
    
    # Mapping kurallarını kesim noktası dışında uygula
    child1 = apply_mapping(child1, mapping1, point1, point2, length)
    child2 = apply_mapping(child2, mapping2, point1, point2, length)
    return [(child1, None), (child2, None)]

def apply_mapping(child, mapping, point1, point2, length):
        for i in range(length):
            if i < point1 or i >= point2:
                current = tuple(map(tuple, child[i]))
                visited = set()
                while current in mapping:
                    if current in visited:
                        print("Cycle detected in PMX mapping!")
                        break
                    visited.add(current)
                    current = mapping[current]
                child[i] = [list(inner) for inner in current]
        return child

def perform_crossover(pair):
    parent1, parent2 = pair
    if parent2 is None:
        # Eğer çift eksikse, tek parent olduğu gibi döner
        return [parent1]
    if random.random() <= cr:
        # PMX ile çaprazlama
        return pmx_crossover(parent1, parent2)
    else:
        # Çaprazlama gerçekleşmezse, ebeveynler olduğu gibi döner
        return [parent1, parent2]

def generate_next_generation_with_pmx(pairs, next_generation_pool):
    # Elit bireyler zaten next_generation_pool içinde
    new_offspring = []
    for pair in pairs:
        # PMX ile çaprazlama yap
        children = perform_crossover(pair)
        new_offspring.extend(children)

    # Yeni nesle yeni bireyleri ekle
    next_generation_pool.extend(new_offspring)
    # Fazlalık bireyleri kaldır
    if len(next_generation_pool) > population_size: 
        next_generation_pool = random.sample(next_generation_pool, population_size)
    elif len(next_generation_pool) < population_size:
        deficit = population_size - len(next_generation_pool)
        # Eksik bireyleri tamamla
        if len(next_generation_pool) > 0:
            additional_individuals = (
                random.sample(next_generation_pool, deficit)
                if len(next_generation_pool) >= deficit
                else random.choices(next_generation_pool, k=deficit)  # Tekrar seçime izin verilir
            )
            next_generation_pool.extend(additional_individuals)
        else:
            raise ValueError("Next generation pool is empty. Cannot generate additional individuals.")

    return next_generation_pool
