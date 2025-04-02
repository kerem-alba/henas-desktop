import React, { useState, useEffect } from "react";
import { getAllScheduleData, getScheduleDataById, runAlgorithm } from "../services/apiService";
import ScheduleResultTable from "../components/ScheduleResultTable";
import ScheduleDoctorSummaryTable from "../components/ScheduleDoctorSummaryTable";
import LogMessagesTable from "../components/LogMessagesTable";
import Footer from "../components/Footer";

const CreateSchedule = () => {
  const [schedules, setSchedules] = useState([]);
  const [selectedScheduleId, setSelectedScheduleId] = useState(null);
  const [scheduleData, setScheduleData] = useState(null);
  const [algorithmResult, setAlgorithmResult] = useState(null);
  const [selectedDoctorCode, setSelectedDoctorCode] = useState(null);
  const [scheduleId, setScheduleId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [hasRunAlgorithm, setHasRunAlgorithm] = useState(false);

  // Geçici bildirim mesajı (toast) için state
  const [notification, setNotification] = useState("");

  useEffect(() => {
    const fetchSchedules = async () => {
      try {
        const allSchedules = await getAllScheduleData();
        setSchedules(allSchedules);
      } catch (error) {
        console.error("Nöbet listeleri alınırken hata oluştu:", error);
      }
    };
    fetchSchedules();
  }, []);

  useEffect(() => {
    const fetchSelectedSchedule = async () => {
      if (!selectedScheduleId) {
        setScheduleData(null);
        return;
      }
      try {
        const data = await getScheduleDataById(selectedScheduleId);
        setScheduleData(data);
      } catch (error) {
        console.error("Seçili nöbet listesi alınırken hata oluştu:", error);
      }
    };
    fetchSelectedSchedule();
  }, [selectedScheduleId]);

  // notification her değiştiğinde 3 saniye sonra otomatik silinsin
  useEffect(() => {
    if (notification) {
      const timer = setTimeout(() => {
        setNotification("");
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [notification]);

  const handleCreateSchedule = async () => {
    if (!scheduleData) {
      setNotification("Lütfen bir nöbet listesi seçin!");
      return;
    }
    setHasRunAlgorithm(true);
    setLoading(true);
    setAlgorithmResult(null);

    try {
      const { schedule, schedule_id } = await runAlgorithm(selectedScheduleId);

      setAlgorithmResult(schedule[0][0]);
      setScheduleId(schedule_id);
      // Klasik alert yerine notification:
      setNotification("Nöbet listesi başarıyla oluşturuldu!");
    } catch (error) {
      console.error("Hata:", error);
      setNotification("Nöbet listesi oluşturulamadı!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="d-flex flex-column background-gradient min-vh-100">
      <div className="container-fluid p-5 flex-grow-1">
        <h2 className="fw-bold display-6 text-black ms-3 mb-4">Nöbet Listesi Oluştur</h2>

        {/* Toast (geçici bildirim) */}
        {notification && (
          <div className="position-fixed top-0 start-50 translate-middle-x p-3" style={{ zIndex: 9999 }}>
            <div className="toast show align-items-center text-white bg-success border-0">
              <div className="d-flex">
                <div className="toast-body">{notification}</div>
                <button type="button" className="btn-close btn-close-white me-2 m-auto" onClick={() => setNotification("")} />
              </div>
            </div>
          </div>
        )}

        <div className="row justify-content-center">
          <div className="col-md-4 col-12 mb-3">
            <div className="card bg-dark text-white p-3 rounded-4">
              <h5>Kayıtlı Nöbet Listesi Verileri</h5>
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

              <button className="btn btn-primary mt-3 w-100" onClick={handleCreateSchedule} disabled={loading}>
                {loading ? "Nöbet Listesi Oluşturuluyor..." : "Nöbet Listesi Oluştur"}
              </button>
            </div>
          </div>
        </div>

        <div className="text-center mt-4">
          {!hasRunAlgorithm && !loading && !algorithmResult && <p className="text-muted">Henüz algoritma çalıştırılmadı.</p>}
          {loading && (
            <>
              <div className="spinner-border text-danger fs-3" role="status"></div>
              <p className="mt-2">Nöbet listesi oluşturuluyor, lütfen bekleyin...</p>
            </>
          )}
        </div>

        <ScheduleResultTable schedule={algorithmResult} selectedDoctorCode={selectedDoctorCode} />
        <div className="row">
          <div className="col-md-6">
            <ScheduleDoctorSummaryTable scheduleData={scheduleData} algorithmResult={algorithmResult} setSelectedDoctorCode={setSelectedDoctorCode} />
          </div>
          <div className="col-md-6">
            <LogMessagesTable schedule_id={scheduleId} />
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default CreateSchedule;
