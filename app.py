from flask import Flask, render_template, Response, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# Initialize global variables
cap = cv2.VideoCapture(0)
track_window = None
roi_hist = None
can_track = False

# CamShift termination criteria
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

def initialize_tracker(frame, track_window):
    """Initialize tracking region based on user selection."""
    x, y, w, h = track_window
    roi = frame[y:y+h, x:x+w]
    
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
    roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
    roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
    
    return roi_hist

def generate_frames():
    """Continuously capture frames and apply tracking if enabled."""
    global track_window, roi_hist, can_track

    while True:
        success, frame = cap.read()
        if not success:
            break
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        if can_track and roi_hist is not None and track_window is not None:
            dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
            ret, track_window = cv2.CamShift(dst, track_window, term_crit)
            
            pts = cv2.boxPoints(ret)
            pts = np.int0(pts)
            frame = cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/set_roi', methods=['POST'])
def set_roi():
    """Receive selection coordinates from frontend."""
    global track_window, roi_hist, can_track

    data = request.json
    x, y, w, h = data['x'], data['y'], data['w'], data['h']

    if w > 5 and h > 5:  # Ensure valid selection
        track_window = (x, y, w, h)
        roi_hist = initialize_tracker(cap.read()[1], track_window)
        can_track = True
        return jsonify({"status": "Tracking initialized"}), 200
    else:
        return jsonify({"error": "Invalid selection"}), 400

@app.route('/stop_tracking', methods=['POST'])
def stop_tracking():
    """Stop tracking when requested by the frontend."""
    global can_track
    can_track = False
    return jsonify({"status": "Tracking stopped"}), 200

@app.route('/')
def index():
    """Render the frontend."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Stream the video to the frontend."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
