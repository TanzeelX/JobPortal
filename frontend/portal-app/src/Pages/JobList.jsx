import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getJobs } from "../api";
import FilterSortJob from "./FilterSortJob";
import "./JobList.css";

function JobList() {
  const [jobs, setJobs] = useState([]);
  const [filteredJobs, setFilteredJobs] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getJobs()
      .then((res) => {
        const data = Array.isArray(res.data)
          ? res.data
          : Array.isArray(res.data.jobs)
            ? res.data.jobs
            : [];

        const normalized = data.map((job) => ({
          id: job.id,
          title: job.title || "Untitled",
          company: job.company || "Unknown",
          location: job.location || "N/A",
          type: job.job_type || job.type || "N/A",
          posting_date: job.posting_date
            ? new Date(job.posting_date).toLocaleDateString()
            : "N/A",
          tags:
            typeof job.tags === "string"
              ? job.tags.split(",").map((t) => t.trim())
              : Array.isArray(job.tags)
                ? job.tags
                : [],
        }));

        setJobs(normalized);
        setFilteredJobs(normalized);
      })
      .catch((err) => {
        console.error("Error fetching jobs:", err);
        setError("Failed to load jobs. Please try again later.");
      });
  }, []);

  
  const handleFilter = (filters) => {
    const keyword = filters.keyword.toLowerCase().trim();
    const location = filters.location.toLowerCase().trim();
    const type = filters.type.toLowerCase();
    const company = filters.company ? filters.company.toLowerCase().trim() : "";
    const tag = filters.tag ? filters.tag.toLowerCase().trim() : "";

    const filtered = jobs.filter((job) => {
      const matchKeyword =
        !keyword ||
        job.title.toLowerCase().includes(keyword) ||
        job.company.toLowerCase().includes(keyword);

      const matchLocation =
        !location || job.location.toLowerCase().includes(location);

      const matchType =
        type === "all" || job.type.toLowerCase() === type.toLowerCase();

      const matchCompany =
        !company || job.company.toLowerCase().includes(company);

      const matchTag =
        !tag || job.tags.some((t) => t.toLowerCase().includes(tag));

      return (
        matchKeyword && matchLocation && matchType && matchCompany && matchTag
      );
    });

    setFilteredJobs(filtered);
  };

  return (


  <div className="job-list-container">
    <div className="job-list-header">
      <h1 className="dashboard-title"><b>Job Portal Dashboard</b></h1>
      <Link to="/add" className="add-btn">
        + Add Job
      </Link>
    </div>

    <FilterSortJob onFilter={handleFilter} />

    {error && <p className="error-message">{error}</p>}

    <div className="job-grid">
      {filteredJobs.length > 0 ? (
        filteredJobs.map((job) => (
          <div className="job-card" key={job.id}>
            <div className="job-card-header">
              <h3 className="job-title">{job.title}</h3>
              <span className="job-type">{job.type}</span>
            </div>

            <p className="company-name">{job.company}</p>

            <div className="job-details">
              <p>
                <i className="fa fa-map-marker" /> {job.location}
              </p>
              <p>
                <i className="fa fa-calendar" /> {job.posting_date}
              </p>
            </div>

            {job.tags.length > 0 && (
              <div className="job-tags">
                {job.tags.map((tag, i) => (
                  <span key={i} className="tag">
                    {tag}
                  </span>
                ))}
              </div>
            )}

            <div className="job-actions">
              <Link to={`/edit/${job.id}`} className="edit-btn">
                Edit
              </Link>
              <Link to={`/delete/${job.id}`} className="delete-btn">
                Delete
              </Link>
            </div>
          </div>
        ))
      ) : (
        <p className="no-jobs">No jobs found.</p>
      )}
    </div>
  </div>
  );
}

export default JobList;
