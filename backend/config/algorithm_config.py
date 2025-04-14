# Algoritma Parametreleri
population_size = 1
shifts_per_day = 2
min_doctors_per_shift = 5
max_doctors_per_shift = 8


doctor_swap_rate = 0.4  # Doctor swap rate
doctor_slide_rate = 0.4  # Doctor slide rate
shift_swap_rate = 0  # Shift swap rate
day_swap_rate = 0.2  # Day swap rate
doctor24_swap_rate = 0  # Doctor 24-hour swap rate
doctor24_slide_rate = 0  # Doctor 24-hour slide rate

initial_fitness_score = 1000  # Başlangıç puanı

# Hard penalty
hard_penalty = 1000

# Soft penalties
penalty_unequal_day_night_shifts = 5  # Gündüz-gece farkı cezası
penalty_weekend_free = 50  # Haftasonu boş olmama cezası
penalty_two_night_shifts = 40  # 2 gece üst üste nöbet cezası
penalty_hierarchy_mismatch = 10  # Nöbet alanındaki hiyerarşi hatası cezası
penalty_shift_on_leave = 50  # İzinli günlerde nöbet tutma cezası

log_to_file = True  # Log dosyasına yazma durumu
import os
file_path = os.path.join(os.path.dirname(__file__), "..", "generation_log.txt")
log_file_path = os.path.abspath(file_path)
