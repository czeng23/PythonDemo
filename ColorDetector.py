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

        frame1 = cv2.boxFilter(frame, -1, (9, 9))

        #Converted to hsv since its easier for easy color comparison
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

        #Obtain hsv value for the center square
        cnt_hsv = hsv[210:310, 250:350]

        h, s, v = cv2.split(cnt_hsv)

        # obtaining average value of hue, saturation, value
        hch = int(h.mean())
        sch = int(s.mean())
        vch = int(v.mean())

        #obtaining max value of hue, saturation, value
        hmax = int(h.max())
        smax = int(s.max())
        vmax = int(v.max())

        # obtaining minimum value of hue, saturation, value
        hmin = int(h.min())
        smin = int(s.min())
        vmin = int(v.min())

        mask = cv2.inRange(hsv1, hsv_lower, hsv_upper)

        result = cv2.bitwise_and(frame1, frame1, mask=mask)

        # This line draws a rectangle with the numbers inside being the parameters. THe first two numbers are the first point while the 2nd set of numbers are the 2nd point.
        cv2.rectangle(frame, (260, 240), (320, 300), (255, 0, 0), 2)

        #Declaring what font we are going to use
        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.rectangle(frame, (0, 400), (640, 480), (0, 0, 0), -1)

        #This line displays the image, and display of the image
        display = "h = " + str(hch) + " s = " + str(sch) + " v = " + str(vch)
        display1 = "hmax = " + str(hsv_upper[0]) + " smax = " + str(hsv_upper[1]) + " vmax = " + str(hsv_upper[2])
        display2 = "hmin = " + str(hsv_lower[0]) + " smin = " + str(hsv_lower[1]) + " vmin = " + str(hsv_lower[2])

        #Puts info on screen
        cv2.putText(frame, display, (10, 420), font, 0.5, (255, 255, 255), 2, cv2.LINE_8)
        cv2.putText(frame, display1, (10, 440), font, 0.5, (0, 0, 255), 2, cv2.LINE_8)
        cv2.putText(frame, display2, (10, 460), font, 0.5, (0, 255, 0), 2, cv2.LINE_8)

        # show the images
        cv2.imshow("Raw Frame", frame)
        # cv2.imshow("Mask", mask)
        cv2.imshow("Filtered Result", result)

        key = cv2.waitKey(1)

        if key == 27:  # When escape key is pressed it breaks the program
            break

        # When the s button is pressed, it creates a new mask
        if key == 115:  # 's' key
            hsv_lower = np.array([hmin, smin, vmin])
            hsv_upper = np.array([hmax, smax, vmax])

        # resets when pressed r
        if key == 114:  # 'r' key
            hsv_lower = np.array([0, 0, 0])
            hsv_upper = np.array([255, 255, 255])

    cap.release()
    cv2.destroyAllWindows()


if __name__ =="__main__":
    args = len(sys.argv) - 1
    camera = 0
    if (args > 0) :
        camera = (int(sys.argv[1]))
    main(camera)
