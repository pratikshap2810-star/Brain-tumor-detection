import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import client from "../api/client";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    client.get("/dashboard").then((res) => setData(res.data)).catch(() => setError("Could not load dashboard."));
  }, []);

  if (error) return <div className="error-text">{error}</div>;
  if (!data) return <div className="loading-text">Loading dashboard...</div>;

  return (
    <div>
      <h2>Dashboard</h2>

      {data.model_status.is_placeholder && (
        <div className="disclaimer">
          ⚠ No trained model detected — the system is currently serving an <b>untrained
          demo/placeholder model</b>. Predictions are not meaningful until <code>ml/train.py</code> is run.
        </div>
      )}

      <div className="card-grid">
        <div className="card stat-card">
          <div className="value">{data.total_cases}</div>
          <div className="label">Total Cases</div>
        </div>
        <div className="card stat-card">
          <div className="value">{data.total_predictions}</div>
          <div className="label">Total Predictions</div>
        </div>
        <div className="card stat-card">
          <div className="value">{data.pending_reviews}</div>
          <div className="label">Pending Reviews</div>
        </div>
        <div className="card stat-card">
          <div className="value">{data.system_status === "operational" ? "🟢" : "🔴"}</div>
          <div className="label">System Status</div>
        </div>
      </div>

      <div className="card">
        <h2>Recent Predictions</h2>
        {data.recent_predictions.length === 0 ? (
          <div className="empty-state">No predictions yet. <Link to="/cases/new">Upload an MRI</Link> to get started.</div>
        ) : (
          <table>
            <thead>
              <tr><th>Case</th><th>Predicted Class</th><th>Confidence</th><th>Time</th><th></th></tr>
            </thead>
            <tbody>
              {data.recent_predictions.map((p) => (
                <tr key={p.id}>
                  <td>{p.case_code}</td>
                  <td>{p.predicted_class}</td>
                  <td>{(p.confidence_score * 100).toFixed(1)}%</td>
                  <td>{new Date(p.predicted_at).toLocaleString()}</td>
                  <td><Link to={`/predictions/${p.id}`}>View</Link></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
