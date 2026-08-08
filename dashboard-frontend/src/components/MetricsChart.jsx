import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { getMetrics } from "../api/pulsewatch";

function formatTime(timestamp) {
  return timestamp.split(" ")[1];
}

export default function MetricsChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const metrics = await getMetrics(20);
      const reversed = [...metrics].reverse().map((m) => ({
        ...m,
        time: formatTime(m.timestamp),
      }));
      setData(reversed);
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="card">
      <h2>CPU / RAM Usage</h2>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#262a36" />
          <XAxis dataKey="time" stroke="#9ca3af" fontSize={12} />
          <YAxis domain={[0, 100]} stroke="#9ca3af" fontSize={12} />
          <Tooltip
            contentStyle={{ background: "#171a23", border: "1px solid #262a36" }}
          />
          <Legend />
          <Line type="monotone" dataKey="cpu_percent" name="CPU %" stroke="#60a5fa" dot={false} />
          <Line type="monotone" dataKey="ram_percent" name="RAM %" stroke="#f472b6" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
