import axios from "axios";

const API_BASE = "http://localhost:5000/api";

export const getMetrics = (limit = 20) =>
  axios.get(`${API_BASE}/metrics?limit=${limit}`).then((res) => res.data);

export const getStatus = () =>
  axios.get(`${API_BASE}/status`).then((res) => res.data);

export const getErrors = (limit = 15) =>
  axios.get(`${API_BASE}/errors?limit=${limit}`).then((res) => res.data);

export const getAlerts = () =>
  axios.get(`${API_BASE}/alerts`).then((res) => res.data);
