from config.algorithm_config import hard_penalty
from collections import Counter
from services.database_service import add_log_messages

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

                        add_log_messages(schedule_data_id, [log_text])

    return penalty

# Hard Constraint 2: Ardışık günlerde aynı doktora shift atanmış mı?
def check_consecutive_shifts(schedule,schedule_data_id, log):
    penalty = 0
    for day_index in range(len(schedule)):
        day = schedule[day_index]
        for shift_index in range(len(day) - 1):
            current_shift = day[shift_index]
            next_shift = day[shift_index + 1]
            for doctor_code in current_shift:
                if doctor_code in next_shift:
                    penalty += hard_penalty

                    if log:
                        log_text = (
                            f"[!] Dr. {doctor_code}: Ardışık nöbet - {day_index + 1}. gün "
                        )

                        add_log_messages(schedule_data_id, [log_text])


            if day_index < len(schedule) - 1:
                next_day_shift = schedule[day_index + 1][shift_index]
                for doctor_code in next_shift:
                    if doctor_code in next_day_shift:
                        penalty += hard_penalty
                        if log:
                            log_text = (
                                f"[!] Dr. {doctor_code}: Ardışık nöbet - {day_index + 1}. günün gecesi ve ertesi sabah "
                            )
                            
                            add_log_messages(schedule_data_id, [log_text])

    return penalty



# Hard Constraint 3: 2 geceden fazla üst üste nöbet kontrolü
def check_three_consecutive_night_shifts(schedule,schedule_data_id, log):
    penalty = 0
    for day_index in range(len(schedule) - 2):
        night_shift_1 = schedule[day_index][1]
        night_shift_2 = schedule[day_index + 1][1]
        night_shift_3 = schedule[day_index + 2][1]
        for doctor_code in night_shift_1:
            if doctor_code in night_shift_2 and doctor_code in night_shift_3:
                penalty += hard_penalty
                if log:
                    log_text = (
                        f"[!] Dr. {doctor_code}: 3 gece üst üste nöbet - {day_index + 1}. günden itibaren"
                    )
                    
                    add_log_messages(schedule_data_id, [log_text])

    return penalty
