import { Navigate, Outlet } from "react-router-dom";

const PrivateRoute = () => {
  const token = localStorage.getItem("access_token");

  // Eğer token yoksa login sayfasına yönlendir
  return token ? <Outlet /> : <Navigate to="/login" replace />;
};

export default PrivateRoute;
