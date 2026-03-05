"""
Flask API Backend for YOLO v11 Object Detection
Exposes REST API endpoint for the React frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import io
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

class YOLODetector:
    def __init__(self):
        """Initialize latest YOLO model"""
        print("🚀 Loading latest YOLO model...")
        # Try latest versions in order: v12, v11 (fallback)
        try:
            self.model = YOLO('yolo12n.pt')  # Latest version
            print("✅ YOLO v12 model loaded successfully!")
        except:
            print("⚠️ YOLO v12 not available, using v11...")
            self.model = YOLO('yolo11n.pt')  # Fallback to v11
            print("✅ YOLO v11 model loaded successfully!")
    
    def detect_people(self, image_bytes):
        """
        Detect people in the image using YOLO v11
        Returns: dict with person count, density, bounding boxes, and annotated image
        """
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        image_np = np.array(image)
        
        # Run YOLO detection (class 0 = person, confidence >= 0.3)
        results = self.model(image_np, classes=[0], conf=0.3)
        
        # Get detections
        boxes = results[0].boxes
        person_count = len(boxes)
        
        # Extract bounding box data
        detections = []
        for box in boxes:
            bbox = box.xyxy[0].cpu().numpy()  # [x1, y1, x2, y2]
            confidence = float(box.conf[0].cpu().numpy())
            detections.append({
                'bbox': [float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])],
                'confidence': confidence
            })
        
        # Create annotated image
        annotated_image = results[0].plot()
        
        # Convert annotated image to base64
        annotated_pil = Image.fromarray(annotated_image)
        buffer = io.BytesIO()
        annotated_pil.save(buffer, format='PNG')
        annotated_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Calculate crowd density
        image_area = image_np.shape[0] * image_np.shape[1]
        density = (person_count / image_area) * 1000000 if image_area > 0 else 0
        
        return {
            'personCount': person_count,
            'density': density,
            'detections': detections,
            'annotatedImage': annotated_base64,
            'imageWidth': image_np.shape[1],
            'imageHeight': image_np.shape[0]
        }

# Initialize detector
detector = YOLODetector()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'model': 'YOLOv11'})

@app.route('/api/detect', methods=['POST'])
def detect():
    """
    Main detection endpoint
    Expects: multipart/form-data with 'image' file
    Returns: JSON with detection results
    """
    try:
        # Check if image file is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        # Read image bytes
        image_bytes = file.read()
        
        # Run detection
        result = detector.detect_people(image_bytes)
        
        return jsonify(result), 200
    
    except Exception as e:
        print(f"❌ Error during detection: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    print("🌐 Starting YOLO v11 API Server...")
    port = int(os.environ.get('PORT', 5000))
    print(f"📡 API will be available at: http://0.0.0.0:{port}")
    print("🔗 React frontend should connect to: /api/detect")
    app.run(host='0.0.0.0', port=port, debug=False)
