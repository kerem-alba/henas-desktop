import { useEffect, useState } from "react";
import { getSchedules, getScheduleById, getScheduleDataById, deleteScheduleById } from "../services/apiService";
import ScheduleResultTable from "../components/ScheduleResultTable";
import ScheduleDoctorSummaryTable from "../components/ScheduleDoctorSummaryTable";
import LogMessagesTable from "../components/LogMessagesTable";
import ScoreIndicator from "../components/ScoreIndicator";
import Footer from "../components/Footer";

const ScheduleLists = () => {
  const [savedSchedules, setSavedSchedules] = useState([]);
  const [schedule, setSchedule] = useState(null);
  const [fitnessScore, setFitnessScore] = useState(null);
  const [schedule_id, setSchedule_id] = useState(null);
  const [selectedDoctorCode, setSelectedDoctorCode] = useState(null);
  const [scheduleData, setScheduleData] = useState(null);
  const [firstDay, setFirstDay] = useState(null);

  useEffect(() => {
    const fetchSchedules = async () => {
      try {
        const data = await getSchedules();
        setSavedSchedules(data);
      } catch (error) {
        console.error("Nöbet listelerini getirirken hata oluştu:", error);
      }
    };
    fetchSchedules();
  }, []);

  const handleSelectSchedule = async (selectedId) => {
    if (!selectedId) return;

    const selectedSchedule = savedSchedules.find((item) => item.id === parseInt(selectedId));

    if (!selectedSchedule) {
      console.error("Seçilen schedule bulunamadı. ID:", selectedId);
      return;
    }

    const { schedule_data_id } = selectedSchedule;
    console.log("Selected schedule_data_id:", schedule_data_id);

    // Seçilen schedule'ın detaylarını getir
    const scheduleResult = await getScheduleById(selectedId);

    // schedule_data_id ile ek veriyi al
    let scheduleDataResponse = null;
    if (schedule_data_id) {
      scheduleDataResponse = await getScheduleDataById(schedule_data_id);
      console.log("scheduleDataResponse:", scheduleDataResponse);
    }

    setSchedule(scheduleResult.schedule);
    setFitnessScore(scheduleResult.fitness_score);
    setSchedule_id(scheduleResult.id);
    setScheduleData(scheduleDataResponse);
    setFirstDay(scheduleDataResponse.first_day);
  };

  const handleDeleteSchedule = async () => {
    if (!schedule_id) {
      alert("Lütfen silmek için bir nöbet listesi seçin!");
      return;
    }

    try {
      await deleteScheduleById(schedule_id);
      alert("Nöbet listesi başarıyla silindi!");
      window.location.reload();
    } catch (error) {
      console.error("Nöbet listesi silinirken hata oluştu:", error);
    }
  };

  return (
    <div className="d-flex flex-column min-vh-100 background-gradient">
      <div className="container-fluid p-5 flex-grow-1">
        <h2 className="fw-bold display-6 text-black ms-3 mb-4">Nöbet Listeleri</h2>
        <div className="row justify-content-center">
          <div className="d-flex flex-wrap gap-5 justify-content-center">
            <div className="card bg-dark text-white p-3 rounded-4" style={{ minWidth: "300px" }}>
              <h5>Kayıtlı Nöbet Listeleri</h5>
              <select onChange={(e) => handleSelectSchedule(e.target.value)} className="form-select mt-2">
                <option value="">Seçiniz...</option>
                {savedSchedules.map((sch) => (
                  <option key={sch.id} value={sch.id}>
                    {`${sch.schedule_data_name} (Score: ${sch.fitness_score})`}
                  </option>
                ))}
              </select>

              <button className="btn btn-danger mt-3" onClick={handleDeleteSchedule} disabled={!schedule_id}>
                Seçili Nöbet Listesini Sil
              </button>
            </div>

            {fitnessScore !== null && (
              <div className="card bg-dark text-white p-3 rounded-4" style={{ minWidth: "200px" }}>
                <ScoreIndicator fitnessScore={fitnessScore} />
              </div>
            )}
          </div>
        </div>

        {schedule && (
          <>
            <ScheduleResultTable schedule={schedule} selectedDoctorCode={selectedDoctorCode} firstDay={firstDay} />

            <div className="row">
              <div className="col-md-6">
                <ScheduleDoctorSummaryTable scheduleData={scheduleData} algorithmResult={schedule} setSelectedDoctorCode={setSelectedDoctorCode} />
              </div>
              <div className="col-md-6">
                <LogMessagesTable schedule_id={schedule_id} />
              </div>
            </div>
          </>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default ScheduleLists;
