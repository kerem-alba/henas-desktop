import React from "react";
import "./styles.css";
import { useState, useEffect } from "react";

const LeavesTable = ({ doctorId, mandatoryLeaves, optionalLeaves, setMandatoryLeaves, setOptionalLeaves, daysInMonth }) => {
  const [daysCount, setDaysCount] = useState(31);

  useEffect(() => {
    if (daysInMonth) {
      setDaysCount(daysInMonth);
    }
  }, [daysInMonth]);

  const days = Array.from({ length: daysCount }, (_, i) => i + 1);
  const shifts = ["Gündüz", "Gece"];

  // Hücrenin zorunlu/opsiyonel mi olduğunu bulalım
  const getShiftStatus = (day, shiftType) => {
    const shiftIndex = shifts.indexOf(shiftType);
    if (mandatoryLeaves.some((m) => m[0] === doctorId && m[1] === day && m[2] === shiftIndex)) {
      return "mandatory";
    }
    if (optionalLeaves.some((o) => o[0] === doctorId && o[1] === day && o[2] === shiftIndex)) {
      return "optional";
    }
    return null;
  };

  // Tıklayınca parent’taki mandatory/optional dizilerini güncelleyelim
  const toggleShift = (day, shiftType) => {
    const shiftIndex = shifts.indexOf(shiftType);

    const isMandatory = mandatoryLeaves.some((m) => m[0] === doctorId && m[1] === day && m[2] === shiftIndex);
    const isOptional = optionalLeaves.some((o) => o[0] === doctorId && o[1] === day && o[2] === shiftIndex);

    // Mandatory -> Optional
    if (isMandatory) {
      setMandatoryLeaves((prev) => prev.filter((m) => !(m[0] === doctorId && m[1] === day && m[2] === shiftIndex)));
      setOptionalLeaves((prev) => [...prev, [doctorId, day, shiftIndex]]);
      return;
    }

    // Optional -> Sil
    if (isOptional) {
      setOptionalLeaves((prev) => prev.filter((o) => !(o[0] === doctorId && o[1] === day && o[2] === shiftIndex)));
      return;
    }

    // Boş -> Mandatory
    setMandatoryLeaves((prev) => [...prev, [doctorId, day, shiftIndex]]);
  };

  return (
    <div className="table-container">
      <div className="info-box">
        <span>
          <span className="info-square mandatory" /> Zorunlu İzin
        </span>
        <span>
          <span className="info-square optional" /> Opsiyonel İzin
        </span>
      </div>

      <table className="mini-table text-dark">
        <thead>
          <tr>
            <th></th>
            {days.map((day) => (
              <th key={day}>{day}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {shifts.map((shiftType) => (
            <tr key={shiftType}>
              <td>{shiftType}</td>
              {days.map((day) => {
                const status = getShiftStatus(day, shiftType);
                return (
                  <td
                    key={`${doctorId}-${day}-${shiftType}`}
                    className={status === "mandatory" ? "mandatory" : status === "optional" ? "optional" : ""}
                    onClick={() => toggleShift(day, shiftType)}
                  />
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default LeavesTable;
