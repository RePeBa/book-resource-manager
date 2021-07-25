import cv2
import time

video = cv2.VideoCapture(0)

check, frame = video.read()

print(check)
print(frame)

gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)


cv2.imshow("View", gray)

cv2.imwrite("AAA.jpg", gray)

print( "If the image is acceptable press any key to subbmit") # TODO - improve format and funcionality

cv2.waitKey(0)

video.release()