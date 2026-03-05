# 🚂 Railway Deployment Guide

## Deploy Your YOLO v11 API to Railway

### Step 1: Prepare Your Repository

1. **Initialize Git** (if not already done):

```bash
cd "C:\Users\Aaron\Downloads\ObjectDetection"
git init
git add .
git commit -m "Initial commit - YOLO v11 API"
```

2. **Push to GitHub**:

```bash
# Create a new repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Railway

1. **Go to [Railway.app](https://railway.app)** and sign up/login with GitHub

2. **Click "New Project"**

3. **Select "Deploy from GitHub repo"**

4. **Choose your repository**

5. Railway will **automatically detect** Python and start deploying!

### Step 3: Configure Environment (Optional)

Railway auto-detects everything, but you can add variables if needed:

- `PORT` - Railway sets this automatically
- `PYTHON_VERSION` - Set to `3.12` (we have runtime.txt for this)

### Step 4: Get Your API URL

Once deployed, Railway gives you a URL like:

```
https://your-app-name.railway.app
```

### Step 5: Update React Frontend

Edit `frontend/src/App.jsx` line 6:

```javascript
const API_URL = "https://your-app-name.railway.app";
```

Or create `frontend/.env.production`:

```bash
VITE_API_URL=https://your-app-name.railway.app
```

### Step 6: Deploy Frontend

**Option A: GitHub Pages**

```bash
cd frontend
npm run build
# Use the GitHub workflow in .github/workflows/deploy-frontend.yml
```

**Option B: Vercel**

```bash
cd frontend
npm install -g vercel
vercel --prod
```

**Option C: Netlify**

```bash
cd frontend
npm run build
# Drag and drop the `dist` folder to netlify.com
```

## ⚠️ Important Notes

### Railway Free Tier Limits:

- $5 free credit per month
- ~500 hours of usage
- Good for demo/testing
- For production, consider upgrading

### Model Size:

- YOLO v11 nano (~6MB) - Currently using ✅
- Larger models (s, m, l, x) will increase memory usage
- Railway handles this fine on paid tiers

### First Deploy:

- Takes 3-5 minutes (downloading PyTorch)
- Subsequent deploys are faster (cached)
- YOLO model downloads on first API call

## 🐛 Troubleshooting

### Build Fails

- Check logs in Railway dashboard
- Verify requirements.txt has all dependencies
- Ensure Python 3.12 is specified

### API Times Out

- Increase timeout in Procfile (already set to 120s)
- Use smaller YOLO model (nano is fastest)
- Check Railway memory limits

### CORS Errors

- Flask-CORS is configured for all origins
- Check that API URL is correct in React app

## 🎉 Success!

Once both are deployed:

1. Visit your frontend URL
2. Upload a theme park image
3. Get real-time crowd detection!

---

**Need help?** Railway has great docs at [docs.railway.app](https://docs.railway.app)
