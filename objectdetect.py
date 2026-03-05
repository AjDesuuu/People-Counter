"""
YOLO v11 Object Detection System for Theme Park Crowd Analysis
Real-time person detection with crowd-based recommendations
"""

import gradio as gr
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class ThemeParkDetector:
    def __init__(self):
        """Initialize YOLO v11 model for person detection"""
        print("Loading YOLO v11 model...")
        # Load YOLOv11 nano model (you can use yolo11n.pt, yolo11s.pt, yolo11m.pt, yolo11l.pt, yolo11x.pt)
        self.model = YOLO('yolo11n.pt')  # Fastest, good for real-time
        print("Model loaded successfully!")
        
    def detect_people(self, image):
        """
        Detect people in the image using YOLO v11
        Returns: annotated image, person count, crowd density, recommendations
        """
        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Run YOLO detection
        results = self.model(image, classes=[0], conf=0.3)  # class 0 = person, confidence threshold 0.3
        
        # Get detections
        boxes = results[0].boxes
        person_count = len(boxes)
        
        # Create annotated image
        annotated_image = results[0].plot()
        
        # Calculate crowd density (people per 1000 pixels²)
        image_area = image.shape[0] * image.shape[1]
        density = (person_count / image_area) * 1000000  # per million pixels
        
        # Generate recommendations
        recommendations = self.generate_recommendations(person_count, density)
        
        # Create detailed statistics
        stats = self.create_statistics(person_count, density, boxes)
        
        return annotated_image, person_count, density, recommendations, stats
    
    def generate_recommendations(self, person_count, density):
        """
        Generate crowd-based recommendations for theme park visitors
        """
        recommendations = []
        
        # Crowd level assessment
        if density < 5:
            crowd_level = "🟢 LOW CROWD"
            recommendations.append("✅ Perfect time to visit! Minimal wait times expected.")
            recommendations.append("🎢 All attractions are likely available with short queues.")
            recommendations.append("📸 Great opportunity for photos without crowds.")
        elif density < 15:
            crowd_level = "🟡 MODERATE CROWD"
            recommendations.append("⚠️ Moderate crowding. Plan your route efficiently.")
            recommendations.append("🎫 Consider using FastPass/Express lanes for popular rides.")
            recommendations.append("🍽️ Restaurants may have 15-30 minute wait times.")
        elif density < 30:
            crowd_level = "🟠 HIGH CROWD"
            recommendations.append("⚠️ High crowd levels detected!")
            recommendations.append("🏃 Visit less popular attractions first.")
            recommendations.append("⏰ Peak hours - consider taking a break and returning later.")
            recommendations.append("🎭 Focus on shows and indoor attractions.")
        else:
            crowd_level = "🔴 VERY HIGH CROWD"
            recommendations.append("🚨 Extreme crowding! Consider alternative areas.")
            recommendations.append("💡 Visit shops, restaurants, or rest areas.")
            recommendations.append("🕐 Return during off-peak hours (early morning/late evening).")
            recommendations.append("🎪 Check live crowd maps for less busy zones.")
        
        # Person count specific recommendations
        if person_count > 50:
            recommendations.append(f"👥 {person_count} people detected - Area is very busy!")
        elif person_count > 20:
            recommendations.append(f"👥 {person_count} people detected - Busy area, plan accordingly.")
        elif person_count > 10:
            recommendations.append(f"👥 {person_count} people detected - Moderate activity.")
        else:
            recommendations.append(f"👥 {person_count} people detected - Low activity, great time to explore!")
        
        # Safety recommendations
        if person_count > 30:
            recommendations.append("🛡️ Safety: Maintain social distancing where possible.")
            recommendations.append("⚠️ Keep belongings secure in crowded areas.")
        
        result = f"\n{crowd_level}\n\n" + "\n\n".join(recommendations)
        return result
    
    def create_statistics(self, person_count, density, boxes):
        """
        Create detailed statistics about the detection
        """
        stats = f"""
📊 **Detection Statistics**

👤 **Total People Detected:** {person_count}
📏 **Crowd Density:** {density:.2f} people per million pixels
🎯 **Detection Confidence:** {len(boxes)} confident detections

🔍 **Detection Details:**
"""
        
        if len(boxes) > 0:
            confidences = [box.conf.item() for box in boxes]
            avg_confidence = np.mean(confidences)
            max_confidence = np.max(confidences)
            min_confidence = np.min(confidences)
            
            stats += f"""
• Average Confidence: {avg_confidence:.2%}
• Highest Confidence: {max_confidence:.2%}
• Lowest Confidence: {min_confidence:.2%}
"""
        else:
            stats += "\n• No people detected in the image"
        
        return stats


def create_ui():
    """
    Create Gradio interface for the detection system
    """
    detector = ThemeParkDetector()
    
    def process_image(image):
        """Process uploaded image and return results"""
        if image is None:
            return None, "❌ Please upload an image", "", ""
        
        annotated_img, count, density, recommendations, stats = detector.detect_people(image)
        
        # Create summary header
        summary = f"**👥 PEOPLE COUNT: {count}**"
        
        return annotated_img, summary, recommendations, stats
    
    # Create Gradio interface
    with gr.Blocks(title="Theme Park Crowd Detection System", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🎢 Theme Park Crowd Detection System
        ### Powered by YOLO v11 - Real-time Person Detection & Smart Recommendations
        
        Upload a CCTV image or photo from your theme park to:
        - 👥 Count the number of people
        - 📊 Analyze crowd density
        - 💡 Receive personalized recommendations
        """)
        
        with gr.Row():
            with gr.Column():
                input_image = gr.Image(
                    label="📤 Upload Theme Park Image (CCTV or Photo)",
                    type="pil",
                    height=400
                )
                detect_btn = gr.Button("🔍 Analyze Crowd", variant="primary", size="lg")
                
                gr.Markdown("""
                ### 📝 Instructions:
                1. Upload an image from your theme park CCTV or camera
                2. Click "Analyze Crowd" to detect people
                3. View results and recommendations below
                
                **Supported formats:** JPG, PNG, JPEG
                """)
            
            with gr.Column():
                output_image = gr.Image(
                    label="🎯 Detection Results (with bounding boxes)",
                    height=400
                )
                person_count_display = gr.Markdown(
                    label="📊 People Count",
                    value="**Awaiting analysis...**"
                )
        
        with gr.Row():
            with gr.Column():
                recommendations_display = gr.Textbox(
                    label="💡 Smart Recommendations",
                    lines=12,
                    interactive=False
                )
            
            with gr.Column():
                stats_display = gr.Textbox(
                    label="📊 Detailed Statistics",
                    lines=12,
                    interactive=False
                )
        
        # Examples section
        gr.Markdown("""
        ### 💡 Tips for Best Results:
        - Use clear images with good lighting
        - CCTV footage works best when captured from elevated angles
        - Higher resolution images provide more accurate counts
        - The system detects people with 30%+ confidence threshold
        """)
        
        # Connect the button
        detect_btn.click(
            fn=process_image,
            inputs=[input_image],
            outputs=[output_image, person_count_display, recommendations_display, stats_display]
        )
    
    return demo


if __name__ == "__main__":
    print("🚀 Starting Theme Park Crowd Detection System...")
    print("📦 Initializing YOLO v11...")
    
    # Create and launch the interface
    demo = create_ui()
    
    print("✅ System ready!")
    print("🌐 Launching web interface...")
    
    # Launch with options
    demo.launch(
        share=False,  # Set to True to create a public link
        server_name="0.0.0.0",  # Allow access from network
        server_port=7860,
        show_error=True
    )
