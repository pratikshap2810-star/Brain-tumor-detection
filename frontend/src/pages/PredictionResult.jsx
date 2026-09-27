import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import client from "../api/client";

export default function PredictionResult() {
  const { predictionId } = useParams();
  const [prediction, setPrediction] = useState(null);
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");
  const [genReportLoading, setGenReportLoading] = useState(false);
  const [reviewText, setReviewText] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    client.get(`/predictions/${predictionId}`)
      .then((res) => setPrediction(res.data))
      .catch(() => setError("Could not load prediction."));
  }, [predictionId]);

  async function handleGenerateReport() {
    setGenReportLoading(true);
    try {
      const res = await client.post("/reports/generate", { prediction_id: predictionId });
      setReport(res.data);
      setReviewText(res.data.reviewed_content || res.data.draft_content);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not generate report.");
    } finally {
      setGenReportLoading(false);
    }
  }

  async function handleSaveReview(approve) {
    setSaving(true);
    try {
      const res = await client.put(`/reports/${report.id}/review`, {
        reviewed_content: reviewText,
        approve,
      });
      setReport(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not save review.");
    } finally {
      setSaving(false);
    }
  }

  if (error) return <div className="error-text">{error}</div>;
  if (!prediction) return <div className="loading-text">Loading prediction...</div>;

  const sortedProbs = Object.entries(prediction.all_class_probabilities).sort((a, b) => b[1] - a[1]);

  return (
    <div>
      <h2>Prediction Result</h2>

      <div className="card">
        <p>
          <b>Predicted class:</b>{" "}
          <span className="badge badge-success" style={{ fontSize: 14 }}>{prediction.predicted_class}</span>
          &nbsp;&nbsp;<b>Confidence:</b> {(prediction.confidence_score * 100).toFixed(1)}%
          &nbsp;&nbsp;<span style={{ color: "#94a3b8", fontSize: 12 }}>Model: {prediction.model_version}</span>
        </p>

        <h2 style={{ fontSize: 14, marginTop: 18 }}>Class Probabilities</h2>
        {sortedProbs.map(([cls, prob]) => (
          <div key={cls}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13 }}>
              <span>{cls}</span><span>{(prob * 100).toFixed(1)}%</span>
            </div>
            <div className="confidence-bar-track">
              <div className="confidence-bar-fill" style={{ width: `${prob * 100}%` }} />
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <h2>Original vs Grad-CAM Explanation</h2>
        <div className="image-compare">
          <div>
            <p style={{ fontSize: 12, color: "#64748b" }}>Grad-CAM Overlay</p>
            {prediction.overlay_url && <img src={prediction.overlay_url} alt="Grad-CAM overlay" />}
          </div>
          <div>
            <p style={{ fontSize: 12, color: "#64748b" }}>Raw Heatmap</p>
            {prediction.heatmap_url && <img src={prediction.heatmap_url} alt="Grad-CAM heatmap" />}
          </div>
        </div>
        <div className="disclaimer">{prediction.disclaimer}</div>
      </div>

      <div className="card">
        <h2>GenAI Draft Report</h2>
        {!report && (
          <button onClick={handleGenerateReport} disabled={genReportLoading}>
            {genReportLoading ? "Generating..." : "Generate Draft Report"}
          </button>
        )}
        {report && (
          <>
            <p>
              <span className={`badge ${report.review_status === "approved" ? "badge-success" : "badge-warning"}`}>
                {report.review_status.replace("_", " ")}
              </span>
            </p>
            <textarea
              rows={16}
              value={reviewText}
              onChange={(e) => setReviewText(e.target.value)}
              style={{ fontFamily: "monospace", fontSize: 13 }}
            />
            <div style={{ display: "flex", gap: 10 }}>
              <button onClick={() => handleSaveReview(false)} disabled={saving} className="btn-secondary">
                Save Edits
              </button>
              <button onClick={() => handleSaveReview(true)} disabled={saving}>
                Approve Report
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
