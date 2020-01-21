import subprocess as sp
import numpy as np
import cv2 as cv


def change():
    pass


def show():
    adbCmd = ['adb', 'shell', 'screenrecord', '--output-format=h264', '-']
    stream = sp.Popen(adbCmd, stdout=sp.PIPE, universal_newlines=True)
    ffmpegCmd = ['ffmpeg', '-i', '-', '-f', 'rawvideo', '-vcodec', 'bmp', '-vf', 'fps=10', '-']
    ffmpeg = sp.Popen(ffmpegCmd, stdin=stream.stdout, stdout=sp.PIPE)
    cv.namedWindow('image', flags=cv.WINDOW_NORMAL)
    cv.resizeWindow('image', 1800, 1100)
    cv.createTrackbar("filter", "image", 0, 1, change)

    while True:
        fileSizeBytes = ffmpeg.stdout.read(6)
        fileSize = 0
        if len(fileSizeBytes) != 6:
            ffmpeg.terminate()
            stream.terminate()
            cv.circle(image, (int(h / 2), int(w / 2)), 63, 0, -1)
            if cv.getTrackbarPos("filter", "image"):
                cv.imshow("image", org)
            else:
                cv.imshow("image", image)
            show()

        for i in range(4):
            fileSize += fileSizeBytes[i + 2] * 256 ** i
        bmpData = fileSizeBytes + ffmpeg.stdout.read(fileSize - 6)
        org = cv.imdecode(np.fromstring(bmpData, np.uint8), 0)

        kernel = np.ones((5, 5), np.float32) / 25
        image = cv.filter2D(org, -1, kernel)
        image = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 13, 2)
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

show()
