import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:5000",
});

export const getJobs = () => API.get("/api/jobs/list");
export const addJob = (job) => API.post("/api/jobs", job);
export const updateJob = (id, job) => API.put(`/api/jobs/${id}`, job);
export const deleteJob = (id) => API.delete(`/api/jobs/${id}`);
