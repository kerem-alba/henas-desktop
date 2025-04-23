import os
import sys
import traceback
from dotenv import load_dotenv

try:
    print("Starting Flask application...")
    print(f"Python executable: {sys.executable}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")

    # Veritabanı yolunu kontrol et
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mydata.db")
    print(f"Database path: {db_path}")
    print(f"Database exists: {os.path.exists(db_path)}")

    # Dotenv yükle
    load_dotenv()

    # Flask uygulamasını içe aktar
    try:
        from app.flask_app import app
        print("Flask app imported successfully")
    except Exception as e:
        print(f"Error importing Flask app: {e}")
        traceback.print_exc()
        sys.exit(1)

    if __name__ == "__main__":
        try:
            # Herhangi bir IP adresinden bağlantı kabul et
            app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
        except Exception as e:
            print(f"Error running Flask app: {e}")
            traceback.print_exc()
            sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    traceback.print_exc()
    sys.exit(1)
