import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "@fortawesome/fontawesome-free/css/all.min.css";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import "./assets/css/sb-admin-2.min.css";
import Agendamientos from "./pages/Agendamientos";


function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/Dashboard" element={<Dashboard />} />
                <Route path="/Login" element={<Login />} />
                <Route path="/Agendamientos" element={<Agendamientos />} />
            </Routes>
        </Router>
    );
}

export default App;
