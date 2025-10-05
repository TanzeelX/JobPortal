import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import JobList from "./Pages/JobList.jsx";
import AddEditJob from "./Pages/AddEditJob.jsx";
import DeleteJob from "./Pages/DeleteJob.jsx";
import FilterSortJob from "./Pages/FilterSortJob.jsx";
import "./App.css";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<JobList />} />
        <Route path="/add" element={<AddEditJob />} />
        <Route path="/edit/:id" element={<AddEditJob />} />
        <Route path="/delete/:id" element={<DeleteJob />} />
        <Route path="/filter" element={<FilterSortJob />} />
      </Routes>
    </Router>
  );
}

export default App;
