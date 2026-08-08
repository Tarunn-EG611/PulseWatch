import { useEffect, useState } from "react";
import { getStatus } from "../api/pulsewatch";

export default function ServiceStatus() {
  const [services, setServices] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = await getStatus();
      setServices(data);
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="card">
      <h2>Service Status</h2>
      {services.length === 0 && <div className="empty">No data yet</div>}
      {services.map((s) => (
        <div className="status-row" key={s.service_name}>
          <span>{s.service_name}</span>
          <span className={`badge ${s.status.toLowerCase()}`}>{s.status}</span>
        </div>
      ))}
    </div>
  );
}
