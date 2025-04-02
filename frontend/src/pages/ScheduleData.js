import React, { useState, useEffect } from "react";
import { getDoctors, getDetailedSeniorities } from "../services/apiService";
import { getAllScheduleData, getScheduleDataById, deleteScheduleData } from "../services/apiService";
import ScheduleTable from "../components/ScheduleTable";
import Footer from "../components/Footer";

const ScheduleData = () => {
  const [doctors, setDoctors] = useState([]);
  const [detailedSeniorities, setDetailedSeniorities] = useState([]);
  const [schedules, setSchedules] = useState([]);
  const [selectedScheduleId, setSelectedScheduleId] = useState(null);
  const [scheduleData, setScheduleData] = useState(null);
  const [isNewScheduleActive, setIsNewScheduleActive] = useState(false);
  const [month, setMonth] = useState("");
  const [year, setYear] = useState("");

  useEffect(() => {
    const fetchBaseData = async () => {
      try {
        const [doctorsData, detailedSenioritiesData] = await Promise.all([getDoctors(), getDetailedSeniorities()]);
        setDoctors(doctorsData);
        setDetailedSeniorities(detailedSenioritiesData);
      } catch (error) {
        console.error("Tüm veriler çekilirken hata oluştu:", error);
      }
    };
    fetchBaseData();
  }, []);

  useEffect(() => {
    const fetchSchedules = async () => {
      try {
        const allSchedules = await getAllScheduleData();
        setSchedules(allSchedules);
      } catch (error) {
        console.error("Schedule listesi alınırken hata:", error);
      }
    };
    fetchSchedules();
  }, []);

  useEffect(() => {
    const fetchSelectedSchedule = async () => {
      if (!selectedScheduleId) return;
      try {
        const data = await getScheduleDataById(selectedScheduleId);
        setIsNewScheduleActive(false);
        setScheduleData(data);
      } catch (error) {
        console.error("Seçili schedule verisi alınırken hata:", error);
      }
    };
    fetchSelectedSchedule();
  }, [selectedScheduleId]);

  const handleNewSchedule = () => {
    setSelectedScheduleId(null);
    setScheduleData(null);
    setIsNewScheduleActive(!isNewScheduleActive);
  };

  const handleDeleteSchedule = async () => {
    if (!selectedScheduleId) {
      alert("Lütfen silmek için bir nöbet listesi seçin!");
      return;
    }

    const confirmDelete = window.confirm("Bu nöbet listesini silmek istediğinize emin misiniz?");
    if (!confirmDelete) return;

    try {
      await deleteScheduleData(selectedScheduleId);
      alert("Nöbet listesi başarıyla silindi!");
      const updatedSchedules = await getAllScheduleData();
      setSchedules(updatedSchedules);
      setSelectedScheduleId(null);
      setScheduleData(null);
    } catch (error) {
      console.error("Nöbet listesi silinirken hata oluştu:", error);
      alert("Silme işlemi başarısız oldu!");
    }
  };

  const calculateMonthInfo = () => {
    if (!month || !year) return { firstDay: "", daysInMonth: "" };

    const firstDay = new Date(year, month - 1, 1).toLocaleDateString("tr-TR", { weekday: "long" });
    const daysInMonth = new Date(year, month, 0).getDate();

    return { firstDay, daysInMonth };
  };

  const { firstDay, daysInMonth } = calculateMonthInfo();

  return (
    <div className="d-flex flex-column min-vh-100 background-gradient ">
      <div className="container-fluid p-5 flex-grow-1">
        <h2 className="fw-bold display-6 text-black ms-3 mb-4">Nöbet Listesi Verileri</h2>

        <div className="row justify-content-center">
          <div className="col-lg-3 col-12 mb-3" style={{ maxWidth: "350px" }}>
            <div className="card bg-dark text-white p-3 mb-3 mt-4 rounded-4">
              <h5>Nöbet Listesi Verileri</h5>
              <select className="form-select mt-2" value={selectedScheduleId || ""} onChange={(e) => setSelectedScheduleId(e.target.value)}>
                <option value="" disabled>
                  Seçiniz...
                </option>
                {schedules.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name}
                  </option>
                ))}
              </select>

              <button className={`btn mt-3 ${isNewScheduleActive ? "btn-success" : "btn-secondary"}`} onClick={handleNewSchedule}>
                Yeni Nöbet Listesi Verisi Ekle
              </button>

              {isNewScheduleActive && (
                <div className="mt-3 p-3 bg-secondary rounded-3">
                  <label className="form-label">Ay Seçin</label>
                  <select className="form-select" value={month} onChange={(e) => setMonth(e.target.value)}>
                    <option value="" disabled>
                      Seçiniz...
                    </option>
                    {Array.from({ length: 12 }, (_, i) => (
                      <option key={i + 1} value={i + 1}>
                        {new Date(0, i).toLocaleDateString("tr-TR", { month: "long" })}
                      </option>
                    ))}
                  </select>

                  <label className="form-label mt-2">Yıl Seçin</label>
                  <input type="number" className="form-control" value={year} onChange={(e) => setYear(e.target.value)} placeholder="Yıl" min="2024" />
                </div>
              )}

              <button className="btn btn-danger mt-3 w-100" onClick={handleDeleteSchedule} disabled={!selectedScheduleId}>
                Seçili Nöbet Listesi Verisini Sil
              </button>
            </div>
          </div>

          <div className="col-lg-9 col-12">
            <ScheduleTable
              doctors={doctors}
              detailedSeniorities={detailedSeniorities}
              scheduleData={scheduleData}
              firstDay={firstDay}
              daysInMonth={daysInMonth}
            />
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default ScheduleData;
