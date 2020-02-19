import numpy as np
import cv2 as cv
import sys


def change():
    pass


cap = cv.VideoCapture(int(sys.argv[1]))
# cap.set(cv.CAP_PROP_FRAME_WIDTH, 3840)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, 2160)
# cap.set(cv.CAP_PROP_FRAME_WIDTH, 2592)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1944)
#cap.set(cv.CAP_PROP_FRAME_WIDTH, 1500)
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1500)
# cap.set(cv.CAP_PROP_BRIGHTNESS, 75)


cv.namedWindow('image', flags=cv.WINDOW_NORMAL)
cv.resizeWindow('image', 1800, 1100)
cv.createTrackbar("filter", "image", 0, 1, change)

while 1:
    # Capture frame-by-frame
    ret, org = cap.read()
    image = cv.cvtColor(org, cv.COLOR_BGR2GRAY)

    kernel = np.ones((5, 5), np.float32) / 25
    image = cv.filter2D(image, -1, kernel)
    image = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)
    image = cv.medianBlur(image, 5)
    h, w = image.shape
    if h > w:
        image = cv.rotate(image, cv.ROTATE_90_COUNTERCLOCKWISE)
    if cv.getTrackbarPos("filter", "image"):
        cv.imshow("image", org)
    else:
        cv.imshow("image", image)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
