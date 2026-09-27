import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import client from "../api/client";

export default function CaseDetail() {
  const { caseId } = useParams();
  const [caseData, setCaseData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    client.get(`/cases/${caseId}`).then((res) => setCaseData(res.data)).catch(() => setError("Could not load case."));
  }, [caseId]);

  if (error) return <div className="error-text">{error}</div>;
  if (!caseData) return <div className="loading-text">Loading case...</div>;

  return (
    <div>
      <h2>Case {caseData.case_code}</h2>
      <div className="card">
        <p><b>Patient Reference:</b> {caseData.patient_ref_id}</p>
        <p><b>Status:</b> <span className="badge badge-neutral">{caseData.status}</span></p>
        <p><b>Created:</b> {new Date(caseData.created_at).toLocaleString()}</p>
        <Link to="/cases">&larr; Back to case history</Link>
      </div>
    </div>
  );
}
