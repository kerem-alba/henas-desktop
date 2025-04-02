import "./App.css";
import Header from "./components/Header";
import CreateSchedule from "./pages/CreateSchedule";
import Hospital from "./pages/Hospital";
import ScheduleData from "./pages/ScheduleData";
import ScheduleLists from "./pages/ScheduleLists";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import Settings from "./pages/Settings";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import PrivateRoute from "./components/PrivateRoute"; // Güncellenmiş PrivateRoute

function App() {
  const isLoginPage = window.location.pathname === "/login";

  return (
    <BrowserRouter>
      {!isLoginPage && <Header />}
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/home" />} />
        <Route path="/home" element={<Home />} />

        {/* Login gerektiren sayfalar için Outlet kullanıyoruz */}
        <Route element={<PrivateRoute />}>
          <Route path="/hospital" element={<Hospital />} />
          <Route path="/schedule-data" element={<ScheduleData />} />
          <Route path="/create-schedule" element={<CreateSchedule />} />
          <Route path="/schedule-lists" element={<ScheduleLists />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
