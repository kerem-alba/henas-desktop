import os
from models.doctor import Doctor
from hill_climbing_algorithm.hill_climbing_algorithm import run_hill_climbing
import time

db_mode = os.getenv("DB_MODE")

if db_mode == "local":
    from services import database_service_postgres as db
elif db_mode == "desktop":
    from services import database_service_sqlite as db


def run_algorithm(schedule_data_id):
    print("Running algorithm...")
    schedule_data = db.get_schedule_data_by_id(schedule_data_id)
    doctors = [
        Doctor(
            doc["code"],
            doc["name"],
            doc["seniority_id"],
            int(doc["shift_count"]),
            doc["shift_areas"],
            doc["shift_duration"],
            doc["optional_leaves"],
            doc["mandatory_leaves"],
        )
        for doc in schedule_data["data"]
    ]

    start_time = time.perf_counter()

    population, schedule_id = run_hill_climbing(doctors, schedule_data_id)

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)
    print(
        f"Algorithm completed in {int(minutes)} minutes and {seconds:.2f} seconds"
    )

    return population, schedule_id
