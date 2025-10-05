import React, { useState } from "react";
import "./FilterSortJob.css";

function FilterSortJob({ onFilter }) {
  const [filters, setFilters] = useState({ keyword: "", location: "", type: "all" });

  const handleChange = (e) => setFilters({ ...filters, [e.target.name]: e.target.value });

  const handleFilter = () => onFilter(filters);
  const handleReset = () => {
    setFilters({ keyword: "", location: "", type: "all" });
    onFilter({ keyword: "", location: "", type: "all" });
  };

  return (
    <div className="filter-container">
      <input name="keyword" placeholder="Search by title or company" value={filters.keyword} onChange={handleChange} />
      <input name="location" placeholder="Location" value={filters.location} onChange={handleChange} />
      <select name="type" value={filters.type} onChange={handleChange}>
        <option value="all">All Types</option>
        <option value="full-time">Full-Time</option>
        <option value="part-time">Part-Time</option>
        <option value="contract">Contract</option>
        <option value="internship">Internship</option>
        <option value="remote">Remote</option>
      </select>
      <div className="filter-buttons">
        <button onClick={handleFilter}>Search</button>
        <button onClick={handleReset}>Reset</button>
      </div>
    </div>
  );
}

export default FilterSortJob;
