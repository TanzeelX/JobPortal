import React, { useState } from "react";
import "./Navbar.css";

function Navbar({ onSearch }) {
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    if (onSearch) onSearch(query);
    console.log("Search query:", query);
  };

  return (
    <nav className="navbar">
      <div className="navbar-logo">Job Portal</div>

      <div className="navbar-search">
        <input
          type="text"
          placeholder="Search jobs..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>
    </nav>
  );
}

export default Navbar;
