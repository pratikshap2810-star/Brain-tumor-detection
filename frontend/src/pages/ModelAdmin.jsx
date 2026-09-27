import { useEffect, useState } from "react";
import client from "../api/client";

export default function ModelAdmin() {
  const [versions, setVersions] = useState(null);
  const [status, setStatus] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    client.get("/models").then((res) => setVersions(res.data)).catch(() => setError("Could not load model versions."));
    client.get("/models/current").then((res) => setStatus(res.data)).catch(() => {});
  }, []);

  return (
    <div>
      <h2>Model &amp; Admin</h2>

      {status && (
        <div className="card">
          <h2>Current Model Status</h2>
          <p><b>Architecture:</b> {status.architecture}</p>
          <p><b>Classes:</b> {status.classes.join(", ")}</p>
          <p>
            <b>Status:</b>{" "}
            {status.is_placeholder
              ? <span className="badge badge-warning">Untrained / Demo Placeholder</span>
              : <span className="badge badge-success">Trained</span>}
          </p>
          {status.metrics && !status.is_placeholder && (
            <>
              <h2 style={{ fontSize: 14 }}>Test Set Metrics</h2>
              <p style={{ fontSize: 13 }}>
                Accuracy: {(status.metrics.test_metrics.accuracy * 100).toFixed(2)}% &middot;
                {" "}Precision: {(status.metrics.test_metrics.precision_macro * 100).toFixed(2)}% &middot;
                {" "}Recall: {(status.metrics.test_metrics.recall_macro * 100).toFixed(2)}% &middot;
                {" "}F1: {(status.metrics.test_metrics.f1_macro * 100).toFixed(2)}%
              </p>
            </>
          )}
        </div>
      )}

      <div className="card">
        <h2>Model Versions</h2>
        {error && <div className="error-text">{error}</div>}
        {versions && versions.length === 0 && <div className="empty-state">No model versions registered yet.</div>}
        {versions && versions.length > 0 && (
          <table>
            <thead>
              <tr><th>Version</th><th>Arch</th><th>Accuracy</th><th>Status</th><th>Deployment</th></tr>
            </thead>
            <tbody>
              {versions.map((v) => (
                <tr key={v.id}>
                  <td>{v.version_tag}</td>
                  <td>{v.architecture}</td>
                  <td>{v.accuracy ? `${(v.accuracy * 100).toFixed(2)}%` : "—"}</td>
                  <td>{v.is_placeholder ? <span className="badge badge-warning">placeholder</span> : <span className="badge badge-success">trained</span>}</td>
                  <td>{v.deployment_status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
