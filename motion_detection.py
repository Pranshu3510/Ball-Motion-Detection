import cv2 as cv
import time as tm
import numpy as np

lower_hsv = np.array([35, 80, 80], dtype="uint8")
upper_hsv = np.array([85, 255, 255],dtype="uint8")

cap = cv.VideoCapture(0)

position = []
timestamp = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Convert to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # Mask only the ball color
    mask = cv.inRange(hsv, lower_hsv, upper_hsv)
    # Reduce noise
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)
    contours, _ = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    centre = None
    if len(contours) > 0:
        # Largest contour = ball by minEnclosingCircle
        c = max(contours, key=cv.contourArea)
        ((x, y), radius) = cv.minEnclosingCircle(c)
        M = cv.moments(c)
        if M["m00"] > 0:
            centre = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 10:
                # Draw ball
                cv.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
                cv.putText(frame,"Ball",(int(x)-50,int(y)-50),cv.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
                # Save history
                position.append(centre)
                timestamp.append(tm.time())
                if len(position) > 20:
                    position.pop(0)
                    timestamp.pop(0)
                # Draw trajectory
                for i in range(1,len(position)):
                    if position[i - 1] is None or position[i] is None:
                        continue
                    cv.line(frame, position[i - 1], position[i], (255,0,0), 2)
                # speed calculation
                if len(position) >= 2:
                    dx = position[-1][0] - position[-2][0]
                    dy = position[-1][1] - position[-2][1]
                    dist = np.sqrt(dx**2 + dy**2)
                    dt = timestamp[-1]-timestamp[-2]
                    if dt > 0:
                        speed = dist / dt
                        cv.putText(frame,f"Speed: {speed:.2f}",(10,30),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
    cv.imshow("Ball Motion", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()