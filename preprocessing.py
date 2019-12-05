from PIL import ImageFilter
from PIL import Image
import numpy


def prepare_image_rubbo(im):
    return clean_image(black_and_white_image_rubbo(im))


def black_and_white_image_rubbo(im):
    im = im.convert('L')
    arr = numpy.asarray(im)
    arr = arr - arr.mean() *0.8 + 128
    return Image.fromarray(arr).convert('1', dither=Image.NONE)


def verify_null_image(im):
    im=prepare_image_rubbo(im)
    arr = numpy.asarray(im)
    if numpy.mean(arr)<0.99:
        return True
    return False
   
    
def black_and_white_image(im):
    im = im.convert('L')
    arr = numpy.asarray(im)
    arr = arr - arr.mean() *0.9 + 128
    return Image.fromarray(arr).convert('1', dither=Image.NONE)


def clean_image(im):
    im = im.convert('L').filter(ImageFilter.BoxBlur(1)).convert('1', dither=Image.NONE)
    return im


def invert_colors(im):
    arr = numpy.asarray(im).astype("int")
    arr = ((1-arr)*255).astype("uint8")
    return Image.fromarray(arr)


def prepare_image(im):
    return clean_image(black_and_white_image(im))


def get_edges(im1):
    im=identify_rectangles(im1)
    pixelMap = im.load()
    rectangles=[]
    already_tested_pixels=[]
    
    for l in range(im.width):
        for m in range(im.height):
            a=pixelMap[l,m]
            if (not [l,m] in already_tested_pixels) and  a == 255:
 
                try:
                    height=0
                    width=0
                    lower_pixel=a
                    right_pixel=a
                    while lower_pixel==255:
                        lower_pixel=0
                        height=height+1
                        lower_pixel=pixelMap[l, m+height]
        
                    while right_pixel==255:
                        right_pixel=0
                        width=width+1
                        right_pixel=pixelMap[l+width,m]
                    rectangle={"height": height, "width": width, "upper_left": [l, m]}
                    rectangle=[[l, m], width, height]
                    rectangles.append(rectangle)
                    #clean image, delete pixels that alrady are in rectangles
                    for a in range(l, l+width):
                        for b in range(m, m+height):
                            c=[a, b]
                            already_tested_pixels.append(c)                           
                except:
                    pass
    
    good_rectangles=[]
    for i in range(len(rectangles)-1):
    
        rec=rectangles[i]
        rec2=rectangles[i+1]
        if rec2[0][1]==rec[0][1]+1:
            pass
        else:
            good_rectangles.append(rec)
    
    return good_rectangles


def identify_words(im):
    im=prepare_image(im)
    im=invert_colors(im)
    k=2
    im.resize((1200, 1600),Image.NEAREST)
    im=im.resize((int(im.width//k) , int(im.height//k)), Image.NEAREST)

    for i in range(2):
        im=im.resize((int(im.width//k) , int(im.height//k)), Image.NEAREST)
        pixelMap = im.load()
        img = Image.new(im.mode, im.size)
        pixelsNew = img.load()
        
        for l in range(im.width):
            for m in range(im.height):
                a=pixelMap[l,m]
                
                if a == 0:
                    try:
                        a=1
                        left_pix=pixelMap[l-a,m]
                        right_pix=pixelMap[l+a,m]
                        upper_pix=pixelMap[l,m+a]
                        lower_pix=pixelMap[l,m-a]
                        left_left_pix=pixelMap[l-2*a,m]
                        sum1=left_pix+upper_pix
                        sum2=left_pix+lower_pix
                        sum3=right_pix+lower_pix
                        sum4=right_pix+upper_pix
                        sum5=right_pix+left_pix
                        sum6=right_pix+left_left_pix
                        if sum1>=510 or sum2>=510 or sum3>=510 or sum4>=510 or sum5>=510 or sum6>=5100 :
                        
                            pixelsNew[l,m] = 255
                        
                        else:
                            pixelsNew[l,m] = 0
                    except:
                        pixelsNew[l,m] = 0
                else:
                    pixelsNew[l,m] = 255
        im=img
    return im
    
    
def identify_rectangles(im):
    im=identify_words(im)
    for i in range(10):
    
        pixelMap = im.load()
        img = Image.new(im.mode, im.size)
        pixelsNew = img.load()
        
        for l in range(im.width):
            for m in range(im.height):
                a=pixelMap[l,m]
                
                if a == 0:
                    try:
                        a=1
                        left_pix=pixelMap[l-a,m]
                        right_pix=pixelMap[l+a,m]
                        upper_pix=pixelMap[l,m+a]
                        lower_pix=pixelMap[l,m-a]
                        left_left_pix=pixelMap[l-2*a,m]
                        sum1=left_pix+upper_pix
                        sum2=left_pix+lower_pix
                        sum3=right_pix+lower_pix
                        sum4=right_pix+upper_pix
                        sum5=right_pix+left_pix
                        sum6=right_pix+left_left_pix
                        if sum1>=510 or sum2>=510 or sum3>=510 or sum4>=510 or sum5>=510 or sum6>=5100 :
                        
                            pixelsNew[l,m] = 255
                        
                        else:
                            pixelsNew[l,m] = 0
                    except:
                        pixelsNew[l,m] = 0
                else:
                    pixelsNew[l,m] = 255
        
        im=img
    return im


def slice_into_words(im):
    edges = get_edges(im)
    cropped_image= identify_rectangles(im)
    k_height=(im.height/cropped_image.height)
    k_width=(im.width/cropped_image.width)
    words=[]
    coordinates=[]
    for i in edges:
        i[0][0]=int((i[0][0]-1.5)*k_width)
        i[0][1]=int((i[0][1]-1)*k_height)

        i[1]=int((i[1]+3)*k_width)

        i[2]=int((i[2]+2)*k_height)
    for a in range(len(edges)):
        i=edges[a]
        if i[0][0]<0:
            i[0][0]=0

        if i[0][1]<0:
            i[0][1]=0

        if i[0][0]+i[1]>im.width:
            right_crop=im.width
        else:
            right_crop=i[0][0]+i[1]

        if i[0][1]+i[2]>im.height:
            lower_crop=im.height
        else:
            lower_crop=i[0][1]+i[2]
        img=im.crop([i[0][0], i[0][1], right_crop, lower_crop])
        coordinates.append([i[0][0], i[0][1], right_crop, lower_crop])

        words.append(img)
    return [words,coordinates]

def find_array(im):
    v=slice_into_words(im)
    words, coordinates =v[0],v[1]
    
    only_real=[]
    for z in range(len(words)):
        img=words[z]
        if verify_null_image(img)==True:
            only_real.append(coordinates[z])
    return only_real
    
    
def mean_color(im):
    arr = numpy.asarray(im)
    meanR = 0
    meanG = 0
    meanB = 0
    arrayformean = arr/(arr.shape[0]*arr.shape[1])
    
    for i in range(arr.shape[0]):
        for j  in range(arr.shape[1]):
            meanR += arrayformean[i][j][0]
            meanG += arrayformean[i][j][1]
            meanB += arrayformean[i][j][2]
    meanR = int(meanR)
    meanG = int(meanG)
    meanB = int(meanB)
    meanIm = Image.new("RGB", (im.width, im.height), color=(meanR, meanG, meanB))

    return meanIm

def subtract_images(im, im2):
    if im.width==im2.width and im.height==im2.height:
        copy = numpy.asarray(im)
        array_im2 = numpy.asarray(im2)
        array_im = copy.copy()
        for i in range(array_im.shape[0]):
            for j in range(array_im.shape[1]):
                for c in range(array_im.shape[2]):
                    array_im[i][j][c] = max(array_im[i][j][c], array_im2[i][j][c])-min(array_im[i][j][c], array_im2[i][j][c])
        sub = Image.fromarray(array_im)
        return sub
    
def find_holds(im):
    arr_im = numpy.asarray(im)
    im2 = mean_color(im)
    sub = subtract_images(im, im2)
    arr_sub = numpy.asarray(sub)
    bouldermap_arr = numpy.array([[[]]])
    bouldermap_arr.resize(arr_im.shape[0], arr_im.shape[1], 3)
    bouldermap_arr += 255
    for i in range(arr_im.shape[0]):
        for j in range(arr_im.shape[1]):
            if arr_sub[i][j][0]>50 or arr_sub[i][j][1]>50 or arr_sub[i][j][2]>50:
                bouldermap_arr[i][j] *= 0
    bouldermap = Image.fromarray(bouldermap_arr.astype("uint8"))
    return find_array(bouldermap)

         
    