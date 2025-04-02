import React from "react";

// 1. Fitness Score'u 10 sabit dilime ayıran fonksiyon.
const getFitnessStage = (score) => {
  if (score < -1000) return 1;
  if (score < 0) return 2;
  if (score < 100) return 3;
  if (score < 200) return 4;
  if (score < 300) return 5;
  if (score < 400) return 6;
  if (score < 500) return 7;
  if (score < 600) return 8;
  if (score < 800) return 9;
  return 10; // 800-1000 (ve üstü)
};

// 2. Aşamalara (1-10) karşılık gelen renkler.
const colors = [
  "#FF0000", // 1 - Kırmızı
  "#FF4000", // 2 - Koyu Turuncu
  "#FF8000", // 3 - Turuncu
  "#FFBF00", // 4 - Açık Turuncu
  "#FFFF00", // 5 - Sarı
  "#BFFF00", // 6 - Açık Yeşilimsi Sarı
  "#80FF00", // 7 - Açık Yeşil
  "#40FF00", // 8 - Yeşil
  "#00FF40", // 9 - Canlı Yeşil
  "#00FF00", // 10 - En Yeşil
];

const FitnessScoreIndicator = ({ fitnessScore }) => {
  // Hangi aşamada olduğumuzu bul
  const stage = getFitnessStage(fitnessScore);

  return (
    <div>
      <h5>Başarı Oranı</h5>

      {/* Başarısızsa uyarı */}
      {fitnessScore < -1000 && <div className="text-danger fw-bold mt-2 mb-2">Başarısız </div>}

      {/* 10 parçadan oluşan gösterge */}
      <div style={{ display: "flex", gap: "4px", marginTop: "5px" }}>
        {Array.from({ length: 10 }, (_, i) => (
          <div
            key={i}
            style={{
              width: "20px",
              height: "20px",
              backgroundColor: i < stage ? colors[i] : "#444", // Aktif olanlar renkli, pasif olanlar gri
              borderRadius: "4px",
              transition: "background 0.3s ease",
            }}
          />
        ))}
      </div>

      {/* Skor metni */}
      <p className="mt-2 mb-0">Skor: {fitnessScore}/1000</p>
    </div>
  );
};

export default FitnessScoreIndicator;
