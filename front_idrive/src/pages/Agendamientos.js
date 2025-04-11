import React, { useState, useEffect } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import "./Agendamientos.css";
import Sidebar from "../components/Sidebar";

const Agendamientos = () => {
  const [agendamientos, setAgendamientos] = useState([]);

  useEffect(() => {
    fetch("http://localhost:3000/Agendamientos/")
      .then((response) => response.json())
      .then((data) => {
        setAgendamientos(data);
      })
      .catch((error) => console.error("Error fetching agendamientos:", error));
  }, []);

  const eventos = agendamientos.map((agendamiento) => ({
    title: `Estudiante: ${agendamiento.id_estudiante}`,
    date: agendamiento.fecha_reserva,
  }));

  return (
    <div className="agendamientos-wrapper">
      <Sidebar />
      <div className="main-content">
        <h2 className="mb-4">Calendario de Agendamientos</h2>

        <div className="mb-4 agendamiento-botones">
          <button className="btn-agendar me-2">Agendar Clase</button>
          <button className="btn-modificar me-2">Modificar</button>
          <button className="btn-cancelar">Cancelar</button>
        </div>

        <FullCalendar
          plugins={[dayGridPlugin]}
          initialView="dayGridMonth"
          events={eventos}
          locale="es"
          height="auto"
        />
      </div>
    </div>
  );
};

export default Agendamientos;




