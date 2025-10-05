import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { deleteJob } from "../api";
import "./DeleteJob.css";

function DeleteJob() {
  const { id } = useParams();
  const navigate = useNavigate();

  const handleDelete = async () => {
    try {
      await deleteJob(id);
      navigate("/");
    } catch (error) {
      console.error("Delete failed:", error);
      alert("Error deleting job. Please try again.");
    }
  };

  return (
    <div className="delete-container">
      <div className="delete-box">
        <h2>⚠️ Confirm Deletion</h2>
        <p>Are you sure you want to permanently delete this job post?</p>
        <div className="delete-buttons">
          <button onClick={handleDelete} className="delete-btn">
            Yes, Delete
          </button>
          <button onClick={() => navigate("/")} className="cancel-btn">
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

export default DeleteJob;
