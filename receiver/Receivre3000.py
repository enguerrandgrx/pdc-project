
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
        print("perimetre: ", peri)
        print(approx_tmp)

        if (peri > 100 and peri < 400):
            approx.append(approx_tmp)
            print(approx)

            cv2.drawContours(copieImg, [approx_tmp], -1, (col, 255-col, col), 4)
            cv2.imwrite('img_CV2_90.jpg', copieImg)

    return approx


# In[4]:

def bords(approx):

    print(approx)
   
    bord = []
    min_x = sys.maxsize
    max_x = 0
    min_y = sys.maxsize
    max_y = 0
    config = 0
    if(len(approx) == 1):
        approx = approx[0]

    for appro in approx:
        if appro[0] > max_x:
            max_x = appro[0]
        if appro[0] < min_x:
            min_x = appro[0]
        if appro[1] > max_y:
            max_y = appro[1]
        if appro[1] < min_y:
            min_y = appro[1]


    if((max_x - min_x)/(max_y - min_y)) < 1:
        config = 2
        mid_y = int( min_y + (max_y - min_y)/2)
        bord = [[min_x, max_x, min_y, mid_y],[min_x, max_x, mid_y, max_y]]


    else:
        config = 1
        bord = [min_x, max_x, min_y, max_y]

    return bord, config


# In[5]:

def detection(path, color = 0): # --------
    start_time = time.time()
    if(type(path) == str):
        img = cv2.imread(path)
        path = img
    img = resize(path)
    #on split l'image en fonction des couleurs
    b,g,r = cv2.split(img)


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




    # on applique un filtre binaire
    if (color == 0 or color == 3):
        ret,seg = cv2.threshold(r,150,255.0,cv2.THRESH_BINARY)
    elif color == 1:
        ret,seg = cv2.threshold(g,150,255.0,cv2.THRESH_BINARY)
    elif color == 2:
        ret,seg = cv2.threshold(b,150,255.0,cv2.THRESH_BINARY)

    # detecte
    edged = cv2.Canny(seg, 100, 100)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    im2, cnts, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



    if(cnts == []):
        return [],[]
    approx = find_screen(cnts, img)


    if(approx == []):
        return [],[]
    bord, sucess = bords(approx)


    print(approx)

    print("les 4 bords de l'ecrans sont : ", bord)
    print("--- %s seconds ---" % (time.time() - start_time))

    return bord,sucess




# Part 2: Color detection
# ================

# In[10]:

def color_detection (bord, path):
    if(type(path) == str):
        img = cv2.imread(path)
        path = img
    elif(type(path) == None):
        return 'end'

    img = resize(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
   
    im1 = []
    im2 = []
    colors1 = []
    colors2 = []

    (bord1, bord2) = bord
 
    im1 = img[bord1[2]:bord1[3],:]
    im2 = img[bord2[2]:bord2[3],:]

    im1 = im1[:,bord1[0]:bord1[1]]
    im2 = im2[:,bord2[0]:bord2[1]]

    colors1 = cutting(im1, 6, 4)
    colors2 = cutting(im2, 6, 4)


    return [colors1, colors2]


# In[11]:

# this function take an image and two index,
def cutting(img, indexX, indexY):
    colors = []
    x = img.shape[0]
    y = img.shape[1]
    for i in range(0,indexX):
        for j in range(0, indexY):
            imTmp = img[int((i)*x/indexX):int((i+1)*x/indexX), int((j)*y/indexY):int((j+1)*y/indexY)]

            color = find_color(imTmp)
            colors.append(color)
    return colors


# In[12]:

rgb_dictionary = {
    (0,0,0): 'black'
    (255,0,0): 'red',
    (0,255,0):'green',
    (0,0,255): 'blue'
    (0,255,255):'blue_cian',
    (255, 0, 255): 'Magenta',
    (255, 255,0): 'yellow',
    (255, 255, 255): 'white',
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
    x = img.shape[0]
    y = img.shape[1]
    mid = img[int(x/2), int(y/2)]
    return witch_color(mid)





def oct_to_ascii(s):

    dec_ascii = int(s, 8)
    asc = chr(dec_ascii)


# In[16]:

start_time = time.time()
#
#

# Part 3: From Video

# ================

# In[22]:

count = 0
screen_detected = False
error = 0
config = -1
bord = []
colors0 = []
colors1 = []

color_prev0 = []
color_prev1 = []

color_red = ['red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red']
color_blue = ['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']

bord_blue = []
bord_red = []

cap = cv2.VideoCapture(0)
if not(cap.isOpened()):
    cap.open()
    print("pas bon")

redD = 0
blueD = 0
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
            bord_red, screen_detected = detection(frame, i)
            print(bord)

            if screen_detected:
                redD = screen_detected

        elif i == 2 and blueD == 0:
            print("BLUE")
            bord_blue, screen_detected = detection(frame, i)
            if screen_detected:
                blueD = screen_detected

        screen_detected = redD + blueD

    if(screen_detected == 2):
        if(len(bord_blue) == 2):
            bord = bord_blue
        elif(len(bord_red) == 2):
            bord = bord_red
        else:
            bord = [bord_red, bord_blue]
        print("screen detected = ", screen_detected)
        print("Bords : ", bord)
        break
    count += 1
    print(count)

print("total nb of round : ",count)
print("--- %s seconds ---" % (time.time() - start_time))

error_count = 0

begin = False

counter = 0

while(True):
    time2 = time.time()
    ret, frame = cap.read()
    color = color_detection(bord, frame)

    if ((color[0] == color_red or color[0] == color_blue or color[1] == color_red or color[1] == color_blue) and not begin):
        pass
    else:
        if (color[0] == color_prev0 and color[1] == color_prev1):
            begin = True
            pass
        elif(color[0] == color_blue or color[1] == color_blue):
            print('----END----')
            break
        elif(color[0] != color[1]):
            begin = True
            error_count = error_count + 1
            if error_count > 2:
                print("-- Error, two differents colors detected --")
                print("Color 1 : ", color[0])
                print("Color 2 : ", color[1])

                colors0.append(color[0])
                colors1.append(color[1])

                color_prev0 = color[0]
                color_prev1 = color[1]

                error_count = 0
                counter = 0

            else:
                time.sleep(0.01)

        else:
            if counter == 0 or counter == 1:
                counter = counter + 1
            else:
                begin = True
                error_count = 0
                print("Color : ", color)
                colors0.append(color[0])
                colors1.append(color[1])
                color_prev0 = color[0]
                color_prev1 = color[1]
                counter = 0



color_to_bin = {'black' = '000', 'red': '001', 'green': '010', 'blue': '011', 'blue_cian': '100', 'magenta': '101', 'yellow': '110', 'white': '111'}

def checksum_checker(colors0, colors1):
    assert(len(colors1) == len(colors0))
    bin_ret = ""

    for i in range(len(colors1)):
        c0 = ""
        
        sub0 = ""
        
        for k in range(colors0[i]):
            sub0 = sub0 + color_to_bin[colors0[i][k]]
        sub0 = sub0[:-9]
        
        for i in range(sub0/8):
            c0 = chr(int(sub0[i*8:i*8+8], base=2)


        bin_ret = bin_ret + c0


    return bin_ret



mot = checksum_checker(colors0,colors1)

print('Mot transmis: ')
print(mot)
print("--- %s seconds ---" % (time.time() - start_time))




























ter = ""

tr_ter = {'red': '0', 'green': '1', 'blue': '2'}

colors0 = np.array(colors0)

colors0 = colors0.flatten()

for i in range(len(colors0)):
    ter = ter + tr_ter[colors0[i]]

#ter = ter[:-8]

ter = ter.rstrip('2')

#print(ter)

if(len(ter)%2 == 1):
    ter = ter + '2'

print(ter)


mot = ter_to_ascii(ter)

print('Mot transmis: ')
print(mot)
print("--- %s seconds ---" % (time.time() - start_time))

# In[23]:




# In[ ]:



# In[ ]:
