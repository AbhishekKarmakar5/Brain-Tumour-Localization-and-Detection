import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mbox
import os
import imageio
import PIL.Image, PIL.ImageTk
import cv2
from tkinter import *
from PIL import Image,ImageTk

from matplotlib import pyplot as plt  
import numpy as np 
plt.style.use("dark_background")
 
root= tk.Tk()
root.configure(bg='grey')
root.title("Brain Processing Output...........")

#--------------------------------------------------------------IMP to use
#root.attributes('-fullscreen', True)

cv_img = cv2.imread("eegDo.png")
height, width, no_channels = cv_img.shape
  
canvas1 = tk.Canvas(root, bg="cyan2",width = 10 + width+10, height = 10 + height+10)
canvas1.pack()

photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
canvas1.create_image(10, 10, image=photo, anchor=tk.NW)

label1 = tk.Label(root, text='Tumour Visulization',bg='black',fg='yellow')
label1.config(font=('Arial', 20, 'bold'))
canvas1.create_window(width/2, 30, window=label1)

label2 = tk.Label(root, text=' File Name: ')
label2.config(font=('Arial', 10,'bold'))
canvas1.create_window(width/2 - 50, 130, window=label2) 

entry1 = tk.Entry (root)
canvas1.create_window(width/2 + 60, 130, window=entry1) 

label4 = tk.Label(root, text= "2D Brain Visulization",bg='black',fg='yellow')
label4.config(font=('Arial', 10,'bold'))
canvas1.create_window(width - 100, height - 20, window=label4)
 
def open_file(): 
    global filename
    entry1.delete(0,"end")
    filename = fd.askopenfilename()
    entry1.insert(0,os.path.basename(filename))

def thresholding():
    
    import imutils
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # find contours in thresholded image, then grab the largest
    # one
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    #Cropping the image
    x,y,w,h = cv2.boundingRect(c)
    crop = image[y:y+h, x:x+w]
    cv2.imwrite('Image.png', crop)

    # determine the most extreme points along the contour
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])

    # draw the outline of the object, then draw each of the
    # extreme points, where the left-most is red, right-most
    # is green, top-most is blue, and bottom-most is teal

    cv2.drawContours(image, [c], -1, (0, 255, 255), 2)   # yellow
    cv2.circle(image, extLeft, 8, (0, 0, 255), -1)  # red
    cv2.circle(image, extRight, 8, (0, 255, 0), -1) #green
    cv2.circle(image, extTop, 8, (255, 0, 0), -1)   # blue
    cv2.circle(image, extBot, 8, (255, 255, 0), -1) # teal


    image1 = cv2.imread('Image.png')  
    img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY) 
      
    ret, thresh1 = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY) 
    ret, thresh2 = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV) 
    ret, thresh3 = cv2.threshold(img, 150, 255, cv2.THRESH_TRUNC) 
    ret, thresh4 = cv2.threshold(img, 150, 255, cv2.THRESH_TOZERO) 
    ret, thresh5 = cv2.threshold(img, 150, 255, cv2.THRESH_TOZERO_INV) 

    titles = ['Original','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
    images = [image1, thresh1, thresh2, thresh3, thresh4, thresh5]

    cv2.imshow("Brain Area", image)


    #----------------------------------------------------------------------------------------------------------
    cnts1 = cv2.findContours(thresh1.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts1 = imutils.grab_contours(cnts1)
    c1 = max(cnts1, key=cv2.contourArea)

    cv2.drawContours(image1, [c1], -1, (255, 0, 0), 2)
    #----------------------------------------------------------------------------------------------------------

    plt.suptitle("Different thresholdings")
    for i in range(6):
        plt.subplot(2,3,i+1),plt.imshow(images[i])
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.show()

    cv2.waitKey(0)  
    

def brainly():

    def ShowImage(title,img,ctype):
      plt.figure(figsize=(10, 10))
      if ctype=='bgr':
        b,g,r = cv2.split(img)       # get b,g,r
        rgb_img = cv2.merge([r,g,b])     # switch it to rgb
        plt.imshow(rgb_img)
      elif ctype=='hsv':
        rgb = cv2.cvtColor(img,cv2.COLOR_HSV2RGB)
        plt.imshow(rgb)
      elif ctype=='gray':
        plt.imshow(img,cmap='gray')
      elif ctype=='rgb':
        plt.imshow(img)
      else:
        raise Exception("Unknown colour type")
      plt.axis('off')
      plt.title(title)
      plt.show()

    img = cv2.imread(filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #ShowImage('Brain MRI',gray,'gray')

    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_OTSU)
    #ShowImage('Thresholding image',thresh,'gray')

    ret, markers = cv2.connectedComponents(thresh)

    #Get the area taken by each component. Ignore label 0 since this is the background.
    marker_area = [np.sum(markers==m) for m in range(np.max(markers)) if m!=0] 
    #Get label of largest component by area
    largest_component = np.argmax(marker_area)+1 #Add 1 since we dropped zero above                        
    #Get pixels which correspond to the brain
    brain_mask = markers==largest_component

    brain_out = img.copy()
    #In a copy of the original image, clear those pixels that don't correspond to the brain
    brain_out[brain_mask==False] = (0,0,0)

    #---------------------------------------------CORE BRAIN OUTPUT--------------------------------------------------------------

    im1 = cv2.cvtColor(brain_out,cv2.COLOR_HSV2RGB)
    ShowImage('Segmented image',im1,'gray') 

    #----------------------------------------------     3D OUTPUT     ----------------------------------------------------------


def viewPrint():
    from matplotlib.pyplot import imread 
    from mpl_toolkits.mplot3d import Axes3D 
    import scipy.ndimage as ndimage 

    def ShowImage(title,img,ctype):
      plt.figure(figsize=(10, 10))
      if ctype=='bgr':
        b,g,r = cv2.split(img)       # get b,g,r
        rgb_img = cv2.merge([r,g,b])     # switch it to rgb
        plt.imshow(rgb_img)
      elif ctype=='hsv':
        rgb = cv2.cvtColor(img,cv2.COLOR_HSV2RGB)
        plt.imshow(rgb)
      elif ctype=='gray':
        plt.imshow(img,cmap='gray')
      elif ctype=='rgb':
        plt.imshow(img)
      else:
        raise Exception("Unknown colour type")
      plt.axis('off')
      plt.title(title)
      plt.show()

    img = cv2.imread(filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_OTSU)
    ret, markers = cv2.connectedComponents(thresh)

    marker_area = [np.sum(markers==m) for m in range(np.max(markers)) if m!=0] 
    largest_component = np.argmax(marker_area)+1
    brain_mask = markers==largest_component
    brain_out = img.copy()
    brain_out[brain_mask==False] = (0,0,0)
    im1 = cv2.cvtColor(brain_out,cv2.COLOR_HSV2RGB)
    #-------------------------------------------------------------brainly to get the brain_out-----------------------    

    mat = im1
    mat = mat[:,:,0] # get the first channel 
    rows, cols = mat.shape 
    xv, yv = np.meshgrid(range(cols), range(rows)[::-1]) 
         
    blurred = ndimage.gaussian_filter(mat, sigma=(5, 5), order=0) 
    fig = plt.figure(figsize=(6,6)) 
        
    ax = fig.add_subplot(221) 
    ax.imshow(mat, cmap='viridis') 
         
    ax = fig.add_subplot(222, projection='3d') 
    ax.elev= 75 
    ax.plot_surface(xv, yv, mat) 

    ax = fig.add_subplot(223) 
    ax.imshow(blurred, cmap='magma') 
         
    ax = fig.add_subplot(224, projection='3d') 
    ax.elev= 75 
    ax.plot_surface(xv, yv, blurred) 
    plt.suptitle("NOTE: Tumour Region has a greater Altitude compared to neighbours where as in case of Non-Tumour, all the regions has more or like same altitude!")
    plt.show()        


def clustering():
	from matplotlib.pyplot import imread
	from mpl_toolkits.mplot3d import Axes3D
	image = cv2.imread(filename)
	# convert to RGB
	image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)

	# reshape the image to a 2D array of pixels and 3 color values (RGB)
	pixel_values = image.reshape((-1, 3))
	# convert to float
	pixel_values = np.float32(pixel_values)

	# define stopping criteria
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

	# number of clusters (K)
	k = 3
	_, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

	# convert back to 8 bit values
	centers = np.uint8(centers)

	# flatten the labels array
	labels = labels.flatten()

	# convert all pixels to the color of the centroids
	segmented_image = centers[labels.flatten()]

	# reshape back to the original image dimension
	segmented_image = segmented_image.reshape(image.shape)
	# show the image


	# disable only the cluster number 2 (turn the pixel into white)
	masked_image = np.copy(image)
	# convert to the shape of a vector of pixel values
	masked_image = masked_image.reshape((-1, 3))
	# color (i.e cluster) to disable
	cluster = 0
	masked_image[labels == cluster] = [255, 255, 255]
	# convert back to original shape
	masked_image = masked_image.reshape(image.shape)
	# show the image


	#----------------------------------------------------------difference-------------------------------
	diff = cv2.subtract(segmented_image, masked_image)
	mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

	th = 0
	imask =  mask>th

	canvas = np.zeros_like(masked_image, np.uint8)
	canvas[imask] = masked_image[imask]
	#----------------------------------------------------------diff 2-------------------------------------------

	titles = ['K-Means Clustering','Disable one cluster','Difference']
	images = [segmented_image,masked_image,canvas]  

	for i in range(3):
		plt.subplot(1,3,i+1),plt.imshow(images[i])
		plt.title(titles[i])
		plt.xticks([]),plt.yticks([])
		plt.autoscale(tight=True)
	plt.show()


def Colour():
    from display import colorSel
    img = cv2.imread(filename)
    img = cv2.resize(img,(300,350))
    img = cv2.cvtColor(img,cv2.COLOR_HSV2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    

    cSel = colorSel(img, hLow=0, sLow=0, vLow=0, hHigh=255, sHigh=255, vHigh=255)    

def YesorNo():
    import tensorflow as tf
    from keras.preprocessing import image

    SelectedModel = tf.keras.models.load_model("modelCNN.tf",compile=True)
    
    test_image = image.load_img(filename, target_size = (64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)

    result = SelectedModel.predict(test_image)
    #training_set.class_indices
    if result[0][0] == 1:
        prediction = 'yes'
    else:
        prediction = 'no'
    
    if(prediction=='yes'):
        mbox.showerror("Found","There is a tumour region present in the brain")
    else:
        mbox.showinfo("Successful","No Tumour Found")
    



button0 = tk.Button (root, text=' Select File ',command=open_file, bg='cornsilk2', font=('Arial', 11, 'bold')) 
canvas1.create_window(width/2, 90, window=button0)

thresh_icon = ImageTk.PhotoImage(file = "thresh.png")     
button1 = tk.Button (root, image=thresh_icon,command=thresholding, bg='yellow',font=('Arial', 11, 'bold')) 
canvas1.create_window(width/2 - 250, 240, window=button1)

brain_icon = ImageTk.PhotoImage(file = "brainly.png") 
button2 = tk.Button (root, image=brain_icon, command=brainly, bg='yellow',font=('Arial', 11, 'bold'))
canvas1.create_window(width/2 - 150, 240, window=button2)

brainTumour_icon = ImageTk.PhotoImage(file = "findt.png") 
button3 = tk.Button (root, image=brainTumour_icon, command=YesorNo, bg='yellow',font=('Arial', 11, 'bold'))
canvas1.create_window(width/2 - 50, 240, window=button3)

view3d_icon = ImageTk.PhotoImage(file = "see3D.png") 
button4 = tk.Button (root, image=view3d_icon, command=viewPrint, bg='yellow',font=('Arial', 11, 'bold'))
canvas1.create_window(width/2 + 50, 240, window=button4)

cluster_icon = ImageTk.PhotoImage(file = "cluster.png") 
button5 = tk.Button (root, image=cluster_icon, command=clustering, bg='yellow',font=('Arial', 11, 'bold'))
canvas1.create_window(width/2 + 150, 240, window=button5)

hue_icon = ImageTk.PhotoImage(file = "hsv.png")     
button1_2 = tk.Button (root, image=hue_icon,command=Colour, bg='yellow',font=('Arial', 11, 'bold')) 
canvas1.create_window(width/2 + 250, 240, window=button1_2)

button8 = tk.Button (root, text='Exit Application', command=root.destroy, bg='LightCyan2', font=('Arial', 11, 'bold'))
canvas1.create_window(width/2, 380, window=button8)

root.geometry("1350x700+0+0")
root.mainloop()
