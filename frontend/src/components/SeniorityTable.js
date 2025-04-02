import React, { useState } from "react";
import DraggableShiftAreaList from "./DraggableShiftAreaList"; // Alt bileşen (aşağıda)

const SeniorityTable = ({
  detailedSeniorities,
  shiftAreas,
  handleMaxShiftsChange,
  handleSeniorityNameChange,
  handleSaveSeniorityChanges,
  handleAddSeniority,
  handleDeleteSeniority,
}) => {
  const [newSeniorityName, setNewSeniorityName] = useState("");
  const [newMaxShifts, setNewMaxShifts] = useState("");

  console.log("detailedSeniorities", detailedSeniorities);
  console.log("shiftAreas", shiftAreas);

  return (
    <div className="mb-4">
      <h3 className="text-center bg-dark text-white p-3 shadow-md rounded-4">Kıdem Listesi</h3>
      <table className="table table-dark table-striped table-hover shadow-md" style={{ borderRadius: "15px", overflow: "hidden" }}>
        <thead className="thead-dark">
          <tr className="align-middle">
            <th className="col-1 text-center">#</th>
            <th className="col-4">Kıdem Adı</th>
            <th className="col-2"> Max Nöbet</th>
            <th className="col-4">Nöbet Alanları</th>
            <th className="col-1 text-center">İşlem</th>
          </tr>
        </thead>
        <tbody>
          {detailedSeniorities.map((seniority, index) => (
            <tr key={seniority.id}>
              <td className="text-center">
                <div className="mt-2">{index + 1}</div>
              </td>
              <td>
                <input
                  type="text"
                  className="form-control bg-secondary text-white"
                  value={seniority.seniority_name}
                  onChange={(e) => handleSeniorityNameChange(index, e.target.value)}
                />
              </td>
              <td>
                <input
                  type="number"
                  className="form-control bg-secondary text-white"
                  value={seniority.max_shifts_per_month}
                  onChange={(e) => handleMaxShiftsChange(index, e.target.value)}
                />
              </td>
              <td>
                <DraggableShiftAreaList
                  allShiftAreas={shiftAreas}
                  activeAreaNames={seniority.shift_area_names}
                  onUpdate={(updatedActiveNames) => {
                    seniority.shift_area_names = updatedActiveNames;
                  }}
                />
              </td>

              <td className="text-center ">
                <button
                  className="btn btn-danger btn-sm rounded"
                  onClick={() => handleDeleteSeniority(seniority.id)}
                  disabled={!seniority.id}
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="Kıdem Sil"
                >
                  <i className="bi bi-trash"></i>
                </button>
              </td>
            </tr>
          ))}

          <tr className="table-success">
            <td className="fw-bold text-center align-middle">+</td>
            <td>
              <input
                type="text"
                className="form-control"
                value={newSeniorityName}
                onChange={(e) => setNewSeniorityName(e.target.value)}
                placeholder="Yeni kıdem adı"
              />
            </td>
            <td>
              <input
                type="number"
                className="form-control"
                value={newMaxShifts}
                onChange={(e) => setNewMaxShifts(e.target.value)}
                placeholder="Max nöbet"
              />
            </td>
            <td></td>
            <td className="text-center align-middle">
              <button
                className="btn btn-success btn-sm"
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                title="Kıdem Ekle"
                onClick={() => {
                  if (newSeniorityName.trim() !== "" && newMaxShifts !== "") {
                    handleAddSeniority(newSeniorityName, newMaxShifts);
                    setNewSeniorityName("");
                    setNewMaxShifts("");
                  }
                }}
                disabled={newSeniorityName.trim() === "" || newMaxShifts === ""}
              >
                <i className="bi bi-plus-lg"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <button className="btn btn-success w-100 shadow-md rounded-3" onClick={handleSaveSeniorityChanges} disabled={detailedSeniorities.length === 0}>
        Değişiklikleri Kaydet
      </button>
    </div>
  );
};

export default SeniorityTable;
