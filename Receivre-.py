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

        if (peri > 100 and peri < 400):# and len(approx_tmp) == 4):
            approx.append(approx_tmp)
            print(approx)

            cv2.drawContours(copieImg, [approx_tmp], -1, (col, 255-col, col), 4)
            cv2.imwrite('img_CV2_90.jpg', copieImg)

            #col = col + 50

    #plt.show()
    # print("approx ",approx)
    # print("len approx ",len(approx))
    return approx

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
    config = 0
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


    if((max_x - min_x)/(max_y - min_y)) < 1:
        config = 2
        mid_y = int( min_y + (max_y - min_y)/2)
        bord = [[min_x, max_x, min_y, mid_y],[min_x, max_x, mid_y, max_y]]


    else:
        config = 1
        bord = [min_x, max_x, min_y, max_y]


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
    bord, sucess = bords(approx)


    print(approx)

    print("les 4 bords de l'ecrans sont : ", bord)
    #print("la configuration est la n°", config)
    print("--- %s seconds ---" % (time.time() - start_time))

    return bord,sucess

# Part 2: Color detection

def color_detection (bord, path):
    if(type(path) == str):
        img = cv2.imread(path)
        path = img
    elif(type(path) == None):
        return 'end'

    img = resize(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # bords = [min_x, max_x, min_y, max_y]
    #cv2.imwrite('img1_CV2_90_8.jpg', img)

    im1 = []
    im2 = []
    colors1 = []
    colors2 = []
    # ========================= A Verifier ======================
    #(min_y, max_y, min_x, max_x) = bord
    #(min_x, max_x, min_y, max_y) = bord
    #mid_x = int( min_x + (max_x - min_x)/2)
    #mid_y = int( min_y + (max_y - min_y)/2)
    #print("mid_x",mid_x)
    #print("mid_y",mid_y)

    #print("min x : ", min_x, " max_x : ", max_x, " min y: ", min_y, " max y: ", max_y)
    #if(config == 2):
    #    #Image dans la hauteur - ie
    #    im1 = img[min_x: max_x, min_y: mid_y ]
    #    im2 = img[min_x: max_x , mid_y:max_y ]
    #elif(config == 1):
    #    #Image dans la Longeur - ie
    #    im1 = img[min_x : mid_x , min_y:max_y]
    #    im2 = img[mid_x : max_x, min_y:max_y]
    #elif(config == 3):
    #    #Image dans  - ie
    #    im1 = img[min_x : mid_x, mid_y : max_y]
    #    im2 = img[mid_x : max_x, min_y : mid_y]
    #elif(config == 4):
        #Image dans  - ie
    #    im1 = img[min_x : mid_x , min_y : mid_y]
    #    im2 = img[mid_x : max_x, mid_y : max_y]

    (bord1, bord2) = bord
    #print("bord 1 : ", bord1)
    #print("bord 2 : ", bord2)
    #print("diff bord 1",bord1[1]-bord1[0],bord1[3]-bord1[2])
    #print("diff bord 2", bord2[1]-bord2[0],bord2[3]-bord2[2])



    im1 = img[bord1[2]:bord1[3],:]
    im2 = img[bord2[2]:bord2[3],:]

    im1 = im1[:,bord1[0]:bord1[1]]
    im2 = im2[:,bord2[0]:bord2[1]]

    #print(im1.shape[0], im1.shape[1])
    #print(im2.shape[0], im2.shape[1])

    #cv2.imwrite('img1_CV2_90.jpg', im1)
    #cv2.imwrite('img2_CV2_90.jpg', im2)


    colors1 = cutting(im1, 3, 3)
    colors2 = cutting(im2, 3, 3)
    # if(colors1 == colors2):
    #     return colors1, colors2
    # else:
    #     print("Error 1 : ", colors1)
    #     print("Error 2 : ", colors2)
    #     #plt.imshow(im1)
    #     #plt.imshow(im2)
    #     #plt.show()
    #     #time.sleep(5)
    #     #plt.close()
    #
    #     #plt.imshow(im2)
    #     #plt.show()
    #     return colors1, colors2

    return [colors1, colors2]

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

#This function
def distance(c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

# this function take a point and find its color
def witch_color(point):
    colors = list(rgb_dictionary.keys())
    closest_colors = sorted(colors, key=lambda color: distance(color, point))
    closest_color = closest_colors[0]
    code = rgb_dictionary[closest_color]
    return code

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



transl = {'00': '000', '01': '001', '02': '010', '10': '011', '11': '100', '12': '101', '20': '110', '21': '111', '22': '111'} # 22 should not happen

def ter_to_bin(s):
    str_bin = ""

    for i in range(0, int(len(s)), 2):
        str_bin = str_bin + transl[s[i:i+2]]

    return str_bin

# https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa
def bin_to_ascii(s):

    rem_mod_8 = len(s)%8;
    s2 = "";

    if (rem_mod_8 == 0):
        #print(0)
        s2 = s
    elif (rem_mod_8 == 1):
        #print(1)
        s2 = s[0:len(s)-1]
    elif (rem_mod_8 == 2):
        #print(2)
        s2 = s[0:len(s)-2]

    #print(len(s2))

    s2 = int((s2), 2)

    return s2.to_bytes((s2.bit_length() + 7) // 8, 'big').decode()


def ter_to_ascii(s):
    return bin_to_ascii(ter_to_bin(s))



start_time = time.time()


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
    print("Camera not detected")

redD = 0
blueD = 0
#greenD = 1
#pinkD = 1
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
        #elif i == 1 and greenD == 0:
        #    print("GREEN")
        #    bord, screen_detected = detection(frame, i)
        #    print(bord)

        #    if screen_detected:
        #        greenD = 1
        elif i == 2 and blueD == 0:
            print("BLUE")
            bord_blue, screen_detected = detection(frame, i)
            if screen_detected:
                blueD = screen_detected
        #elif i == 3 and pinkD == 0:
        #   print("PINK")
        #  bord, screen_detected = detection(frame, i)
        #  if screen_detected:
        #      pinkD = 1

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
#print("detected colors : ",colors)
print("--- %s seconds ---" % (time.time() - start_time))

error_count = 0

begin = False

counter = 0

final_counter = 0;

while(True):
    time2 = time.time()
    ret, frame = cap.read()
    color = color_detection(bord, frame)
    #print("color: ",color)

    if ((color[0] == color_red or color[0] == color_blue or color[1] == color_red or color[1] == color_blue) and not begin):
        pass
    else:
        #print("final_counter ",final_counter)
        if (color[0] == color_prev0 and color[1] == color_prev1):
            final_counter = final_counter + 1
            if(final_counter > 100):
                print('----END----')
                break
            begin = True
            pass
        elif(color[0] == color_blue or color[1] == color_blue or (final_counter > 100)):
            print('----END----')
            break
        elif(color[0] != color[1]):
            final_counter = 0
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

                #if(error > 10):
                #image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                time.sleep(0.01)

            #plt.imshow(frame)
            #plt.show()
        else:
            final_counter = 0
            if counter == 0:
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
    #print(time.time() - time2)

#
#
# for i in range(len(colors0)):
#     ter = ter + tr_ter[colors0[i]]
#
# #ter = ter[:-8]
#
# ter = ter.rstrip('2')
#
# #print(ter)
#
# if(len(ter)%2 == 1):
#     ter = ter + '2'
#
# print(ter)

#mot = ter_to_ascii(ter)

tr_ter = {'red': '0', 'green': '1', 'blue': '2'}

def checksum_checker(colors0, colors1):
    assert(len(colors1) == len(colors0))
    bin_ret = ""

    for i in range(len(colors1)):
        c0 = ""
        c1 = ""

        for j in range(len(colors1[i])):
            c0 = c0 + tr_ter[colors0[i][j]]
            c1 = c1 + tr_ter[colors1[i][j]]

        bin_0 = ter_to_bin(c0[:-1])
        bin_1 = ter_to_bin(c1[:-1])
        bin_final = ""

        test_0_0 = (int(bin_0[0])+int(bin_0[1])+int(bin_0[2]))%2
        test_1_0 = (int(bin_0[3])+int(bin_0[4])+int(bin_0[5]))%2
        test_2_0 = (int(bin_0[6])+int(bin_0[7])+int(bin_0[8]))%2

        checksum_0_0 = bin_0[9]
        checksum_1_0 = bin_0[10]
        checksum_2_0 = bin_0[11]

        test_0_1 = (int(bin_1[0])+int(bin_1[1])+int(bin_1[2]))%2
        test_1_1 = (int(bin_1[3])+int(bin_1[4])+int(bin_1[5]))%2
        test_2_1 = (int(bin_1[6])+int(bin_1[7])+int(bin_1[8]))%2

        checksum_0_1 = bin_1[9]
        checksum_1_1 = bin_1[10]
        checksum_2_1 = bin_1[11]


        if(test_0_0 == checksum_0_0):
            bin_final = bin_final + bin_0[0:3]
        else:
            bin_final = bin_final + bin_1[0:3]

        if(test_1_0 == checksum_1_0):
            bin_final = bin_final + bin_0[3:6]
        else:
            bin_final = bin_final + bin_1[3:6]
        if(test_2_0 == checksum_2_0):
            bin_final = bin_final + bin_0[6:8]
        else:
            bin_final = bin_final + bin_1[6:8]

        bin_ret = bin_ret + bin_final


    return bin_to_ascii(bin_ret)


#colors0 = colors0[:-1]
#colors1 = colors1[:-1]
#colors0 = [['green', 'red', 'red', 'red', 'red', 'blue', 'red', 'green', 'red'], ['green', 'red', 'red', 'red', 'green', 'green', 'red', 'green', 'green']]
#colors1 = [['green', 'red', 'red', 'red', 'red', 'blue', 'red', 'green', 'red'], ['green', 'red', 'red', 'red', 'green', 'green', 'red', 'green', 'green']]
mot = checksum_checker(colors0,colors1)

print('Mot transmis: ')
print(mot)
print("--- %s seconds ---" % (time.time() - start_time))
