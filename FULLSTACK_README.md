# 🎢 Theme Park Crowd Detection System - Full Stack Setup

Complete YOLO v11 detection system with React frontend and Flask API backend.

## 🏗️ Architecture

- **Backend**: Python Flask API with YOLO v11 (`api_server.py`)
- **Frontend**: React + Vite app (`frontend/`)
- **Model**: YOLO v11 nano for real-time person detection

## 🚀 Quick Start

### 1. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

First run will download YOLO v11 model (~6MB).

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 3. Start Both Servers

**Terminal 1 - Start API Backend:**

```bash
python api_server.py
```

API runs on `http://localhost:5000`

**Terminal 2 - Start React Frontend:**

```bash
cd frontend
npm run dev
```

Frontend runs on `http://localhost:5173`

### 4. Open Your Browser

Visit `http://localhost:5173` and upload a theme park image!

## 📁 Project Structure

```
ObjectDetection/
│
├── api_server.py          # Flask API with YOLO v11
├── objectdetect.py        # Original Gradio version (standalone)
├── requirements.txt       # Python dependencies
│
├── frontend/              # React application
│   ├── src/
│   │   ├── App.jsx       # Main app with API calls
│   │   ├── App.css       # Styling
│   │   └── crowdUtils.js # Recommendation logic
│   ├── package.json
│   └── vite.config.js
│
└── .github/
    └── workflows/
        └── deploy-frontend.yml  # GitHub Pages deployment
```

## 🔧 Configuration

### Change YOLO Model

Edit `api_server.py` line 19:

```python
self.model = YOLO('yolo11n.pt')  # Options: yolo11n, yolo11s, yolo11m, yolo11l, yolo11x
```

### Change API URL (Production)

Edit `frontend/src/App.jsx` line 6:

```javascript
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";
```

Or set environment variable:

```bash
VITE_API_URL=https://your-api-domain.com npm run build
```

## 📊 API Endpoints

### `GET /api/health`

Health check endpoint.

**Response:**

```json
{
  "status": "ok",
  "model": "YOLOv11"
}
```

### `POST /api/detect`

Person detection endpoint.

**Request:** `multipart/form-data` with `image` file

**Response:**

```json
{
  "personCount": 15,
  "density": 8.5,
  "detections": [...],
  "annotatedImage": "base64...",
  "imageWidth": 1920,
  "imageHeight": 1080
}
```

## 🎯 Features

✅ **YOLO v11 Detection** - Most accurate person counting  
✅ **Real-time Results** - Fast API responses  
✅ **Bounding Boxes** - Visual detection overlay  
✅ **Crowd Levels** - 4 tiers (Low, Moderate, High, Very High)  
✅ **Smart Recommendations** - Context-aware visitor advice  
✅ **Responsive UI** - Clean React interface

## 🌐 Deployment Options

### Option 1: Local Development (Current Setup)

- Backend: Run `python api_server.py` locally
- Frontend: Run `npm run dev` locally
- Great for testing and development

### Option 2: Deploy Backend + Static Frontend

1. Deploy Flask API to a cloud service (Heroku, Railway, GCP, AWS)
2. Update `VITE_API_URL` in frontend
3. Build frontend: `npm run build`
4. Deploy `frontend/dist/` to static hosting (Netlify, Vercel, GitHub Pages)

### Option 3: Full Stack Deployment

- Deploy both backend and frontend to the same server
- Use services like Railway, Render, or DigitalOcean

## 🐛 Troubleshooting

### "Failed to analyze image" Error

**Solution:** Make sure API server is running on port 5000

```bash
python api_server.py
```

### CORS Errors

**Solution:** Flask-CORS is configured. If issues persist, check firewall/proxy settings.

### Model Download Issues

**Solution:** Manually download from https://github.com/ultralytics/assets/releases

### Port Already in Use

**Backend:** Change port in `api_server.py` line 109
**Frontend:** Vite will auto-assign another port

## 💡 Tips

- Use higher YOLO models (yolo11m, yolo11l) for better accuracy
- API server supports GPU acceleration (CUDA) automatically
- Frontend has dev proxy configured for seamless local development
- Use confidence threshold adjustment in `api_server.py` line 32

## 📝 Alternative: Standalone Gradio Version

If you prefer the all-in-one Python version:

```bash
python objectdetect.py
```

This runs a Gradio interface without needing the React frontend.

---

**Made with ❤️ for Theme Park Operations**
