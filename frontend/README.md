# React Crowd Detection Frontend

Deployable React app for person counting and crowd recommendations with YOLO v11 backend.

## Features

- Upload CCTV/theme park photo
- Detect people using YOLO v11 (via API)
- Show people count and crowd density
- Generate crowd recommendations
- Real-time bounding box visualization

## Prerequisites

The Flask API backend must be running:

```bash
# From project root
python api_server.py
```

## Run locally

```bash
npm install
npm run dev
```

Visit `http://localhost:5173`

## Build locally

```bash
npm run build
npm run preview
```

## Configuration

### Change API URL

Create `.env.local` file:

```bash
VITE_API_URL=http://localhost:5000
```

Or edit `src/App.jsx` line 6.

## Deploy

### Static Frontend + API Backend

1. **Deploy Flask API** to cloud service (Railway, Render, Heroku, etc.)
2. **Update API URL**: Set `VITE_API_URL` environment variable
3. **Build frontend**: `npm run build`
4. **Deploy `dist/` folder** to:
   - Netlify
   - Vercel
   - GitHub Pages (see workflow)
   - Any static hosting

### GitHub Pages Deployment

1. Deploy API backend first and get URL
2. Update `VITE_API_URL` in build environment
3. Push to GitHub
4. Enable Pages in repo settings (Source: GitHub Actions)
5. Workflow at `.github/workflows/deploy-frontend.yml` will auto-deploy

## Important

- This frontend **requires** the Python Flask API (`api_server.py`) to be running
- Uses actual YOLO v11 model for accurate person detection
- API handles all detection logic; frontend handles visualization only
- Make sure API URL is accessible from where frontend is deployed
