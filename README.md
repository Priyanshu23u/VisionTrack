# Object Tracking with OpenCV & Flask

## Overview
This project is a **real-time object tracking system** built using **OpenCV** and **Flask**. It allows users to select an object in a live webcam feed and track its movement dynamically using the **CamShift algorithm**.

## Features
- Real-time **object tracking** using OpenCV
- Interactive web-based **object selection**
- Live video streaming via **Flask & OpenCV**
- Backend API to **start, stop, and reset tracking**
- Uses **HSV color space & histogram back-projection** for robust tracking
- User-friendly **web interface** with JavaScript-based ROI selection

## Tech Stack
### **Frontend**
- HTML, CSS, JavaScript (Fetch API)
- Flask (Jinja2 Templating for rendering pages)

### **Backend**
- Python (Flask Framework)
- OpenCV (cv2) for real-time video processing
- NumPy for image processing operations

## Installation & Setup
### **1. Clone the Repository**
```bash
git clone https://github.com/your-repo/object-tracking.git
cd object-tracking
```

### **2. Install Dependencies**
```bash
pip install flask opencv-python numpy
```

### **3. Run the Application**
```bash
python app.py
```

### **4. Open in Browser**
Go to:  
```
http://127.0.0.1:5000/
```

## Usage Instructions
1. Open the web interface.
2. Click and drag on the video feed to **select an object**.
3. The system will start tracking the selected object in real-time.
4. Click **Stop Tracking** to halt the process.

## Project Structure
```
📂 object-tracking/
├── 📄 app.py        # Flask backend & OpenCV tracking logic
├── 📄 main.py       # Standalone OpenCV tracker (alternative)
├── 📄 index.html    # Frontend UI
├── 📄 README.md     # Project documentation
```

## Future Enhancements
- Implement **multiple object tracking**.
- Improve tracking accuracy with **Deep Learning (YOLO/SSD)**.
- Deploy as a **web application using Docker & cloud services**.

