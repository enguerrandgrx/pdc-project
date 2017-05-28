
# coding: utf-8

# In[1]:

import numpy as np
import cv2
from matplotlib import pyplot as plt
import time
import math
import sys
import copy

col = 0
copieImg = 0
# Part 1: Screen detection
# ================

# In[2]:

#this function take the center of the image
def resize(im):
    x = im.shape[0]
    y = im.shape[1]
    return im[int(x/3):int(2*x/3), int(y/3):int(2*y/3)]


# In[3]:

def find_screen(cnts, image):
    global col
    total = 0
    approx_tmp = 0
    approx = []
    # loop over the contours
    #print("cnts")
    #print(cnts)
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        #print("perimetre ", peri)
        approx_tmp = cv2.approxPolyDP(c, 0.02 * peri, True)
        approx_tmp = np.squeeze(approx_tmp)
        #print(approx)
        #cv2.drawContours(image, [approx_tmp], -1, (0, 255, 0), 4)
        #print("approx_tmp ",approx_tmp)
        #print("len approx_tmp",len(approx_tmp))
        print("perimetre: ", peri)
        print(approx_tmp)
        #cv2.drawContours(copieImg, [approx_tmp], -1, (col, 255-col, col), 4)

        if (peri > 100 and peri < 400 and len(approx_tmp) == 4):
            approx.append(approx_tmp)
            print(approx)

            cv2.drawContours(copieImg, [approx_tmp], -1, (col, 255-col, col), 4)
            cv2.imwrite('img_CV2_90.jpg', copieImg)

            #col = col + 50

    #plt.show()
    # print("approx ",approx)
    # print("len approx ",len(approx))
    return approx


# In[4]:

def bords(approx):

    print(approx)
    # if(len(approx) == 2):
    #     approx = np.concatenate((approx[0], approx[1]), axis = 0)
    # approx = np.squeeze(approx)
    bord = []
    min_x = sys.maxsize
    max_x = 0
    min_y = sys.maxsize
    max_y = 0
    #config = -1
    if(len(approx) == 1):
        approx = approx[0]
    #print("approx 0 ",approx)

    for appro in approx:
        if appro[0] > max_x:
            max_x = appro[0]
        if appro[0] < min_x:
            min_x = appro[0]
        if appro[1] > max_y:
            max_y = appro[1]
        if appro[1] < min_y:
            min_y = appro[1]

    bord.extend([min_x, max_x, min_y, max_y])

    # if(len(approx) == 4):
    #     if(max_x - min_x > max_y - min_y):
    #         config = 2
    #     else:
    #         config = 1
    # else:
    #     approx_x = approx[:,0]
    #     approx_y = approx[:,1]
    #     fit = np.polyfit(approx_x,approx_y,1)
    #     if(fit[0] < 0):
    #         config = 3
    #     else:
    #         config = 4
    # return bord,config

    return bord


# In[5]:

def detection(path, color = 0): # --------
    start_time = time.time()
    if(type(path) == str):
        img = cv2.imread(path)
        path = img
    img = resize(path)
    #on split l'image en fonction des couleurs
    b,g,r = cv2.split(img)

    #print("--- %s seconds ---" % (time.time() - start_time))

    # on parcours l'image et on mets r a 0 si b ou r superieur a un seuil (ici 50)
    for x in range(0, r.shape[0]):
        for y in range(0, r.shape[1]):
            if color == 0:
                if(b[x][y] < 80 and g[x][y] < 70 and r[x][y] > 160):
                    r[x][y] = 255
                else:
                    r[x][y] = 0
            elif color == 1:
                if(r[x][y] < 130 and b[x][y] < 140 and g[x][y] > 150):
                    g[x][y] = 255
                else:
                    g[x][y] = 0
            elif color == 2:
                if(r[x][y] < 60 and g[x][y] < 30 and b[x][y] > 200):
                    b[x][y] = 255
                else:
                    b[x][y] = 0
            elif color == 3:
                if(r[x][y] > 100 and g[x][y] < 70 and b[x][y] > 160):
                    r[x][y] = 255
                else:
                    r[x][y] = 0


    #print("--- %s seconds ---" % (time.time() - start_time))

    #cv2.imwrite('img_CV2_90.jpg', r)

    # on applique un filtre binaire
    if (color == 0 or color == 3):
        ret,seg = cv2.threshold(r,150,255.0,cv2.THRESH_BINARY)
    elif color == 1:
        ret,seg = cv2.threshold(g,150,255.0,cv2.THRESH_BINARY)
    elif color == 2:
        ret,seg = cv2.threshold(b,150,255.0,cv2.THRESH_BINARY)

    # cv2.imwrite('img_CV2_90.jpg', seg)
    # detecte
    edged = cv2.Canny(seg, 100, 100)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    im2, cnts, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



    #print(cnts)
    if(cnts == []):
        return [],[]
    approx = find_screen(cnts, img)
    if(approx == []):
        return [],[]
    bord = bords(approx)

    # if(not (bord == [])):
    #     plt.imshow(img)
    #     plt.show()

    #plt.show()
    sucess = True
    print(approx)

    print("les 4 bords de l'ecrans sont : ", bord)
    #print("la configuration est la n°", config)
    print("--- %s seconds ---" % (time.time() - start_time))

    return bord,sucess



# In[6]:

# bord1, config1, sucss = detection('screen_red1.png')
#
#
# # In[7]:
#
# bord2, config2, s = detection('screen_red2.png')
#
#
# # In[8]:
#
# bord3, config3, s = detection('screen_red3.png')
#
#
# # In[9]:
#
# bord4, config4, s = detection('screen_red4.png')


# Part 2: Color detection
# ================

# In[10]:

def color_detection (bord, config, path):
    if(type(path) == str):
        img = cv2.imread(path)
        path = img
    elif(type(path) == None):
        return 'end'

    img = resize(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # bords = [min_x, max_x, min_y, max_y]

    im1 = []
    im2 = []
    colors1 = []
    colors2 = []
    # ========================= A Verifier ======================
    (min_y, max_y, min_x, max_x) = bord
    #(min_x, max_x, min_y, max_y) = bord
    mid_x = int( min_x + (max_x - min_x)/2)
    mid_y = int( min_y + (max_y - min_y)/2)
    #print("mid_x",mid_x)
    #print("mid_y",mid_y)

    #print("min x : ", min_x, " max_x : ", max_x, " min y: ", min_y, " max y: ", max_y)
    if(config == 2):
        #Image dans la hauteur - ie
        im1 = img[min_x: max_x, min_y: mid_y ]
        im2 = img[min_x: max_x , mid_y:max_y ]
    elif(config == 1):
        #Image dans la Longeur - ie
        im1 = img[min_x : mid_x , min_y:max_y]
        im2 = img[mid_x : max_x, min_y:max_y]
    elif(config == 3):
        #Image dans  - ie
        im1 = img[min_x : mid_x, mid_y : max_y]
        im2 = img[mid_x : max_x, min_y : mid_y]
    elif(config == 4):
        #Image dans  - ie
        im1 = img[min_x : mid_x , min_y : mid_y]
        im2 = img[mid_x : max_x, mid_y : max_y]



    colors1 = cutting(im1, 3, 3)
    colors2 = cutting(im2, 3, 3)
    if(colors1 == colors2):
        return colors1
    else:
        print("Error 1 : ", colors1)
        print("Error 2 : ", colors2)
        print("Image 1")
        plt.imshow(im1)
        plt.imshow(im2)
        plt.show()
        time.sleep(5)
        plt.close()

        print("Image 2")
        #plt.imshow(im2)
        #plt.show()
        return 'error'



# In[11]:

# this function take an image and two index,
def cutting(img, indexX, indexY):
    colors = []
    x = img.shape[0]
    y = img.shape[1]
    #print("x cutting",x)
    #print("y cutting",y)
    for i in range(0,indexX):
        #print("Index of i:", i)
        for j in range(0, indexY):
            #print("Index of j:", j)
            imTmp = img[int((i)*x/indexX):int((i+1)*x/indexX), int((j)*y/indexY):int((j+1)*y/indexY)]
            #plt.imshow(imTmp)
            #plt.show()
            color = find_color(imTmp)
            colors.append(color)
    return colors


# In[12]:

rgb_dictionary = {
    #
    (255,0,0): 'red',
    (0,255,0):'green',
    #(0,255,250):'blue_cian',
    (0,0,255): 'blue'
    #(255, 255,0): 'yellow',
    #(255, 0, 255): 'Magenta',
    #(255, 255, 255): 'white',
    #(0,0,0): 'black'
}


# In[13]:

#This function
def distance(c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)


# In[14]:

# this function take a point and find its color
def witch_color(point):
    colors = list(rgb_dictionary.keys())
    closest_colors = sorted(colors, key=lambda color: distance(color, point))
    closest_color = closest_colors[0]
    code = rgb_dictionary[closest_color]
    return code


# In[15]:

# this function take an square and output its color
def find_color(img):
    #plt.imshow(img)
    #plt.show()
    x = img.shape[0]
    y = img.shape[1]
    #print("x",x)
    #print("y",y)
    mid = img[int(x/2), int(y/2)]
    return witch_color(mid)


# In[16]:

start_time = time.time()
#
# # print(color_detection(bord3, config3, 'color_screen3.png'))
# print("--- %s seconds ---" % (time.time() - start_time))
#

# Part 3: From Video
# ================

# In[22]:

count = 0
screen_detected = False
error = 0
config = -1
bord = []
colors = []
color_prev = ['red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red']
color_red = ['red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red']
color_blue = ['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']



cap = cv2.VideoCapture(0)
if not(cap.isOpened()):
    cap.open()
    print("pas bon")

redD = 0
blueD = 0
greenD = 1
pinkD = 1
while(True):
    ret, frame = cap.read()
    k= cv2.waitKey(1)
    if k == ord('q'):#press q to quit
        break
    number_screen = 0
    copieImg = copy.copy(resize(frame))
    for i in range(4):
        if i == 0 and redD == 0:
            print("RED")
            bord, screen_detected = detection(frame, i)
            print(bord)

            if screen_detected:
                redD = 1
        elif i == 1 and greenD == 0:
            print("GREEN")
            bord, screen_detected = detection(frame, i)
            print(bord)

            if screen_detected:
                greenD = 1
        elif i == 2 and blueD == 0:
            print("BLUE")
            bord, screen_detected = detection(frame, i)
            if screen_detected:
                blueD = 1
        elif i == 3 and pinkD == 0:
            print("PINK")
            bord, screen_detected = detection(frame, i)
            if screen_detected:
                pinkD = 1

        screen_detected = redD + blueD + greenD + pinkD

    if(screen_detected == 4):
        print("screen detected = ", screen_detected)
        break
    count += 1
    print(count)

print("total nb of round : ",count)
print("detected colors : ",colors)
print("--- %s seconds ---" % (time.time() - start_time))

erreur = False

while(True):
    ret, frame = cap.read()
    color = color_detection(bord, config, frame)
    #print("color",color)
    if(not (color == color_red)):
#        print("color",color)
        if (color == color_prev):
            b = "papate"
        elif(color == 'end'):
            color = color_blue
            print('----END----')
            break
        elif(color == None or color == 'error'):
            if erreur:
                error = error + 1
                if(error > 10):
                    break
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                erreur = True
                time.sleep(0.1)

            #plt.imshow(frame)
            #plt.show()
        else:
            print("color : ", color)
            colors.append(color)
            color_prev = color
            erreur = False



# In[23]:




# In[ ]:



# In[ ]:
