#!/usr/bin/env python3

import cv2
import numpy as np
import sys

def main(camera = 0):
    cap = cv2.VideoCapture(camera)
    hsv_lower = np.array([0, 0, 0])
    hsv_upper = np.array([255, 255, 255])

    while True:
        _, frame = cap.read()

        #Blur is used to remove noise so the color detection can be consistent
        frame1 = cv2.GaussianBlur(frame, (85, 85), 0)

        #Converting BGR to HSV is used for consistency
        hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

        #Records and detects hsv is a designated square
        cnt_hsv = hsv1[240:300, 260:320]

        #split the hsv values
        h, s, v = cv2.split(cnt_hsv)

        #Average hsv
        hch = int(h.mean())
        sch = int(s.mean())
        vch = int(v.mean())

        # max hsv
        hmax = min(int(h.max()) + 20, 255)
        smax = min(int(s.max()) + 40, 255)
        vmax = min(int(v.max()) + 40, 255)

        # min hsv
        hmin = max(int(h.min()) - 1, 0)
        smin = max(int(s.min()) - 1, 0)
        vmin = max(int(v.min()) - 1, 0)

        # creates a mask
        mask = cv2.inRange(hsv1, hsv_lower, hsv_upper)

        #prints result
        result = cv2.bitwise_and(frame1, frame1, mask=mask)

        # converts to grayscale for accuracy
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

        #creates threshold
        _, thresh1 = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        #Creates contours, or center points
        contours, hierarchy_ = cv2.findContours(thresh1, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        cv2.drawContours(frame, contours, -1, (0, 0, 255), 6)

        # Finds these contours
        if (len(contours) > 0):
            M = cv2.moments(contours[0])
            if ((M["m00"]) != 0):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)

        # draws a blue rectangle for selection
        cv2.rectangle(frame, (260, 240), (320, 300), (255, 0, 0), 2)

        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.rectangle(frame, (0, 400), (640, 480), (0, 0, 0), -1)

        display = "h = " + str(hch) + " s = " + str(sch) + " v = " + str(vch) + " X = " + str(cX) + " Y = " + str(cY)
        display1 = "hmax = " + str(hsv_upper[0]) + " smax = " + str(hsv_upper[1]) + " vmax = " + str(hsv_upper[2])
        display2 = "hmin = " + str(hsv_lower[0]) + " smin = " + str(hsv_lower[1]) + " vmin = " + str(hsv_lower[2])

        # top line hsv mean value
        cv2.putText(frame, display, (10, 420), font, 0.5, (255, 255, 255), 2, cv2.LINE_8)
        # middle line upper hsv limit
        cv2.putText(frame, display1, (10, 440), font, 0.5, (0, 0, 255), 2, cv2.LINE_8)
        # bottom line min hsv limit
        cv2.putText(frame, display2, (10, 460), font, 0.5, (0, 255, 0), 2, cv2.LINE_8)

        # show the images
        cv2.imshow("Raw Frame", frame)
        cv2.imshow("Threshold", thresh1)
        cv2.imshow("Filtered Result", result)

        # check if a key is pressed
        key = cv2.waitKey(1)

        if key == 27:  # 'Esc exit
            break

        # set the new mask setting
        if key == 115:  # 's' key
            hsv_lower = np.array([hmin, smin, vmin])
            hsv_upper = np.array([hmax, smax, vmax])

        # reset to include all color
        if key == 114:  # 'r' key
            hsv_lower = np.array([0, 0, 0])
            hsv_upper = np.array([255, 255, 255])

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # pick a camera
    args = len(sys.argv) - 1
    camera = 0
    if (args > 0):
            camera = (int(sys.argv[1]))
    main(camera)