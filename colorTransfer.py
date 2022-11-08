import PIL 
import math
import numpy as np


matrix1 = np.array([[0.3811,0.5783,0.0402],
           [0.1967,0.7244,0.0782],
           [0.0241,0.1288,0.8444]])

matrix2 = np.array([[1/math.sqrt(3),0,0],
          [0,1/math.sqrt(6),0],
          [0,0,1/math.sqrt(2)]])

matrix3 = np.array([[1,1,1],
           [1,1,-2],
           [1,-1,0]])

matrix4 = np.array([[1/math.sqrt(3),0,0],
           [0,1/math.sqrt(6),0],
           [0,0,1/math.sqrt(2)]])

matrix5 = np.array([[1,1,1],
           [1,1,-1],
           [1,-2,0]])


matrix6 = np.array([[math.sqrt(3)/3,0,0],
          [0,math.sqrt(6)/6,0],
          [0,0,math.sqrt(2)/2]])


matrix7 = np.array([[4.4679,-3.5873,0.1193],
           [-1.2186,2.3809,-0.1624], 
           [0.0497,-0.2439,1.2045]])



def preprocessing (image):
    image = np.array(image)
    image = image.transpose((2,0,1)).reshape(3,-1)
    image=np.matmul(matrix1,image)
    image=np.log(image)
    image = np.matmul(matrix3,image)
    image = np.matmul(matrix2,image)
    return image


def pixelValueChecker(pixelValue):
    if (pixelValue > 255) :
      pixelValue = 255
    elif (pixelValue < 0 ) :
      pixelValue = 0
    elif(math.isnan(pixelValue)):
      pixelValue = 0  
    return pixelValue
      


def convertLABSpace(source,sourceWidth,sourceHeight,target,targetWidth,targetHeight):
    main_source = source
    pixels = main_source.load()
    source = preprocessing(source)
    target = preprocessing(target)
    for i in range(3):
        source[i] = (source[i] - np.mean(source[i]))
        source[i] = (np.nanvar(np.array(target[i])) / np.nanvar(np.array(source[i]))) * source[i]
        source[i] =   (source[i] + np.nanmean(target[i]))
    source = np.matmul(matrix6,source)
    source = np.matmul(matrix5,source)
    for i in range(3):
        source[i] = (source[i] * 10**source[i])
    source = np.matmul(matrix7,source)
    source = source/500  # normalizing for get more succesful result
    
    k=0
    for i in range(sourceHeight):
      for j in range(sourceWidth):
          coordinates = x,y = (j,i)
          red = source[0][k] 
          red = pixelValueChecker(red)
          green = source[1][k] 
          green = pixelValueChecker(green)
          blue = source[2][k] 
          blue = pixelValueChecker(blue)
          pixels[coordinates] = (int(red),int(green),int(blue))
          k+=1    
    main_source.save("result.jpg")
    

def colorTransfer(source,target):
    sourceWidth, sourceHeight = source.size
    targetWidth, targetHeight = target.size
    convertLABSpace(source, sourceWidth, sourceHeight,target,targetWidth,targetHeight)
    
    
sourceImageWithReadingPIL = PIL.Image.open("scotland_house.jpg") 
targetImageWithReadingPIL = PIL.Image.open("ocean_day.jpg")  
colorTransfer(sourceImageWithReadingPIL,targetImageWithReadingPIL)   
    