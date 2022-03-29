#detect color the pic must be in HSv
import cv2 as cv
import numpy as np

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv.cvtColor( imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
        return ver

def empty(a):
    pass
path="sources/img.png"
cv.namedWindow("trackbar")
cv.resizeWindow("trackbar",640,480)


cv.createTrackbar("HUE min","trackbar",0,179,empty)
cv.createTrackbar("HUE max","trackbar",179,179,empty)
cv.createTrackbar("SAT min","trackbar",0,255,empty)
cv.createTrackbar("SAT max","trackbar",255,255,empty)
cv.createTrackbar("VAL min","trackbar",0,255,empty)
cv.createTrackbar("VAL max","trackbar",255,255,empty)

while True:
    img=cv.imread(path)
    imgHSV=cv.cvtColor(img,cv.COLOR_BGR2HSV)
    hmin = cv.getTrackbarPos("HUE min","trackbar")
    hmax = cv.getTrackbarPos("HUE max", "trackbar")
    smin = cv.getTrackbarPos("SAT min", "trackbar")
    smax = cv.getTrackbarPos("SAT max", "trackbar")
    vmin = cv.getTrackbarPos("VAL min", "trackbar")
    vmax = cv.getTrackbarPos("VAL max", "trackbar")
    print(hmin,hmax,smin,smax,vmin,vmax)
    lower=np.array([hmin,smin,vmin])
    upper=np.array([hmax,smax,vmax])
    mask=cv.inRange(imgHSV,lower,upper)
    result=cv.bitwise_and(img,img,mask=mask)

    imgfinally=stackImages(0.6,([img,imgHSV],[mask,result]))
    cv.imshow("all",imgfinally)

    if cv.waitKey(1) & 0xFF==ord('q'):
        break