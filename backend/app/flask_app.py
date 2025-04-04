import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from config.secrets import Config
import config.globals as g
from config import init_db

db_mode = os.getenv("DB_MODE")

if db_mode == "local":
    from services import database_service_postgres as db
elif db_mode == "desktop":
    from services import database_service_sqlite as db

from run_algorithm import run_algorithm
import json


init_db.init_db()
app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)  
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "https://henas.vercel.app"]}})


@app.route("/login", methods=["POST"])
def login():
    """Kullanıcı girişini doğrular ve JWT token döndürür."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Kullanıcı adı ve şifre gerekli"}), 400

    user_id = db.authenticate_user(username, password)
    
    if user_id:
        access_token = create_access_token(identity=str(user_id))  
        refresh_token = create_refresh_token(identity=str(user_id))  # Yeni refresh token ekledik
        return jsonify({
            "message": "Giriş başarılı",
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    else:
        return jsonify({"error": "Geçersiz kullanıcı adı veya şifre"}), 401


@app.route("/refresh", methods=["POST"])
  
def refresh():
    """Refresh token ile yeni access token üretir."""
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)
    return jsonify({"access_token": new_access_token}), 200
   


@app.route("/get-doctors", methods=["GET"])
def get_detailed_doctors_endpoint():
    try:
        doctors = db.get_detailed_doctors()

        formatted_doctors = [
            {
                "name": doc[0],
                "seniority_id": doc[1],
                "max_shifts_per_month": doc[2],
                "shift_areas": doc[3],
            }
            for doc in doctors
        ]
        return app.response_class(
            response=json.dumps(formatted_doctors, ensure_ascii=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/run-algorithm", methods=["POST"])
def run_algorithm_endpoint():
    try:
        data = request.get_json()
        schedule_id = data.get("schedule_id")

        if not schedule_id:
            return jsonify({"error": "schedule_id is required"}), 400

        population, generated_schedule_id = run_algorithm(schedule_id)

        return jsonify({
            "schedule": population,
            "schedule_id": generated_schedule_id
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/doctors", methods=["GET"])
def list_doctors_endpoint():
    try:
        doctors = db.get_doctors()
        return jsonify(doctors)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/doctors", methods=["POST"])
def add_doctor_endpoint():
    try:
        data = request.json

        if not data.get("name") or not data.get("seniority_id"):
            return jsonify({"error": "name and seniority_id are required"}), 400

        new_id = db.add_doctor(data)

        return jsonify({"id": new_id, "message": "Doctor added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route("/doctors/all", methods=["PUT"])
def update_doctors_endpoint():
    try:
        data = request.json
        db.update_all_doctors(data)
        return jsonify({"message": "Doctors updated successfully"}), 200
    except Exception as e:
        print("Hata Ayrıntısı:", e)
        return jsonify({"error": str(e)}), 500



@app.route("/doctors/<int:doctor_id>", methods=["DELETE"])
def delete_doctor_endpoint(doctor_id):
    try:
        db.delete_doctor(doctor_id)
        return jsonify({"message": "Doctor deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/seniority", methods=["GET"])
def list_seniority():
    try:
        seniority = db.get_seniority()
        return jsonify(seniority), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/seniority/detailed", methods=["GET"])
def list_detailed_seniority():
    try:
        seniority = db.get_detailed_seniority()
        return jsonify(seniority), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/seniority", methods=["POST"])
def add_seniority_endpoint():
    try:
        data = request.json

        if not data.get("seniority_name") or not data.get("max_shifts_per_month"):
            return jsonify({"error": "seniority_name ve max_shifts_per_month gereklidir"}), 400

        # Eğer shift_area_ids boşsa, tüm shift_areas ID’lerini al
        if not data.get("shift_area_ids"):
            shift_areas = db.get_shift_areas()  # Mevcut methodu kullan
            data["shift_area_ids"] = [area["id"] for area in shift_areas.values()]

        # Servis fonksiyonunu çağır (veritabanı işlemi burada yapılır)
        new_id = db.add_seniority(data)

        return jsonify({"id": new_id, "message": "Kıdem başarıyla eklendi!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route("/seniority/all", methods=["PUT"])
def update_seniorities_endpoint():
    try:
        data = request.json
        db.update_all_seniorities(data)
        return jsonify({"message": "Seniorities updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/seniority/<int:seniority_id>", methods=["DELETE"])
def delete_seniority_endpoint(seniority_id):
    try:
        db.delete_seniority(seniority_id)
        return jsonify({"message": "Seniority deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/shift-areas", methods=["GET"])
def list_shift_areas():
    try:
        shift_areas = db.get_shift_areas()
        return jsonify(shift_areas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/shift-areas", methods=["POST"])
def add_shift_area_endpoint():
    try:
        data = request.json

        if not data.get("area_name") or not data.get("min_doctors_per_area"):
            return jsonify({"error": "area_name and min_doctors_per_area are required"}), 400

        new_id = db.add_shift_area(data)
        return jsonify({"id": new_id, "message": "Shift area added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/shift-areas/all", methods=["PUT"])
def update_shift_areas_endpoint():
    try:
        data = request.json
        db.update_all_shift_areas(data)
        return jsonify({"message": "Shift areas updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/shift-areas/<int:shift_area_id>", methods=["DELETE"])
  
def delete_shift_area_endpoint(shift_area_id):
    try:
        db.delete_shift_area(shift_area_id)
        return jsonify({"message": "Shift area deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/schedule-data/<int:schedule_id>", methods=["GET"])
  
def get_schedule_data_endpoint(schedule_id):
    try:
        schedule = db.get_schedule_data_by_id(schedule_id)

        if not schedule:
            return jsonify({"error": "Schedule not found"}), 404

        return jsonify(schedule), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/schedule-data", methods=["GET"])
  
def get_all_schedule_data_endpoint():
    try:
        schedule_data = db.get_all_schedule_data()
        return jsonify(schedule_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/schedule-data", methods=["POST"])
  
def add_schedule_data_endpoint():
    try:
        data = request.json

        if not data.get("name") or not data.get("schedule") or not data.get("first_day") or not data.get("days_in_month"):
            return jsonify({"error": "name and schedule (JSON) are required"}), 400

        new_id = db.add_schedule_data(
            data["name"], 
            data["schedule"], 
            data["first_day"], 
            data["days_in_month"]
        )
        return jsonify(new_id), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/schedule-data/<int:schedule_id>", methods=["PUT"])
  
def update_schedule_data_endpoint(schedule_id):
    try:
        data = request.json

        if not data.get("name") or not data.get("schedule"):
            return jsonify({"error": "name and schedule (JSON) are required"}), 400

        db.update_schedule_data(schedule_id, data["name"], data["schedule"])

        return jsonify({"message": "Schedule data updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/schedule-data/<int:schedule_id>", methods=["DELETE"])
  
def delete_schedule_data_endpoint(schedule_id):
    try:
        db.delete_schedule_data(schedule_id)
        return jsonify({"message": "Schedule data deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/schedules/<int:schedule_id>", methods=["GET"])
  
def get_schedule_by_id_endpoint(schedule_id):
    """Belirtilen ID'ye sahip schedule'ı getirir."""
    try:
        schedule = db.get_schedule_by_id(schedule_id)
        if schedule:
            return jsonify(schedule), 200
        else:
            return jsonify({"error": "Schedule not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/schedules/<int:schedule_id>", methods=["DELETE"])
def delete_schedule_endpoint(schedule_id):
    """Belirtilen ID'ye sahip schedule'ı siler."""
    try:
        db.delete_schedule(schedule_id)
        return jsonify({"message": "Schedule deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/schedules", methods=["GET"])
def list_schedules_endpoint():
    try:
        schedules = db.get_all_schedules()
        return jsonify(schedules)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/settings", methods=["GET"])
def get_settings():
    """Mevcut MAX_GENERATIONS değerini döndür."""
    return jsonify({"max_generations": g.MAX_GENERATIONS}), 200

@app.route("/settings", methods=["POST"])
def update_settings():
    """MAX_GENERATIONS değerini güncelle."""
    try:
        data = request.json
        if "max_generations" in data:
            g.MAX_GENERATIONS = int(data["max_generations"])  # Yeni değeri güncelle
            return jsonify({
                "message": "Çözüm kalitesi güncellendi!",
                "max_generations": g.MAX_GENERATIONS
            }), 200
        else:
            return jsonify({"error": "Geçersiz veri"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

