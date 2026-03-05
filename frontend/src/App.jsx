import { useState } from "react";
import { getRecommendations } from "./crowdUtils";
import "./App.css";

// API endpoint - change to your deployed backend URL for production
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

function App() {
  const [analyzing, setAnalyzing] = useState(false);
  const [selectedImageUrl, setSelectedImageUrl] = useState("");
  const [annotatedImageUrl, setAnnotatedImageUrl] = useState("");
  const [rawImage, setRawImage] = useState(null);
  const [personCount, setPersonCount] = useState(0);
  const [density, setDensity] = useState(0);
  const [recommendations, setRecommendations] = useState([]);
  const [crowdLevelLabel, setCrowdLevelLabel] = useState("");
  const [error, setError] = useState("");

  const handleImageUpload = (event) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    setError("");
    const imageUrl = URL.createObjectURL(file);
    setSelectedImageUrl(imageUrl);
    setRawImage(file);
    setPersonCount(0);
    setDensity(0);
    setRecommendations([]);
    setCrowdLevelLabel("");
    setAnnotatedImageUrl("");
  };

  const analyzeImage = async () => {
    if (!rawImage) {
      setError("Please upload an image first.");
      return;
    }

    setAnalyzing(true);
    setError("");

    try {
      // Create FormData and append the image
      const formData = new FormData();
      formData.append("image", rawImage);

      // Send to YOLO v11 API
      const response = await fetch(`${API_URL}/api/detect`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const result = await response.json();

      // Update state with detection results
      const count = result.personCount;
      const calculatedDensity = result.density;

      // Set annotated image from base64
      setAnnotatedImageUrl(`data:image/png;base64,${result.annotatedImage}`);

      // Generate recommendations
      const recommendationResult = getRecommendations(count, calculatedDensity);

      setPersonCount(count);
      setDensity(calculatedDensity);
      setCrowdLevelLabel(recommendationResult.crowdLevel.label);
      setRecommendations(recommendationResult.items);
    } catch (err) {
      console.error("Detection error:", err);
      setError(
        "Failed to analyze image. Make sure the API server is running on port 5000.",
      );
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>🎢 Theme Park Crowd Detector</h1>
        <p className="subtitle">
          Powered by YOLO v11 - Upload a CCTV or park photo to count people
        </p>
      </header>

      <section className="card">
        <label htmlFor="imageUpload" className="upload-label">
          Upload image
        </label>
        <input
          id="imageUpload"
          type="file"
          accept="image/*"
          onChange={handleImageUpload}
        />

        <button
          type="button"
          disabled={analyzing || !rawImage}
          onClick={analyzeImage}
        >
          {analyzing ? "🔍 Analyzing with YOLO v11..." : "Analyze Crowd"}
        </button>

        {error && <p className="error">{error}</p>}
      </section>

      <section className="layout">
        <div className="card">
          <h2>Detection Result</h2>
          {annotatedImageUrl ? (
            <div className="image-wrap">
              <img src={annotatedImageUrl} alt="Detection result" />
            </div>
          ) : selectedImageUrl ? (
            <div className="image-wrap">
              <img src={selectedImageUrl} alt="Uploaded scene" />
              <p className="hint">Click "Analyze Crowd" to process</p>
            </div>
          ) : (
            <p>No image uploaded yet.</p>
          )}
        </div>

        <div className="card">
          <h2>People Count</h2>
          <p className="metric">{personCount}</p>
          <p>Crowd density: {density.toFixed(2)} people / million pixels</p>
          <p>{crowdLevelLabel}</p>
        </div>
      </section>

      <section className="card">
        <h2>Recommendations</h2>
        {recommendations.length === 0 ? (
          <p>Run analysis to get recommendations.</p>
        ) : (
          <ul>
            {recommendations.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

export default App;
