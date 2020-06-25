import cv2
import numpy as np
### Counters or Shape detection ###
### Stack function, which can join images ###
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
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
##########################################
def get_shape(img):
    shapes, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for s in shapes:
        area = cv2.contourArea(s)
        print("Area of the contor",area)
        if area >= 1000:
            cv2.drawContours(img_copy, s, -1, (255,0,0), 2)
            # perimeter  = cv2.arcLength(s, True)
            # approx = cv2.approxPolyDP(s, 0.02*perimeter, True)
            # No_corners = len(approx)
            # x, y, w, h = cv2.boundingRect(approx)
            # print("No of corners of that contor", No_corners)
            # if No_corners == 3:
            #     object_shape = "Triangle"
            # elif No_corners == 4:
            #     asratio = float(w)/float(h)
            #     if asratio > 0.9 and asratio < 1.03:
            #         object_shape = "Square"
            #     else: object_shape = "Rectangle"
            # elif No_corners > 4:
            #     object_shape = "Circle"
            # else:
            #     object_shape = "None"

            #cv2.rectangle(img_copy, (x,y), (x+w, y+h), (0,0,255), 2)
            #cv2.putText(img_copy, object_shape, (x, y-8), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)


pic = cv2.imread("Data/2d.png")
img = cv2.resize(pic, (640,480))
img_canny = cv2.Canny(img, 150,150)
img_copy = img.copy()
get_shape(img_canny)
# cv2.imshow("image", img)
# cv2.imshow("Canny_image", img_canny)
img_stack = stackImages(0.8, [img, img_canny, img_copy])
cv2.imshow("Stacked _img", img_stack)
cv2.waitKey(0)