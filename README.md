# 🎢 Theme Park Crowd Detection System

A real-time person detection and crowd analysis system powered by YOLO v11, designed for theme park CCTV monitoring and crowd management.

## � Two Versions Available

### 🚀 **Full Stack Version (React + YOLO v11 API)** - RECOMMENDED

Modern React frontend connected to Python Flask API with YOLO v11.

**Quick Start:**

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install frontend dependencies
cd frontend
npm install
cd ..

# 3. Start API server (Terminal 1)
python api_server.py

# 4. Start React frontend (Terminal 2)
cd frontend
npm run dev
```

**Or use PowerShell script:**

```powershell
.\start_servers.ps1
```

👉 **See [FULLSTACK_README.md](FULLSTACK_README.md) for complete setup guide**

---

### 📦 **Standalone Gradio Version**

All-in-one Python application with built-in UI (no separate frontend needed).

```bash
pip install -r requirements.txt
python objectdetect.py
```

Opens at `http://localhost:7860`

---

## 🌐 React Web App (GitHub Deploy)

If you want a deployable web app for GitHub, use the React frontend in [frontend/README.md](frontend/README.md).

- React app path: `frontend`
- Auto deploy workflow: `.github/workflows/deploy-frontend.yml`
- Note: For GitHub Pages deployment, you'll need to deploy the Flask API separately and update the API URL in the React app

> **Important:** Browser-only deployment requires a hosted API backend. See deployment section in [FULLSTACK_README.md](FULLSTACK_README.md).

---

## ✨ Features

- **👥 Real-time Person Detection**: Uses YOLO v11 for accurate person counting
- **📊 Crowd Density Analysis**: Calculates crowd density metrics
- **💡 Smart Recommendations**: Provides actionable advice based on crowd levels
- **🎯 High Accuracy**: Confidence-based detection with detailed statistics
- **🖥️ User-Friendly UI**: Clean Gradio interface for easy image upload and analysis

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python objectdetect.py
```

### 3. Open Your Browser

The system will automatically open at: `http://localhost:7860`

## 📖 How to Use

1. **Upload Image**: Click the upload area and select a CCTV image or photo from your theme park
2. **Analyze**: Click the "🔍 Analyze Crowd" button
3. **View Results**:
   - See detected people with bounding boxes
   - Check the total person count
   - Read crowd-based recommendations
   - Review detailed statistics

## 🎯 Crowd Levels & Recommendations

The system provides different recommendations based on crowd density:

- 🟢 **LOW CROWD** (< 5 people/million pixels): Perfect time to visit
- 🟡 **MODERATE CROWD** (5-15): Plan route efficiently
- 🟠 **HIGH CROWD** (15-30): Visit less popular attractions
- 🔴 **VERY HIGH CROWD** (> 30): Consider alternative areas

## 🔧 Configuration Options

### Change YOLO Model Size

In `objectdetect.py`, modify line 17:

```python
# Options: yolo11n.pt (fastest), yolo11s.pt, yolo11m.pt, yolo11l.pt, yolo11x.pt (most accurate)
self.model = YOLO('yolo11n.pt')
```

### Adjust Detection Confidence

Modify line 26 to change confidence threshold:

```python
results = self.model(image, classes=[0], conf=0.3)  # 0.3 = 30% confidence
```

### Enable Public Sharing

In `objectdetect.py`, line 210:

```python
demo.launch(
    share=True,  # Creates a public link
    server_name="0.0.0.0",
    server_port=7860
)
```

## 📊 Example Use Cases

- **Queue Management**: Monitor attraction queues in real-time
- **Crowd Control**: Identify overcrowded areas for staff deployment
- **Safety Monitoring**: Ensure safe capacity levels
- **Operations Planning**: Analyze crowd patterns for staffing decisions
- **Guest Experience**: Provide crowd updates to visitors

## 🎨 Model Options

| Model      | Speed      | Accuracy  | Use Case         |
| ---------- | ---------- | --------- | ---------------- |
| yolo11n.pt | ⚡ Fastest | Good      | Real-time CCTV   |
| yolo11s.pt | Fast       | Better    | Balanced         |
| yolo11m.pt | Medium     | High      | Higher accuracy  |
| yolo11l.pt | Slow       | Very High | Precision tasks  |
| yolo11x.pt | Slowest    | Best      | Maximum accuracy |

## 🛠️ System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **GPU**: Optional but recommended for faster processing
- **OS**: Windows, Linux, or macOS

## 📝 Notes

- First run will download the YOLO v11 model (~6-50MB depending on version)
- GPU acceleration (CUDA) will be used automatically if available
- Supports JPG, PNG, JPEG image formats
- Works best with elevated camera angles (like CCTV)

## 🐛 Troubleshooting

### Model Download Issues

If the model fails to download, manually download from:
https://github.com/ultralytics/assets/releases

### GPU Not Detected

Install CUDA-enabled PyTorch:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Port Already in Use

Change the port in `objectdetect.py`:

```python
demo.launch(server_port=7861)  # Try different port
```

## 📄 License

This project uses YOLO v11 from Ultralytics (AGPL-3.0 License)

## 🤝 Support

For issues or questions, check the console output for detailed error messages.

---

**Made with ❤️ for Theme Park Operations**
