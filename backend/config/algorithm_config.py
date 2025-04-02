# Algoritma Parametreleri
max_generations = 2000
population_size = 1
shifts_per_day = 2
min_doctors_per_shift = 5
max_doctors_per_shift = 8

e = 2  # Elitist count
etr = 0.4  # Elit transfer rate
ecr = 0.8  # Elit crossover rate
tr = 0.8  # Tournament attendance rate
ps = "random"  # Parent pairing strategy
shuffle_sequential = False  # Parent pairing shuffle sequential
cr = 0.9  # Crossover rate
mr = 0.8  # Mutation rate
mi = 3  # Mutation intensity between 1 - 5


doctor_swap_rate = 0.3  # Doctor swap rate
doctor_slide_rate = 0.3  # Doctor slide rate
shift_swap_rate = 0.2  # Shift swap rate
day_swap_rate = 0.2  # Day swap rate

initial_fitness_score = 1000  # Başlangıç puanı

# Hard penalty
hard_penalty = 1000

# Soft penalties
penalty_unequal_day_night_shifts = 5  # Gündüz-gece farkı cezası
penalty_weekend_free = 50  # Haftasonu boş olmama cezası
penalty_two_night_shifts = 40  # 2 gece üst üste nöbet cezası
penalty_hierarchy_mismatch = 10  # Nöbet alanındaki hiyerarşi hatası cezası
penalty_shift_on_leave = 50  # İzinli günlerde nöbet tutma cezası
