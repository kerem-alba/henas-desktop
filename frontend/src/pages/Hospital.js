import React, { useState, useEffect } from "react";
import {
  getDoctors,
  getSeniorities,
  updateDoctors,
  getDetailedSeniorities,
  getShiftAreas,
  updatedSeniorities,
  updateShiftAreas,
  addShiftArea,
  deleteShiftArea,
  addDoctor,
  deleteDoctor,
  addSeniority,
  deleteSeniority,
} from "../services/apiService";
import DoctorTable from "../components/DoctorTable";
import SeniorityTable from "../components/SeniorityTable";
import ShiftAreasTable from "../components/ShiftAreasTable";
import Footer from "../components/Footer";
import "./styles.css";

const Hospital = () => {
  const [doctors, setDoctors] = useState([]);
  const [seniorities, setSeniorities] = useState([]);
  const [detailedSeniorities, setDetailedSeniorities] = useState([]);
  const [shiftAreas, setShiftAreas] = useState([]);

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        const [doctorsData, senioritiesData, detailedSenioritiesData, shiftAreasData] = await Promise.all([
          getDoctors(),
          getSeniorities(),
          getDetailedSeniorities(),
          getShiftAreas(),
        ]);

        console.log("Backend'den gelen detailedSenioritiesData:", detailedSenioritiesData);

        const sortedDoctors = doctorsData.sort((a, b) => a.id - b.id);

        const seniorityNames = senioritiesData.map((seniority) => ({
          id: seniority.id,
          name: seniority.seniority_name,
        }));

        setDoctors(sortedDoctors);
        setSeniorities(seniorityNames);
        setDetailedSeniorities(detailedSenioritiesData);
        setShiftAreas(shiftAreasData);
      } catch (error) {
        console.error("Tüm veriler çekilirken hata oluştu:", error);
      }
    };

    fetchAllData();
  }, []);

  const handleSeniorityChange = (index, newSeniorityId) => {
    setDoctors((prevDoctors) => {
      const updatedDoctors = [...prevDoctors];
      const matched = seniorities.find((s) => s.id === parseInt(newSeniorityId, 10));
      if (matched) {
        updatedDoctors[index].seniority_name = matched.name;
      }
      return updatedDoctors;
    });
  };

  const handleNameChange = (index, newName) => {
    setDoctors((prev) => {
      const updated = [...prev];
      updated[index].name = newName;
      return updated;
    });
  };

  const handleAddDoctor = async (name, seniorityId) => {
    try {
      const response = await addDoctor(name, seniorityId);
      if (!response.id) throw new Error("Backend geçerli bir ID döndürmedi.");

      setDoctors((prev) => [
        ...prev,
        {
          id: response.id,
          name,
          seniority_name: seniorities.find((s) => s.id === seniorityId)?.name || "Bilinmeyen",
        },
      ]);
    } catch (error) {
      console.error("Doktor eklenirken hata:", error);
      alert("Doktor eklenirken bir hata oluştu.");
    }
  };

  // Doktor silme
  const handleDeleteDoctor = async (doctorId) => {
    try {
      await deleteDoctor(doctorId);
      setDoctors((prev) => prev.filter((doc) => doc.id !== doctorId));
    } catch (error) {
      console.error("Doktor silinirken hata:", error);
      alert("Doktor silinirken bir hata oluştu.");
    }
  };

  // Doktorlar değişikliklerini kaydet
  const handleSaveChanges = async () => {
    try {
      const payload = doctors.map((doctor) => ({
        id: doctor.id,
        name: doctor.name.trim(),
        seniority_id: seniorities.find((s) => s.name === doctor.seniority_name).id,
      }));
      const response = await updateDoctors(payload);
      alert(response.message);
    } catch (error) {
      console.error("Doktor değişiklikleri kaydedilirken hata:", error);
      alert("Değişiklikler kaydedilirken bir hata oluştu.");
    }
  };

  // Kıdem tablosu - Max Nöbet değişince
  const handleMaxShiftsChange = (index, newMaxShifts) => {
    setDetailedSeniorities((prev) => {
      const updated = [...prev];
      updated[index].max_shifts_per_month = newMaxShifts;
      return updated;
    });
  };

  // Kıdem tablosu - Kıdem adı değişince
  const handleSeniorityNameChange = (index, newName) => {
    setDetailedSeniorities((prev) => {
      const updated = [...prev];
      updated[index].seniority_name = newName;
      return updated;
    });
  };

  // Yeni kıdem ekleme
  const handleAddSeniority = async (seniorityName, maxShifts) => {
    try {
      // İstersen tüm shift area'ları ilk başta aktif eklemek isteyebilirsin
      const shiftAreaIds = shiftAreas.map((area) => area.id);

      const response = await addSeniority(seniorityName, maxShifts, shiftAreaIds);
      if (!response.id) throw new Error("Kıdem eklerken ID gelmedi.");

      setDetailedSeniorities((prev) => [
        ...prev,
        {
          id: response.id,
          seniority_name: seniorityName,
          max_shifts_per_month: maxShifts,
          // Yeni eklenen kıdemde tüm alanları aktif saymak istersen:
          shift_area_names: shiftAreas.map((a) => a.area_name),
        },
      ]);
    } catch (error) {
      console.error("Kıdem eklenirken hata:", error);
      alert("Kıdem eklenirken bir hata oluştu.");
    }
  };

  // Kıdem silme
  const handleDeleteSeniority = async (seniorityId) => {
    try {
      await deleteSeniority(seniorityId);
      setDetailedSeniorities((prev) => prev.filter((sen) => sen.id !== seniorityId));
    } catch (error) {
      console.error("Kıdem silinirken hata:", error);
      alert("Kıdem silinirken bir hata oluştu.");
    }
  };

  // Kıdem değişikliklerini kaydet (backend'e)
  const handleSaveSeniorityChanges = async () => {
    try {
      // shift_area_names -> shift_area_ids
      const cleanedData = detailedSeniorities.map((sen) => ({
        id: sen.id,
        seniority_name: sen.seniority_name,
        max_shifts_per_month: sen.max_shifts_per_month,
        shift_area_ids: [
          ...new Set(
            sen.shift_area_names
              .map((name) => {
                const found = shiftAreas.find((a) => a.area_name === name);
                return found ? found.id : null;
              })
              .filter((id) => id !== null)
          ),
        ],
      }));

      console.log("Backend'e giden veri:", cleanedData);

      const response = await updatedSeniorities(cleanedData);
      alert(response.message);
    } catch (error) {
      console.error("Kıdem değişiklikleri kaydedilirken hata:", error);
      alert("Değişiklikler kaydedilirken bir hata oluştu.");
    }
  };

  // Shift alanı tablosu - İsim değişince
  const handleShiftAreaNameChange = (index, newName) => {
    setShiftAreas((prev) => {
      const updated = [...prev];
      updated[index].area_name = newName;
      return updated;
    });
  };

  const handleMinDoctorsPerAreaChange = (index, newMinDoctors) => {
    setShiftAreas((prev) => {
      const updated = [...prev];
      updated[index].min_doctors_per_area = newMinDoctors;
      return updated;
    });
  };

  // Shift alanları değişikliklerini kaydet
  const handleSaveShiftAreaChanges = async () => {
    try {
      const payload = shiftAreas.map((a) => ({
        id: a.id,
        area_name: a.area_name.trim(),
        min_doctors_per_area: a.min_doctors_per_area,
      }));
      const response = await updateShiftAreas(payload);
      alert(response.message);
    } catch (error) {
      console.error("Nöbet alanı değişiklikleri kaydedilirken hata:", error);
      alert("Değişiklikler kaydedilirken bir hata oluştu.");
    }
  };

  // Yeni nöbet alanı ekle
  const handleAddShiftArea = async (areaName, minDoctors) => {
    try {
      const response = await addShiftArea(areaName, minDoctors);
      if (!response.id) {
        throw new Error("Backend'den geçerli bir yanıt gelmedi.");
      }
      setShiftAreas((prev) => [...prev, { id: response.id, area_name: areaName, min_doctors_per_area: minDoctors }]);
    } catch (error) {
      console.error("Nöbet alanı eklenirken hata:", error);
      alert("Nöbet alanı eklenirken bir hata oluştu.");
    }
  };

  // Nöbet alanı silme
  const handleDeleteShiftArea = async (areaId) => {
    try {
      await deleteShiftArea(areaId);
      setShiftAreas((prev) => prev.filter((area) => area.id !== areaId));
    } catch (error) {
      console.error("Nöbet alanı silinirken hata:", error);
      alert("Nöbet alanı silinirken bir hata oluştu.");
    }
  };

  return (
    <div className="d-flex flex-column background-gradient min-vh-100">
      <div className="container-fluid p-5 flex-grow-1">
        <h2 className="fw-bold display-6 text-black ms-3">Hastane Veritabanı</h2>
        <div className="row mt-5">
          <div className="col-lg-6 col-md-12 mb-4 px-4">
            <DoctorTable
              doctors={doctors}
              seniorities={seniorities}
              handleNameChange={handleNameChange}
              handleSeniorityChange={handleSeniorityChange}
              handleSaveChanges={handleSaveChanges}
              handleAddDoctor={handleAddDoctor}
              handleDeleteDoctor={handleDeleteDoctor}
            />
          </div>

          <div className="col-lg-6 col-md-12 mb-4 px-4">
            <SeniorityTable
              detailedSeniorities={detailedSeniorities}
              shiftAreas={shiftAreas}
              handleMaxShiftsChange={handleMaxShiftsChange}
              handleSeniorityNameChange={handleSeniorityNameChange}
              handleSaveSeniorityChanges={handleSaveSeniorityChanges}
              handleAddSeniority={handleAddSeniority}
              handleDeleteSeniority={handleDeleteSeniority}
            />

            <ShiftAreasTable
              shiftAreas={shiftAreas}
              handleShiftAreaNameChange={handleShiftAreaNameChange}
              handleMinDoctorsPerAreaChange={handleMinDoctorsPerAreaChange}
              handleSaveShiftAreaChanges={handleSaveShiftAreaChanges}
              handleAddShiftArea={handleAddShiftArea}
              handleDeleteShiftArea={handleDeleteShiftArea}
            />
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Hospital;
