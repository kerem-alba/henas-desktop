import React, { useState, useEffect } from "react";
import Slider from "rc-slider";
import { getSettings, updateSettings } from "../services/apiService";
import "rc-slider/assets/index.css";

const generationMap = {
  1: 2000,
  2: 15000,
  3: 30000,
  4: 60000,
  5: 120000,
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
        <div className="bg-dark p-3 rounded text-light">
          <p className="mb-2 fs-5 fw-bold"> Önerilen Çözüm Kalitesi</p>
          <p className="mb-2">
            <strong>4</strong> seviyesi en verimli sonuçları verir. Başarı puanı düşük kalırsa <strong>5</strong> denenebilir.
          </p>

          <p className="mb-2 fs-6 fw-bold">⏱️ Ortalama Çözüm Süreleri</p>
          <ul className="mb-3" style={{ paddingLeft: "1rem" }}>
            <li>
              <strong>Seviye 1:</strong> &lt; 10 saniye
            </li>
            <li>
              <strong>Seviye 2:</strong> 10 - 30 saniye
            </li>
            <li>
              <strong>Seviye 3:</strong> 30 saniye - 1 dakika
            </li>
            <li>
              <strong>Seviye 4:</strong> 1 - 2 dakika
            </li>
            <li>
              <strong>Seviye 5:</strong> 2 - 4 dakika
            </li>
          </ul>

          <p className="mb-0">
            Süreler, bilgisayarınızın <strong>işlemci hızı</strong> ve <strong>donanım performansına</strong> göre değişebilir.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Settings;
