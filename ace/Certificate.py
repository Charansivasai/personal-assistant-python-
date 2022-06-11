
from PIL import ImageFont, ImageDraw, Image  
import cv2  
import numpy as np  
import os
import csv

f = open("names.txt","r")
names_list = f.read().split("\n")
#print(names_list)

f1 = open("coords.txt","r")
coordinates = f1.read().split("\n")

flag=True

for i in range(len(names_list)):


    name_to_print = names_list[i]
    #date_to_print = "30/10/2021"  
 
    image = cv2.imread("cse.jpg")  

    cv2_im_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)  

  
    pil_im = Image.fromarray(cv2_im_rgb)  

    draw = ImageDraw.Draw(pil_im)  

    font = ImageFont.truetype("./fonts/Lato-Black.ttf", 40)     
    font1 = ImageFont.truetype("./fonts/MLSJN.ttf", 22) 

    
    draw.text((int(coordinates[0]), int(coordinates[1])), name_to_print, font=font , fill='black')
    #draw.text((int(coordinates[2]), int(coordinates[3])), date_to_print , font=font1, fill='blue')
    
    cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)  
    
    if flag:
        cv2.imshow('Certificate', cv2_im_processed) 
        flag=False
    path = ''
    cv2.imwrite('./output/'+name_to_print+'.png',cv2_im_processed)

    cv2.waitKey(0)  

    cv2.destroyAllWindows()

