import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import client from "../api/client";

export default function CaseList() {
  const [cases, setCases] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    client.get("/cases").then((res) => setCases(res.data)).catch(() => setError("Could not load cases."));
  }, []);

  return (
    <div>
      <h2>Case History</h2>
      <div className="card">
        {error && <div className="error-text">{error}</div>}
        {!cases && !error && <div className="loading-text">Loading cases...</div>}
        {cases && cases.length === 0 && (
          <div className="empty-state">No cases yet. <Link to="/cases/new">Create your first case</Link>.</div>
        )}
        {cases && cases.length > 0 && (
          <table>
            <thead>
              <tr><th>Case Code</th><th>Patient Ref</th><th>Status</th><th>Created</th><th></th></tr>
            </thead>
            <tbody>
              {cases.map((c) => (
                <tr key={c.id}>
                  <td>{c.case_code}</td>
                  <td>{c.patient_ref_id}</td>
                  <td><span className="badge badge-neutral">{c.status}</span></td>
                  <td>{new Date(c.created_at).toLocaleDateString()}</td>
                  <td><Link to={`/cases/${c.id}`}>Open</Link></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
