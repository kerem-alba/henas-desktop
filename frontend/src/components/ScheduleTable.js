import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import LeavesTable from "./LeavesTable";
import { addScheduleData, updateScheduleData, getAllScheduleData } from "../services/apiService";

const ScheduleTable = ({ doctors, detailedSeniorities, scheduleData, firstDay, daysInMonth }) => {
  const [scheduleName, setScheduleName] = useState("");
  const [doctorCodes, setDoctorCodes] = useState({});
  const [localShiftCounts, setLocalShiftCounts] = useState({});
  const [mandatoryLeaves, setMandatoryLeaves] = useState([]);
  const [optionalLeaves, setOptionalLeaves] = useState([]);
  const [expandedRow, setExpandedRow] = useState(null);

  const navigate = useNavigate(); // Navigate fonksiyonunu tanımla

  const tableTitle = scheduleData ? scheduleData.name : "Yeni Nöbet Listesi Verisi Ekle";

  useEffect(() => {
    if (scheduleData && scheduleData.data) {
      setScheduleName(scheduleData.name || "");

      const newDoctorCodes = {};
      const newLocalShiftCounts = {};
      const newMandatory = [];
      const newOptional = [];

      scheduleData.data.forEach((schedDoc) => {
        const matchedDoctor = doctors.find((d) => d.name === schedDoc.name);
        if (matchedDoctor) {
          newDoctorCodes[matchedDoctor.id] = schedDoc.code || "";
          const docIndex = doctors.findIndex((d) => d.id === matchedDoctor.id);
          newLocalShiftCounts[docIndex] = schedDoc.shift_count || 0;

          if (schedDoc.mandatory_leaves) {
            schedDoc.mandatory_leaves.forEach(([day, shiftIndex]) => {
              newMandatory.push([matchedDoctor.id, day, shiftIndex]);
            });
          }
          if (schedDoc.optional_leaves) {
            schedDoc.optional_leaves.forEach(([day, shiftIndex]) => {
              newOptional.push([matchedDoctor.id, day, shiftIndex]);
            });
          }
        }
      });

      setDoctorCodes(newDoctorCodes);
      setLocalShiftCounts(newLocalShiftCounts);
      setMandatoryLeaves(newMandatory);
      setOptionalLeaves(newOptional);
    } else {
      // Yeni bir liste oluşturuluyorsa otomatik kod ataması yap
      setScheduleName("");
      const autoCodes = {};
      doctors.forEach((doctor, idx) => {
        autoCodes[doctor.id] = String.fromCharCode(65 + idx);
      });
      setDoctorCodes(autoCodes);
      setLocalShiftCounts({});
      setMandatoryLeaves([]);
      setOptionalLeaves([]);
    }
  }, [scheduleData, doctors]);

  // Kaydet veya Güncelle
  const handleSaveScheduleData = async () => {
    if (!scheduleName.trim()) {
      alert("Lütfen bir nöbet listesi adı girin!");
      return;
    }

    try {
      const existingSchedules = await getAllScheduleData();
      const isDuplicate = existingSchedules.some((s) => s.name.trim().toLowerCase() === scheduleName.trim().toLowerCase());

      if (!scheduleData && isDuplicate) {
        alert("Bu isimde bir nöbet listesi zaten mevcut! Lütfen farklı bir isim girin.");
        return;
      }

      const newScheduleData = doctors.map((doctor, index) => {
        const matchedSeniority = detailedSeniorities.find((s) => s.seniority_name === doctor.seniority_name);
        const shiftCount = localShiftCounts[index] || matchedSeniority?.max_shifts_per_month || 0;

        return {
          code: doctorCodes[doctor.id] || "",
          name: doctor.name,
          seniority_id: matchedSeniority?.id,
          shift_areas: matchedSeniority?.shift_area_ids,
          shift_count: shiftCount,
          mandatory_leaves: mandatoryLeaves.filter((leave) => leave[0] === doctor.id).map(([_, day, shiftIdx]) => [day, shiftIdx]),
          optional_leaves: optionalLeaves.filter((leave) => leave[0] === doctor.id).map(([_, day, shiftIdx]) => [day, shiftIdx]),
        };
      });

      if (scheduleData && scheduleData.id) {
        await updateScheduleData(scheduleData.id, scheduleName, newScheduleData);
        alert("Nöbet listesi başarıyla güncellendi!");
      } else {
        await addScheduleData(scheduleName, newScheduleData, firstDay, daysInMonth);
        alert("Nöbet listesi başarıyla kaydedildi!");
        navigate("/create-schedule");
      }

      setScheduleName("");
    } catch (error) {
      console.error("Nöbet listesi işlemi sırasında hata:", error);
      alert("İşlem başarısız oldu!");
    }
  };

  const toggleRow = (doctorId) => {
    setExpandedRow(expandedRow === doctorId ? null : doctorId);
  };

  if (!doctors.length) {
    return <div className="mt-4 text-center">Listelemek için doktor verisi yok.</div>;
  }

  return (
    <div className="mt-4 mx-auto">
      <h3 className="text-center bg-dark text-white p-3 shadow-md rounded-4">{tableTitle}</h3>

      <table className="table table-dark table-striped table-hover shadow-md" style={{ borderRadius: "15px", overflow: "hidden" }}>
        <thead className="thead-dark">
          <tr className="align-middle">
            <th className="col-1 text-center">#</th>
            <th className="col-1">Kod</th>
            <th className="col-2">Doktor Adı</th>
            <th className="col-1">Kıdem</th>
            <th className="col-1">Nöbet Alanları</th>
            <th className="col-1">Nöbet Sayısı</th>
            <th className="col-1 text-center">İzinler</th>
          </tr>
        </thead>
        <tbody>
          {doctors.map((doctor, index) => {
            const matchedSeniority = detailedSeniorities.find((s) => s.seniority_name === doctor.seniority_name);
            const shiftAreas = matchedSeniority?.shift_area_names.join(", ") || "Alan Yok";

            return (
              <React.Fragment key={doctor.id}>
                <tr className="align-middle">
                  <td className="align-middle text-center">{index + 1}</td>
                  <td>
                    <input
                      type="text"
                      className="form-control bg-secondary text-white"
                      value={doctorCodes[doctor.id] || ""}
                      onChange={(e) =>
                        setDoctorCodes((prev) => ({
                          ...prev,
                          [doctor.id]: e.target.value.toUpperCase(),
                        }))
                      }
                    />
                  </td>
                  <td>{doctor.name}</td>
                  <td>{doctor.seniority_name}</td>
                  <td>{shiftAreas}</td>
                  <td>
                    <input
                      type="number"
                      className="form-control bg-secondary text-white"
                      value={localShiftCounts[index] ?? matchedSeniority?.max_shifts_per_month ?? ""}
                      onChange={(e) => {
                        const newValue = Number(e.target.value);
                        setLocalShiftCounts((prev) => ({
                          ...prev,
                          [index]: newValue,
                        }));
                      }}
                    />
                  </td>
                  <td className="text-center">
                    <button className="btn btn-sm btn-outline-light" onClick={() => toggleRow(doctor.id)}>
                      {expandedRow === doctor.id ? "İzinleri Gizle" : "İzinleri Göster"}
                    </button>
                  </td>
                </tr>

                {expandedRow === doctor.id && (
                  <tr>
                    <td colSpan="7" className="p-0">
                      <div className="bg-light p-3">
                        <LeavesTable
                          doctorId={doctor.id}
                          mandatoryLeaves={mandatoryLeaves}
                          optionalLeaves={optionalLeaves}
                          setMandatoryLeaves={setMandatoryLeaves}
                          setOptionalLeaves={setOptionalLeaves}
                          daysInMonth={daysInMonth}
                        />
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            );
          })}
        </tbody>
      </table>

      {/* Kaydetme / Güncelleme Butonu */}
      <div className="d-flex align-items-center gap-2 mt-3">
        <input
          type="text"
          className="form-control"
          placeholder="Nöbet listesi adı girin..."
          value={scheduleName}
          onChange={(e) => setScheduleName(e.target.value)}
        />
        <button className={`btn shadow-md rounded-3 ${scheduleData ? "btn-warning" : "btn-success"}`} onClick={handleSaveScheduleData}>
          {scheduleData ? "Güncelle" : "Kaydet"}
        </button>
      </div>
    </div>
  );
};

export default ScheduleTable;
