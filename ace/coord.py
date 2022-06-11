


import numpy as np
import cv2 as cv

f = open("coords.txt","w")


def draw_circle(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        

        cv.putText(img,"coordinates (%d,%d)"%(x,y),(60,60),2,1,(0,255,0)) 
        f.write(str(x)+"\n")                                              
        f.write(str(y)+"\n")                                              #DOUBLE CLICK TO SELECT
                                                                           #COORDS WITH GREEN TEXT WILL BE DISPLAYED
# Create a black image, a window and bind the function to window
img = cv.imread("cse.jpg")



cv.namedWindow('image')
cv.setMouseCallback('image',draw_circle)
while(1):
    cv.imshow('image',img)
    if cv.waitKey(10) & 0xFF == 27:   #Press Escape Key to terminate window
        break
cv.destroyAllWindows()   

f.close()
