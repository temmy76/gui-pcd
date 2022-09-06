from ast import For
from operator import length_hint
from turtle import width
import cv2 as cv

image = cv.imread("static/uploads/foto.jpg",1)
# cv.imshow('testing', image)
# cv.waitKey(0)
# cv.destroyAllWindows()

reso = image.shape 


width = reso[1]
length = reso[0]
rgb = []
for i in range(length-1):
    for j in range(width-1):
        rgb.append(image[i,j])
RGB2 = []
for i in range(len(rgb)):
    RGB2[i] = rgb[i]

print(RGB2)