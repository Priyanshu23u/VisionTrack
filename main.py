import cv2
import numpy as np

# Naming the output window
window_name = 'Result'
cv2.namedWindow(window_name)

cap = cv2.VideoCapture(0)

x, y, w, h = 0, 0, 0, 0
first_point_saved = False
second_point_saved = False
track_window = None
can_track = False
roi_hist = None

def click_event(event, px, py, flags, param):
    global x, y, w, h, first_point_saved, second_point_saved, track_window, can_track
    
    if event == cv2.EVENT_LBUTTONDOWN:
        x, y = px, py
        first_point_saved = True
        second_point_saved = False
        can_track = False  # Stop tracking until selection is completed

    elif event == cv2.EVENT_LBUTTONUP:
        w = abs(px - x)
        h = abs(py - y)

        if w > 5 and h > 5:  # Ensure valid selection
            track_window = (min(x, px), min(y, py), w, h)
            print("Tracking Window:", track_window)
            first_point_saved = False
            second_point_saved = True
        else:
            print("Invalid selection. Please select a larger region.")

    elif event == cv2.EVENT_RBUTTONDOWN:
        can_track = False  # Stop tracking
        print("Tracking stopped.")

cv2.setMouseCallback(window_name, click_event)

# Initialize the tracker
def initialize_tracker(frame, track_window):
    x, y, w, h = track_window
    roi = frame[y:y+h, x:x+w]

    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))  # Filter for better tracking
    roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
    roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    return roi_hist

# Termination criteria for CamShift
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if second_point_saved:
        roi_hist = initialize_tracker(frame, track_window)
        second_point_saved = False
        can_track = True

    if can_track and roi_hist is not None and track_window is not None:
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)  # Convert to integer
        frame = cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

    elif first_point_saved:
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

    cv2.imshow(window_name, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
