import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { addJob, updateJob, getJobs } from "../api";
import "./JobForm.css";

function AddEditJob() {
  const [job, setJob] = useState({
    title: "",
    company: "",
    location: "",
    job_type: "full-time",
    tags: "",
  });

  const navigate = useNavigate();
  const { id } = useParams();

  useEffect(() => {
    if (id) {
      getJobs().then((res) => {
        const data = Array.isArray(res.data)
          ? res.data
          : res.data.jobs || [];

        const existing = data.find((j) => j.id === parseInt(id));
        if (existing) {
          setJob({
            title: existing.title || "",
            company: existing.company || "",
            location: existing.location || "",
            job_type: existing.job_type || "full-time",
            tags: Array.isArray(existing.tags)
              ? existing.tags.join(", ")
              : existing.tags || "",
          });
        }
      });
    }
  }, [id]);

  const handleChange = (e) =>
    setJob({ ...job, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      ...job,
      tags: job.tags
        .split(",")
        .map((t) => t.trim())
        .filter((t) => t.length > 0),
    };

    if (id) await updateJob(id, payload);
    else await addJob(payload);

    navigate("/");
  };

  return (
    <div className="form-container">
      <h2>{id ? "Edit Job Posting" : "Create New Job"}</h2>

      <form className="job-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Job Title</label>
          <input
            name="title"
            id="title"
            value={job.title}
            onChange={handleChange}
            placeholder="Enter job title"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="company">Company</label>
          <input
            name="company"
            id="company"
            value={job.company}
            onChange={handleChange}
            placeholder="Enter company name"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="location">Location</label>
          <input
            name="location"
            id="location"
            value={job.location}
            onChange={handleChange}
            placeholder="Enter location"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="job_type">Job Type</label>
          <select
            name="job_type"
            id="job_type"
            value={job.job_type}
            onChange={handleChange}
          >
            <option value="full-time">Full-Time</option>
            <option value="part-time">Part-Time</option>
            <option value="contract">Contract</option>
            <option value="internship">Internship</option>
            <option value="remote">Remote</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="tags">Tags</label>
          <input
            name="tags"
            id="tags"
            value={job.tags}
            onChange={handleChange}
            placeholder="e.g. React, Remote, Internship"
          />
        </div>

        <button type="submit" className="submit-btn">
          {id ? "Update Job" : "Add Job"}
        </button>
      </form>
    </div>
  );
}

export default AddEditJob;
