from config.algorithm_config import (
    penalty_unequal_day_night_shifts,
    penalty_two_night_shifts,
    penalty_weekend_free,
    penalty_hierarchy_mismatch,
    penalty_shift_on_leave,
    hard_penalty,
)
from services.database_service import add_log_messages
import config.globals as g


def check_unequal_day_night_shifts(schedule, schedule_data_id, log):
    penalty = 0
    doctor_shift_counts = {}

    for day in schedule:
        day_shift = day[0] 
        night_shift = day[1] 

        for doctor in day_shift:
            doctor_shift_counts[doctor] = doctor_shift_counts.get(
                doctor, {"day": 0, "night": 0}
            )
            doctor_shift_counts[doctor]["day"] += 1

        for doctor in night_shift:
            doctor_shift_counts[doctor] = doctor_shift_counts.get(
                doctor, {"day": 0, "night": 0}
            )
            doctor_shift_counts[doctor]["night"] += 1

    for doctor, shifts in doctor_shift_counts.items():
        shift_difference = shifts["night"] - shifts["day"]
        if shift_difference > 0:
            penalty += (shift_difference) * penalty_unequal_day_night_shifts
            if log:
                log_text = (
                    f"Dr. {doctor} : Gece-gündüz shiftleri eşit değil -  "
                    f"{shifts['day']} gündüz, {shifts['night']} gece."
                )
                add_log_messages(schedule_data_id, [log_text])

    return penalty


def check_two_night_shifts(schedule,schedule_data_id, log):
    penalty = 0
    doctor_night_shifts = {}

    # Her doktorun gece nöbetlerini gün gün kontrol et
    for day_index, day in enumerate(schedule):
        night_shift = day[1]  # Gece shift

        for doctor in night_shift:
            if doctor not in doctor_night_shifts:
                doctor_night_shifts[doctor] = []

            doctor_night_shifts[doctor].append(day_index)

    # Doktorların gece nöbetlerini kontrol et
    for doctor, night_days in doctor_night_shifts.items():
        for i in range(len(night_days) - 1):
            if night_days[i + 1] == night_days[i] + 1:  # 2 gece üst üste kontrolü
                penalty += penalty_two_night_shifts
                if log:
                    log_text = (
                        f"Dr. {doctor} : 2 gece üst üste nöbet - {night_days[i] + 1}. gün ve {night_days[i + 1] + 1}. gün."
                    )
                    add_log_messages(schedule_data_id, [log_text])

    return penalty


def check_weekend_free(schedule, doctors, schedule_data_id, log):
    penalty = 0

    # Her doktorun nöbet tuttuğu günleri takip et
    doctor_shifts = {doctor.code: set() for doctor in doctors}

    # Programdaki nöbetleri kontrol et
    for day_index, day in enumerate(schedule):
        for shift in day:
            for doctor in shift:
                doctor_shifts[doctor].add(day_index)

    # Haftanın günlerini düzenle
    total_days = len(schedule)
    weekend_days = [
        (5 - g.week_start_day) % 7,
        (6 - g.week_start_day) % 7,
    ]  # Cumartesi ve Pazar günleri

    # Her doktorun hafta sonu boş olup olmadığını kontrol et
    for doctor, shifts in doctor_shifts.items():
        has_free_weekend = False

        # Tüm hafta sonlarını kontrol et
        for i in range(0, total_days, 7):  # Her hafta başlangıcı
            saturday = i + weekend_days[0]
            sunday = i + weekend_days[1]

            if saturday < total_days and sunday < total_days:
                if saturday not in shifts and sunday not in shifts:
                    has_free_weekend = True
                    break

        # Eğer hiç boş hafta sonu yoksa ceza uygula
        if not has_free_weekend:
            penalty += penalty_weekend_free
            if log:
                log_text = f"Dr. {doctor}: Boş haftasonu yok."
                add_log_messages(schedule_data_id, [log_text])

    return penalty


def check_hierarchy_mismatch(schedule, doctors, schedule_data_id, log):
    penalty = 0
    doctor_dict = {doctor.code: doctor for doctor in doctors}

    # Alan bazında minimum doktor ihtiyacı
    min_doctors_per_area = {
        info["id"]: info["min_doctors_per_area"] for _, info in g.shift_areas_data.items()
    }

    for day_index, day in enumerate(schedule):
        for shift_index, shift in enumerate(day):
            # Her area için sayıcılar
            primary_counts = {area_id: 0 for area_id in min_doctors_per_area.keys()}
            secondary_counts = {area_id: 0 for area_id in min_doctors_per_area.keys()}
            tertiary_counts = {area_id: 0 for area_id in min_doctors_per_area.keys()}

            # Doktorları say
            for doctor_code in shift:
                doctor = doctor_dict.get(doctor_code)
                if not doctor or not doctor.shift_areas:
                    continue

                # 1) Birincil alan
                if len(doctor.shift_areas) >= 1:
                    primary_area = doctor.shift_areas[0]
                    if primary_area in primary_counts:
                        primary_counts[primary_area] += 1

                # 2) İkincil alan
                if len(doctor.shift_areas) >= 2:
                    secondary_area = doctor.shift_areas[1]
                    if secondary_area in secondary_counts:
                        secondary_counts[secondary_area] += 1

                # 3) Üçüncül alan
                if len(doctor.shift_areas) >= 3:
                    tertiary_area = doctor.shift_areas[2]
                    if tertiary_area in tertiary_counts:
                        tertiary_counts[tertiary_area] += 1

            # Eksikleri kapatmaya çalış
            for area_id, required_count in min_doctors_per_area.items():
                current_count = primary_counts.get(area_id, 0)
                missing = required_count - current_count

                if missing <= 0:
                    continue

                # Log için alan ismini bul
                area_name = next(
                    (name for name, data in g.shift_areas_data.items() if data["id"] == area_id),
                    area_id
                )

                # Eksik varsa log
                if log:
                    log_text = f"{area_name} alanında {missing} doktor eksik - {day_index + 1}. gün {shift_index + 1}. shift"

                # İkincil alan
                can_fill_secondary = secondary_counts.get(area_id, 0)
                fill_secondary = min(missing, can_fill_secondary)
                if fill_secondary > 0:
                    penalty += fill_secondary * penalty_hierarchy_mismatch
                    missing -= fill_secondary
                    if log:
                        log_text = f"{area_name} alanında {fill_secondary} doktor ikincil tercihinde çalışacak. - {day_index + 1}. gün {shift_index + 1}. shift" 
                        add_log_messages(schedule_data_id, [log_text])

                # Üçüncül alan
                if missing > 0:
                    can_fill_tertiary = tertiary_counts.get(area_id, 0)
                    fill_tertiary = min(missing, can_fill_tertiary)
                    if fill_tertiary > 0:
                        penalty += fill_tertiary * 1.2 * penalty_hierarchy_mismatch
                        missing -= fill_tertiary
                        if log:
                            log_text = f"{area_name} alanında {fill_tertiary} doktor üçüncü tercihinde çalışacak. - {day_index + 1}. gün {shift_index + 1}. shift"  
                            add_log_messages(schedule_data_id, [log_text])

                # Hâlâ eksik varsa hard_penalty
                if missing > 0:
                    penalty += missing * hard_penalty
                    if log:
                        log_text = f"[!] {area_name} alanında {missing} doktor eksik, yeri doldurulamadı- {day_index + 1}. gün {shift_index + 1}. shift"
                        add_log_messages(schedule_data_id, [log_text])

    return penalty


def check_leave_days(schedule, doctors, schedule_data_id, log):

    penalty = 0

    for day_index, day in enumerate(schedule):
        for shift_index, shift in enumerate(day):
            for doctor_code in shift:
                # Doktor bilgisi varsa izinleri kontrol et
                doctor = next((doc for doc in doctors if doc.code == doctor_code), None)
                if not doctor:
                    continue

                # Optional izin ihlali
                if [day_index + 1, shift_index] in doctor.optional_leaves:
                    penalty += penalty_shift_on_leave
                    if log:
                        log_text = f"Dr. {doctor_code}: Opsiyonel izninde nöbet - {day_index + 1}. gün, {shift_index}. shift."
                        add_log_messages(schedule_data_id, [log_text])

                # Mandatory izin ihlali
                if [day_index + 1, shift_index] in doctor.mandatory_leaves:
                    penalty += hard_penalty
                    if log:
                        log_text = f"[!] Dr. {doctor_code}: Zorunlu izninde nöbet - {day_index + 1}. gün, {shift_index}. shift."                        
                        add_log_messages(schedule_data_id, [log_text])

    return penalty
