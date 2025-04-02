from models.doctor import Doctor
from genetic_algorithm.genetic_algorithm import run_genetic_algorithm
from hill_climbing_algorithm.hill_climbing_algorithm import run_hill_climbing
from services.database_service import get_schedule_data_by_id
import time

def run_algorithm(schedule_data_id):
    schedule_data = get_schedule_data_by_id(schedule_data_id)

    doctors = [
        Doctor(
            doc["code"],
            doc["name"],
            doc["seniority_id"],
            int(doc["shift_count"]),
            doc["shift_areas"],
            doc["optional_leaves"],
            doc["mandatory_leaves"],
        )
        for doc in schedule_data["data"]
    ]

    start_time = time.perf_counter()

    # run_genetic_algorithm(doctors)
    population, schedule_id = run_hill_climbing(doctors, schedule_data_id)
    print("000")

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    print(
        f"Algorithm completed in {int(minutes)} minutes and {seconds:.2f} seconds"
    )

    return population, schedule_id
