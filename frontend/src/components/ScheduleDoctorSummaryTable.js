import React from "react";

const ScheduleDoctorSummaryTable = ({ scheduleData, algorithmResult, setSelectedDoctorCode }) => {
  if (!scheduleData || !scheduleData.data) return null;

  return (
    <div className="mt-4">
      <h4 className="text-center bg-dark text-white p-2 rounded-3">Nöbet Özeti</h4>
      <table className="table table-dark table-striped table-hover shadow-md">
        <thead>
          <tr>
            <th className="text-center">Doktor Kodu</th>
            <th className="text-center">Doktor Adı</th>
            <th className="text-center">Toplam Nöbet</th>
            <th className="text-center">Gündüz Nöbet</th>
            <th className="text-center">Gece Nöbet</th>
          </tr>
        </thead>
        <tbody>
          {[...scheduleData.data]
            .sort((a, b) => a.code.localeCompare(b.code))
            .map((doctor) => {
              let dayShiftCount = 0;
              let nightShiftCount = 0;

              if (algorithmResult) {
                algorithmResult.forEach((day) => {
                  if (day[0].includes(doctor.code)) dayShiftCount++;
                  if (day[1].includes(doctor.code)) nightShiftCount++;
                });
              } else {
                dayShiftCount = "-";
                nightShiftCount = "-";
              }

              return (
                <tr key={doctor.code} onClick={() => setSelectedDoctorCode(doctor.code)} style={{ cursor: "pointer" }}>
                  <td className="text-center">{doctor.code}</td>
                  <td className="text-center">{doctor.name}</td>
                  <td className="text-center">{doctor.shift_count}</td>
                  <td className="text-center">{dayShiftCount}</td>
                  <td className="text-center">{nightShiftCount}</td>
                </tr>
              );
            })}
        </tbody>
      </table>
    </div>
  );
};

export default ScheduleDoctorSummaryTable;
