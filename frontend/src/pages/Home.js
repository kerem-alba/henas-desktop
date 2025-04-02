import Footer from "../components/Footer";

export default function HomePage() {
  return (
    <div className="d-flex flex-column background-gradient min-vh-100">
      <div className="container-fluid p-5 flex-grow-1">
        <div className="d-flex justify-content-center mb-4 pb-3">
          <img src="/henas-bot.png" alt="Henas Bot" width="150" height="150" />
        </div>

        {/* Adımlar Kartları */}
        <div className="row g-4">
          {/* 1. Doktor Bilgileri */}
          <div className="col-md-4">
            <div className="card shadow-lg bg-dark text-white rounded-4 transition-card">
              <div className="card-body text-center">
                <h5 className="fw-bold">1️⃣ Doktor Bilgileri</h5>
                <p className="text-white-50">Doktorların kıdem ve isim bilgilerini girin.</p>
                <a href="/hospital" className="btn btn-success w-50">
                  Hastanem'e Git
                </a>
              </div>
            </div>
          </div>

          {/* 2. Nöbet Listesi Verileri */}
          <div className="col-md-4">
            <div className="card shadow-lg bg-dark text-white rounded-4 transition-card">
              <div className="card-body text-center">
                <h5 className="fw-bold">2️⃣ Nöbet Listesi Verileri</h5>
                <p className="text-white-50">Doktor kodlarını düzenleyin, nöbet sayılarını ve izinleri girin.</p>
                <a href="/schedule-data" className="btn btn-success w-50">
                  Verileri Düzenle
                </a>
              </div>
            </div>
          </div>

          {/* 3. Ayarlar */}
          <div className="col-md-4">
            <div className="card shadow-lg bg-primary text-white rounded-4 transition-card">
              <div className="card-body text-center">
                <h5 className="fw-bold">3️⃣ Ayarlar</h5>
                <p className="text-white-50">İstenen liste kalitesini seçin.</p>
                <a href="/settings" className="btn btn-light w-50">
                  Ayarları Düzenle
                </a>
              </div>
            </div>
          </div>

          {/* 4. Nöbet Listesi Oluştur */}
          <div className="col-md-4">
            <div className="card shadow-lg bg-dark text-white rounded-4 transition-card">
              <div className="card-body text-center">
                <h5 className="fw-bold">4️⃣ Nöbet Listesi Oluştur</h5>
                <p className="text-white-50">Hazırlanan nöbet listesini seçerek algoritmayı çalıştırın.</p>
                <a href="/create-schedule" className="btn btn-success w-50">
                  Listeyi Oluştur
                </a>
              </div>
            </div>
          </div>

          {/* 5. Bekleme Süreci */}
          <div className="col-md-4">
            <div className="card shadow-lg bg-warning text-dark rounded-4 transition-card">
              <div className="card-body text-center">
                <h5 className="fw-bold">5️⃣ Algoritma Çalışırken Bekleyin</h5>
                <p className="text-dark p-3">Seçilen listeye göre algoritma nöbet listesini oluşturacaktır.</p>
              </div>
            </div>
          </div>

          {/* 6. Kayıtlı Nöbet Listeleri */}
          <div className="col-md-4">
            <div className="card shadow-lg bg-dark text-white rounded-4 transition-card">
              <div className="card-body text-center">
                <h5 className="fw-bold">6️⃣ Kayıtlı Nöbet Listeleri</h5>
                <p className="text-white-50">Oluşturulan nöbet listesinin detaylarını görüntüleyin.</p>
                <a href="/schedule-lists" className="btn btn-success w-50">
                  Listelere Git
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}
