import React, { useState } from "react";

const DoctorTable = ({ doctors, seniorities, handleNameChange, handleSeniorityChange, handleSaveChanges, handleAddDoctor, handleDeleteDoctor }) => {
  const [newDoctorName, setNewDoctorName] = useState("");
  const [newDoctorSeniority, setNewDoctorSeniority] = useState("");

  return (
    <div className="mb-4">
      <h3 className="text-center bg-dark text-white p-3 shadow-md rounded-4">Doktorlar Listesi</h3>
      <table className="table table-dark table-striped table-hover shadow-md" style={{ borderRadius: "15px", overflow: "hidden" }}>
        <thead className="thead-dark">
          <tr className="align-middle">
            <th className="text-center">#</th>
            <th>Ad</th>
            <th>Kıdem</th>
            <th className="text-center">İşlem</th>
          </tr>
        </thead>
        <tbody>
          {doctors.map((doctor, index) => (
            <tr className="text-center" key={doctor.id || index}>
              <td className="align-middle">{index + 1}</td>
              <td>
                <input
                  type="text"
                  className="form-control bg-secondary text-white"
                  value={doctor.name}
                  onChange={(e) => handleNameChange(index, e.target.value)}
                />
              </td>
              <td>
                <select
                  className="form-select bg-secondary text-white"
                  value={seniorities.find((s) => s.name === doctor.seniority_name)?.id || ""}
                  onChange={(e) => handleSeniorityChange(index, e.target.value)}
                >
                  <option className="bg-light" disabled value="">
                    Kıdem Seç
                  </option>
                  {seniorities.map((seniority) => (
                    <option key={seniority.id} value={seniority.id}>
                      {seniority.name}
                    </option>
                  ))}
                </select>
              </td>
              <td className="align-middle text-center ">
                <button
                  className="btn btn-danger btn-sm rounded"
                  onClick={() => handleDeleteDoctor(doctor.id)}
                  disabled={!doctor.id}
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  title="Doktoru Sil"
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
                value={newDoctorName}
                onChange={(e) => setNewDoctorName(e.target.value)}
                placeholder="Yeni doktor adı"
              />
            </td>
            <td>
              <select className="form-select" value={newDoctorSeniority} onChange={(e) => setNewDoctorSeniority(e.target.value)}>
                <option disabled value="">
                  Kıdem Seç
                </option>
                {seniorities.map((seniority) => (
                  <option key={seniority.id} value={seniority.id}>
                    {seniority.name}
                  </option>
                ))}
              </select>
            </td>
            <td className="text-center align-middle">
              <button
                className="btn btn-success btn-sm"
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                title="Yeni Doktor Ekle"
                onClick={() => {
                  if (newDoctorName.trim() !== "" && newDoctorSeniority !== "") {
                    handleAddDoctor(newDoctorName, newDoctorSeniority);
                    setNewDoctorName("");
                    setNewDoctorSeniority("");
                  }
                }}
                disabled={newDoctorName.trim() === "" || newDoctorSeniority === ""}
              >
                <i className="bi bi-plus-lg"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <button className="btn btn-success w-100 shadow-md rounded-3" onClick={handleSaveChanges} disabled={doctors.length === 0}>
        Değişiklikleri Kaydet
      </button>
    </div>
  );
};

export default DoctorTable;
