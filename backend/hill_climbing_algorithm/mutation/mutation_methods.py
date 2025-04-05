import random
from config.algorithm_config import min_doctors_per_shift, max_doctors_per_shift, log_to_file, log_file_path
import config.globals as g


def mutate_schedule(schedule, doc_rate, slide_rate, shift_rate, day_rate, doc24_slide_rate, doc24_swap_rate):
    # Rastgele bir mutasyon türü seç
    mutation_type = random.choices(
        ["doctor_swap", "doctor_slide", "shift_swap", "day_swap","doctor24_swap", "doctor24_slide"],
        weights=[doc_rate, slide_rate,  shift_rate, day_rate, doc24_slide_rate, doc24_swap_rate],
        k=1
    )[0]

    if mutation_type == "doctor_swap":
        return doctor_swap(schedule)
    elif mutation_type == "doctor_slide":
        return doctor_slide(schedule)
    elif mutation_type == "shift_swap":
        return shift_swap(schedule)
    elif mutation_type == "day_swap":
        return day_swap(schedule)
    elif mutation_type == "doctor24_swap":
        return doctor24_swap(schedule)
    elif mutation_type == "doctor24_slide":
        return doctor24_slide(schedule)

    return schedule

def doctor_swap(schedule):
    max_tries = 100
    for _ in range(max_tries):
        day1_index, day2_index = random.sample(range(len(schedule)), 2)
        shift1_index = random.randint(0, len(schedule[day1_index]) - 1)
        shift2_index = random.randint(0, len(schedule[day2_index]) - 1)

        shift1 = schedule[day1_index][shift1_index]
        shift2 = schedule[day2_index][shift2_index]

        candidates1 = [d for d in shift1 if g.code_to_duration.get(d) == "12"]
        candidates2 = [d for d in shift2 if g.code_to_duration.get(d) == "12"]

        if candidates1 and candidates2:
            doc1 = random.choice(candidates1)
            doc2 = random.choice(candidates2)

            idx1 = shift1.index(doc1)
            idx2 = shift2.index(doc2)

            shift1[idx1], shift2[idx2] = doc2, doc1

            if log_to_file:
                with open(log_file_path, "a") as log_file:
                    log_file.write(
                        f"Swap (12'lik): Dr. {doc1} (Day {day1_index + 1}, Shift {shift1_index + 1}) "
                        f"Dr. {doc2} (Day {day2_index + 1}, Shift {shift2_index + 1})\n")

            return schedule

    return schedule


def doctor_slide(schedule):
    max_tries = 100

    for _ in range(max_tries):
        day_from = random.randint(0, len(schedule) - 1)
        shift_from = random.randint(0, len(schedule[day_from]) - 1)

        candidates = [d for d in schedule[day_from][shift_from] if g.code_to_duration.get(d) == "12"]
        if len(candidates) > 0 and len(schedule[day_from][shift_from]) > min_doctors_per_shift:
            doctor_to_slide = random.choice(candidates)
            break
    else:
        return schedule

    for _ in range(max_tries):
        day_to = random.randint(0, len(schedule) - 1)
        shift_to = random.randint(0, len(schedule[day_to]) - 1)

        if len(schedule[day_to][shift_to]) < max_doctors_per_shift:
            break
    else:
        return schedule

    schedule[day_from][shift_from].remove(doctor_to_slide)
    schedule[day_to][shift_to].append(doctor_to_slide)

    if log_to_file:
        with open(log_file_path, "a") as log_file:
            log_file.write(
                f"Slide (12'lik): Dr. {doctor_to_slide} moved from Day {day_from + 1}, Shift {shift_from + 1} "
                f"to Day {day_to + 1}, Shift {shift_to + 1}\n")

    return schedule


def shift_swap(schedule):
    day1_index, day2_index = random.sample(range(len(schedule)), 2)
    day1, day2 = schedule[day1_index], schedule[day2_index]

    shift1_index = random.randint(0, len(day1) - 1)
    shift2_index = random.randint(0, len(day2) - 1)

    day1[shift1_index], day2[shift2_index] = day2[shift2_index], day1[shift1_index]
    
    if log_to_file:
        with open(log_file_path, "a") as log_file:
            log_file.write(
                f"Shift Swap: Day {day1_index + 1} Shift {shift1_index + 1} "
                f"Day {day2_index + 1} Shift {shift2_index + 1}\n"
            )
    return schedule


def day_swap(schedule):
    """İki günü tamamen yer değiştirir."""
    idx1, idx2 = random.sample(range(len(schedule)), 2) 
    schedule[idx1], schedule[idx2] = schedule[idx2], schedule[idx1] 

    if log_to_file:
        with open(log_file_path, "a") as log_file:
            log_file.write(f"Day Swap: Day {idx1 + 1} <-> Day {idx2 + 1}\n")

    return schedule

def doctor24_swap(schedule):
    def find_valid_24_doctor():
        tries = 0
        max_tries = 100

        while tries < max_tries:
            day_index = random.randint(0, len(schedule) - 1)
            day = schedule[day_index]
            day_shift = day[0]
            night_shift = day[1]

            for doctor_code in day_shift:
                if doctor_code in night_shift and g.code_to_duration.get(doctor_code) == "24":
                    return day_index, doctor_code
            tries += 1

        return None, None

    day1_index, doc1 = find_valid_24_doctor()
    if doc1 is None:
        return schedule 

    for _ in range(100):
        day2_index, doc2 = find_valid_24_doctor()
        if doc2 and doc2 != doc1 and day2_index != day1_index:
            break
    else:
        return schedule 

    for shift_index in [0, 1]: 
        schedule[day1_index][shift_index] = [
            doc2 if d == doc1 else d for d in schedule[day1_index][shift_index]
        ]
        schedule[day2_index][shift_index] = [
            doc1 if d == doc2 else d for d in schedule[day2_index][shift_index]
        ]

    if log_to_file:  
        with open(log_file_path, "a") as log_file:  
            log_file.write(
                f"24h Swap: Dr. {doc1} (Day {day1_index + 1}) <-> Dr. {doc2} (Day {day2_index + 1})\n")

    return schedule

def doctor24_slide(schedule):
    max_tries = 100

    for _ in range(max_tries):
        day_from = random.randint(0, len(schedule) - 1)
        day = schedule[day_from]
        day_shift = day[0]
        night_shift = day[1]

        for doctor_code in day_shift:
            if doctor_code in night_shift and g.code_to_duration.get(doctor_code) == "24":
                doctor_to_move = doctor_code
                break
        else:
            continue 
        break
    else:
        return schedule

    for _ in range(max_tries):
        day_to = random.randint(0, len(schedule) - 1)
        if day_to != day_from:
            if (
                len(schedule[day_to][0]) < max_doctors_per_shift and
                len(schedule[day_to][1]) < max_doctors_per_shift
            ):
                break
    else:
        return schedule  

    if doctor_to_move in schedule[day_from][0]:
        schedule[day_from][0].remove(doctor_to_move)
    if doctor_to_move in schedule[day_from][1]:
        schedule[day_from][1].remove(doctor_to_move)

    schedule[day_to][0].append(doctor_to_move)
    schedule[day_to][1].append(doctor_to_move)

    if log_to_file:
        with open(log_file_path, "a") as log_file:
            log_file.write(
                f"24h Slide: Dr. {doctor_to_move} moved from Day {day_from + 1} -> Day {day_to + 1}\n")

    return schedule

