import MetricsChart from "./components/MetricsChart";
import ServiceStatus from "./components/ServiceStatus";
import ErrorFeed from "./components/ErrorFeed";
import "./App.css";

export default function App() {
  return (
    <div className="app">
      <h1>PulseWatch</h1>
      <div className="subtitle">Hospital server monitoring dashboard — live view</div>
      <div className="grid">
        <MetricsChart />
        <ServiceStatus />
        <ErrorFeed />
      </div>
    </div>
  );
}
