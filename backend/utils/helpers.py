def assign_codes(doctors):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    doctor_mapping = {}

    for index, doctor in enumerate(doctors):
        code = alphabet[index % len(alphabet)]
        doctor.code = code
        doctor_mapping[code] = doctor

    return doctors, doctor_mapping
