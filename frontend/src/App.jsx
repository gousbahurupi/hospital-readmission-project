import { Routes, Route } from "react-router-dom";
import { Sidebar } from "./components/layout/Sidebar.jsx";
import { Dashboard } from "./pages/Dashboard.jsx";
import { PredictionPage } from "./pages/PredictionPage.jsx";
import { AgentPage } from "./pages/AgentPage.jsx";
import { ModelInfoPage } from "./pages/ModelInfoPage.jsx";

export default function App() {
  return (
    <div className="min-h-screen flex bg-paper">
      <Sidebar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/assessment" element={<PredictionPage />} />
        <Route path="/agent" element={<AgentPage />} />
        <Route path="/model-info" element={<ModelInfoPage />} />
      </Routes>
    </div>
  );
}
