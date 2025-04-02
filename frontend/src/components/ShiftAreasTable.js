import React, { useState } from "react";

const ShiftAreasTable = ({
  shiftAreas,
  handleShiftAreaNameChange,
  handleMinDoctorsPerAreaChange,
  handleSaveShiftAreaChanges,
  handleAddShiftArea,
  handleDeleteShiftArea,
}) => {
  const [newAreaName, setNewAreaName] = useState("");
  const [newMinDoctorsPerArea, setNewMinDoctorsPerArea] = useState(1);

  return (
    <div className="mt-5">
      <h3 className="text-center bg-dark text-white p-3 shadow-md rounded-4">Nöbet Alanları Listesi</h3>
      <table className="table table-dark table-striped table-hover shadow-md" style={{ borderRadius: "15px", overflow: "hidden" }}>
        <thead className="thead-dark">
          <tr className="align-middle">
            <th className="col-1 text-center">#</th>
            <th className="col-8">Nöbet Alanı</th>
            <th className="col-2">Min. Nöbetçi</th>
            <th className="col-1 text-center">İşlem</th>
          </tr>
        </thead>
        <tbody>
          {shiftAreas.map((area, index) => (
            <tr key={area.id || index}>
              <td className="text-center">
                <div className="mt-2">{index + 1}</div>
              </td>
              <td>
                <input
                  type="text"
                  className="form-control bg-secondary text-white"
                  value={area.area_name}
                  onChange={(e) => handleShiftAreaNameChange(index, e.target.value)}
                />
              </td>
              <td>
                <input
                  type="number"
                  className="form-control bg-secondary text-white"
                  value={area.min_doctors_per_area}
                  onChange={(e) => handleMinDoctorsPerAreaChange(index, e.target.value)}
                />
              </td>
              <td className="text-center align-middle">
                <button className="btn btn-danger btn-sm ms-auto" onClick={() => handleDeleteShiftArea(area.id)} disabled={!area.id}>
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
                value={newAreaName}
                onChange={(e) => setNewAreaName(e.target.value)}
                placeholder="Yeni nöbet alanı adı"
              />
            </td>
            <td>
              <input
                type="number"
                className="form-control me-2"
                value={newMinDoctorsPerArea}
                onChange={(e) => setNewMinDoctorsPerArea(e.target.value)}
                placeholder="Min. nöbetçi sayısı"
              />
            </td>
            <td className="text-center align-middle">
              <button
                className="btn btn-success btn-sm ms-auto"
                type="button"
                style={{ cursor: "pointer" }} // Butona cursor: pointer ekliyoruz
                onClick={() => {
                  if (newAreaName.trim() !== "") {
                    handleAddShiftArea(newAreaName, newMinDoctorsPerArea);
                    setNewAreaName("");
                    setNewMinDoctorsPerArea(1);
                  }
                }}
                disabled={newAreaName.trim() === ""}
              >
                <i className="bi bi-plus-lg"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <button className="btn btn-success w-100 shadow-md rounded-3" onClick={handleSaveShiftAreaChanges} disabled={shiftAreas.length === 0}>
        Değişiklikleri Kaydet
      </button>
    </div>
  );
};

export default ShiftAreasTable;
