/* eslint-disable jsx-a11y/anchor-is-valid */
import React from "react";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
      <div className="container-fluid px-5 mx-3">
        <Link className="navbar-brand fw-bold d-flex align-items-center fs-4" to="/">
          <img src="henas-bot.png" alt="Nöbet Asistanı Logo" width="50" height="50" className="me-2" />
          HENAS - Hekim Nöbet Asistanı
        </Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav" style={{ fontSize: "1.2rem" }}>
          <ul className="navbar-nav ms-auto">
            <li className="nav-item dropdown">
              <a className="nav-link dropdown-toggle" id="nobetListeleriDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Nöbet Listeleri
              </a>
              <ul className="dropdown-menu">
                <li>
                  <Link className="dropdown-item" to="/schedule-data">
                    📊 Nöbet Listesi Verileri
                  </Link>
                </li>
                <li>
                  <Link className="dropdown-item" to="/create-schedule">
                    ➕ Nöbet Listesi Oluştur
                  </Link>
                </li>
                <li>
                  <Link className="dropdown-item" to="/schedule-lists">
                    📁 Kayıtlı Nöbet Listeleri
                  </Link>
                </li>
              </ul>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/hospital">
                ⚕️ Hastanem
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/settings">
                ⚙️ Ayarlar
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/profile">
                👤 Profil
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Header;
