import { useEffect, useState } from "react";
import { getErrors } from "../api/pulsewatch";

export default function ErrorFeed() {
  const [errors, setErrors] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = await getErrors(15);
      setErrors(data);
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="card">
      <h2>Recent Errors &amp; Warnings</h2>
      {errors.length === 0 && <div className="empty">No log events yet</div>}
      {errors.map((e) => (
        <div className="log-row" key={e.id}>
          <span className={`badge ${e.severity.toLowerCase()}`}>{e.severity}</span>{" "}
          {e.message}
          <div className="meta">{e.timestamp} — {e.process}</div>
        </div>
      ))}
    </div>
  );
}
