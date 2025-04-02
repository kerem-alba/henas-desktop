import React, { useState, useEffect } from "react";
import Slider from "rc-slider";
import { getSettings, updateSettings } from "../services/apiService";
import "rc-slider/assets/index.css";

const generationMap = {
  1: 2000,
  2: 8000,
  3: 15000,
  4: 40000,
  5: 80000,
};

const Settings = () => {
  const [qualityLevel, setQualityLevel] = useState(2); // Varsayılan seviye: 3 (10000)

  useEffect(() => {
    getSettings()
      .then((data) => {
        const mappedLevel = Object.keys(generationMap).find((key) => generationMap[key] === data.max_generations);
        setQualityLevel(mappedLevel ? Number(mappedLevel) : 3);
      })
      .catch((err) => {
        console.error("Ayarları alırken hata oluştu:", err);
      });
  }, []);

  const handleSave = () => {
    updateSettings(generationMap[qualityLevel])
      .then(() => alert("Çözüm kalitesi güncellendi!"))
      .catch((err) => console.error("Ayarları kaydederken hata oluştu:", err));
  };

  return (
    <div className="d-flex flex-column pt-5 align-items-center min-vh-100 bg-light background-gradient">
      <div className="text-center p-4 bg-dark shadow rounded" style={{ width: "300px" }}>
        <h4 className="pb-3">Çözüm Kalitesi</h4>
        <Slider
          min={1}
          max={5}
          step={1}
          value={qualityLevel}
          onChange={(value) => setQualityLevel(value)}
          marks={{
            1: "1",
            2: "2",
            3: "3",
            4: "4",
            5: "5",
          }}
          styles={{
            track: { backgroundColor: "#007bff", height: 8 },
            handle: { borderColor: "#007bff", height: 20, width: 20, backgroundColor: "#007bff" },
            rail: { backgroundColor: "#ddd", height: 8 },
          }}
        />
        <button className="btn btn-primary mt-5" onClick={handleSave}>
          Kaydet
        </button>
      </div>
      <div className="card mt-4 p-3 bg-dark shadow rounded">
        <p className="text-light mb-1">Çözüm kalitesi arttıkça, algoritma daha iyi sonuçlar bulacaktır.</p>
        <p className="text-light mb-1">
          Ancak, backend’in deploy edildiği <strong>Render</strong> ortamında sınırlamalar olduğu için süre artmaktadır.
        </p>
        <p className="text-light">
          <strong>Yerel ortamda </strong> algoritma çalışma süresi maksimum 2 dakika sürerken, <strong> Render’da 20 dakikaya</strong> kadar
          çıkabiliyor.
        </p>
        <p className="fw-bold text-danger">
          ⚠️ Test amaçlı kullanımda <strong>1 veya 2</strong> kalite seviyesi önerilir.
        </p>
      </div>
    </div>
  );
};

export default Settings;
