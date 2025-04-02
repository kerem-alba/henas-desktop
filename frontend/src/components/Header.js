/* eslint-disable jsx-a11y/anchor-is-valid */
import React from "react";

const Header = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
      <div className="container-fluid px-5 mx-3">
        <a className="navbar-brand fw-bold d-flex align-items-center fs-4" href="/">
          <img src="/henas-bot.png" alt="Nöbet Asistanı Logo" width="50" height="50" className="me-2" />
          HENAS - Hekim Nöbet Asistanı
        </a>
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
                  <a className="dropdown-item" href="/schedule-data">
                    📊 Nöbet Listesi Verileri
                  </a>
                </li>
                <li>
                  <a className="dropdown-item" href="/create-schedule">
                    ➕ Nöbet Listesi Oluştur
                  </a>
                </li>
                <li>
                  <a className="dropdown-item" href="/schedule-lists">
                    📁 Kayıtlı Nöbet Listeleri
                  </a>
                </li>
              </ul>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/hospital">
                ⚕️ Hastanem
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/settings">
                ⚙️ Ayarlar
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/profile">
                👤 Profil
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Header;
