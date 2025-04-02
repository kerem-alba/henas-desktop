import React from "react";
import { useNavigate } from "react-router-dom";
import { logout } from "../services/apiService";

const Profile = () => {
  const username = localStorage.getItem("username");
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="d-flex flex-column justify-content-center align-items-center min-vh-100 bg-light background-gradient">
      <div className="text-center p-4 bg-dark shadow rounded" style={{ width: "350px" }}>
        <img src="/gu-logo.png" alt="GaziUniversity" width="150" height="150" className="mb-3" />
        <h2 className="mb-3">{username}</h2>
        <button className="btn btn-danger w-100" onClick={handleLogout}>
          Çıkış Yap
        </button>
      </div>
    </div>
  );
};

export default Profile;
