import { Routes, Route, Navigate, NavLink } from "react-router-dom";
import { useAuth } from "./AuthContext";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import CaseList from "./pages/CaseList";
import NewCase from "./pages/NewCase";
import CaseDetail from "./pages/CaseDetail";
import PredictionResult from "./pages/PredictionResult";
import ModelAdmin from "./pages/ModelAdmin";

function ProtectedLayout({ children }) {
  const { user, logout } = useAuth();
  if (!user) return <Navigate to="/login" replace />;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h1>XAI &amp; GenAI Brain Tumor Detection</h1>
        <nav>
          <NavLink to="/">Dashboard</NavLink>
          <NavLink to="/cases">Cases</NavLink>
          <NavLink to="/cases/new">New Case / Upload</NavLink>
          <NavLink to="/admin">Model &amp; Admin</NavLink>
        </nav>
      </aside>
      <div className="main">
        <div className="topbar">
          <div className="user-chip">
            {user.full_name} &middot; {user.role}
          </div>
          <button className="btn-secondary" onClick={logout}>Logout</button>
        </div>
        {children}
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<ProtectedLayout><Dashboard /></ProtectedLayout>} />
      <Route path="/cases" element={<ProtectedLayout><CaseList /></ProtectedLayout>} />
      <Route path="/cases/new" element={<ProtectedLayout><NewCase /></ProtectedLayout>} />
      <Route path="/cases/:caseId" element={<ProtectedLayout><CaseDetail /></ProtectedLayout>} />
      <Route path="/predictions/:predictionId" element={<ProtectedLayout><PredictionResult /></ProtectedLayout>} />
      <Route path="/admin" element={<ProtectedLayout><ModelAdmin /></ProtectedLayout>} />
    </Routes>
  );
}
