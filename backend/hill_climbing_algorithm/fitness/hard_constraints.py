import os
from config.algorithm_config import hard_penalty
from collections import Counter
import config.globals as g

db_mode = os.getenv("DB_MODE")

if db_mode == "local":
    from services import database_service_postgres as db
elif db_mode == "desktop":
    from services import database_service_sqlite as db

# Hard Constraint 1: Aynı shift içinde aynı doktor birden fazla kez atanmış mı?
def check_duplicate_shifts(schedule, schedule_data_id, log):
    penalty = 0
    for day_index, day in enumerate(schedule):
        for shift_index, shift in enumerate(day):
            freq = Counter(shift)
            for doctor_code, count in freq.items():
                if count > 1:
                    penalty += hard_penalty * (count - 1)

                    if log:
                        log_text = (
                            f"[!] Dr. {doctor_code}: Aynı nöbette {count} kere - {day_index + 1}. gün, {shift_index + 1}. shift."
                        )
                        db.add_log_messages(schedule_data_id, [log_text])

    return penalty

# Hard Constraint 2: Ardışık shiftlerde aynı doktora shift atanmış mı?
# Ardışık nöbetlerde 24 saat tamamlanmadı mı?

def check_consecutive_shifts(schedule, schedule_data_id, log):
    penalty = 0
    total_days = len(schedule)

    for day_index in range(total_days):
        day_shift = schedule[day_index][0]
        night_shift = schedule[day_index][1]

        # Aynı gün ve ertesi sabah kontrolü
        for doctor_code in set(day_shift + night_shift):
            duration = g.code_to_duration.get(doctor_code)

            # Aynı gün hem gündüz hem gece atanma (sadece 12 saatlikler)
            if duration == "12" and doctor_code in day_shift and doctor_code in night_shift:
                penalty += hard_penalty
                if log:
                    log_text = f"[!] Dr. {doctor_code}: Ardışık nöbet - {day_index + 1}. gün"
                    db.add_log_messages(schedule_data_id, [log_text])

            # Gece → ertesi sabah (tüm doktorlar için geçerli)
            if (
                day_index < total_days - 1
                and doctor_code in night_shift
                and doctor_code in schedule[day_index + 1][0]
            ):
                penalty += hard_penalty
                if log:
                    log_text = f"[!] Dr. {doctor_code}: Gece sonrası ertesi sabah tekrar atanmış - {day_index + 2}. gün sabah"
                    db.add_log_messages(schedule_data_id, [log_text])

    return penalty




# Hard Constraint 3: 2 geceden fazla üst üste nöbet kontrolü
def check_three_consecutive_night_shifts(schedule,schedule_data_id, log):
    penalty = 0
    for day_index in range(len(schedule) - 2):
        night_shift_1 = schedule[day_index][1]
        night_shift_2 = schedule[day_index + 1][1]
        night_shift_3 = schedule[day_index + 2][1]
        for doctor_code in night_shift_1:
            if (doctor_code in night_shift_2 
                and doctor_code in night_shift_3 
                and g.code_to_duration.get(doctor_code) == "12"
            ):
                penalty += hard_penalty
                if log:
                    log_text = (
                        f"[!] Dr. {doctor_code}: 3 gece üst üste nöbet - {day_index + 1}. günden itibaren"
                    )
                    
                    db.add_log_messages(schedule_data_id, [log_text])

    return penalty
