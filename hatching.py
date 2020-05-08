import cv2
from numpy import *
import random

#######################################################################
def perp( a ) :
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return 
def seg_intersect(a1,a2, b1,b2) :
    flag=1
    if a1[1]>a2[1]:
        if b1[1]>a1[1] or b1[1]<a2[1]:
            flag=0 #no intersection
    if a1[1]<=a2[1]:
        if b1[1]<a1[1] or b1[1]>a2[1]:
            flag=0 #no intersection

        
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = dot( dap, db)
    num = dot( dap, dp )
    if denom.astype(float)==0:
        temp=0.000001
    else:
        temp=denom.astype(float)
    return flag, (num / temp)*db + b1

#########################################################################

def rotateImage(image, angle):
  image_center = tuple(array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_NEAREST )
  return result


#########################################################################

def hatching( input_img,line_space,line_angle ) :
    inters_array=[]
    inters_array_sorted_list=[]
    global blank_image
    height, width= input_img.shape
    temp_image = zeros((height, width,3), uint8)
    temp_image[:]=(255,255,255)
    
    hatch_img=rotateImage(input_img, line_angle)
    contours,hierarchy = cv2.findContours(hatch_img, 1, 2)
    

    print len(contours)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>20:

            polygon= cv2.approxPolyDP(cnt,3,True)
            
        #for loop in polygon array and drawing
        #for polygon in polygon_sel:    
            point_last=polygon[len(polygon)-1]
            
            if len(polygon)>3:
                    for points in polygon:        
                        cv2.line(temp_image, (int(points[0][0]), int(points[0][1])), \
                                 (int(point_last[0][0]), int(point_last[0][1])), (0,0,0), 1)
                        point_last=points
            
    #create and draw scan line 
    for scan_y in range(0,height/line_space):    
        h1 = array( [0.0, scan_y*line_space] )
        h2 = array( [width, scan_y*line_space] )   
        
        #for loop in polygon array and find intersections
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area>20:
                polygon= cv2.approxPolyDP(cnt,3,True)    
   
                point_last=polygon[len(polygon)-1]
                for points in polygon:        
                    #cv2.line(blank_image, (int(points[0]), int(points[1])), (int(point_last[0]), int(point_last[1])), (0,0,225), 2)
                    
                    #p1_x = (points[0][0])+random.uniform(-1.5, 1.5)
                    #p1_y = (points[0][1])+random.uniform(-1.5, 1.5)
                    #p2_x = (point_last[0][0])+random.uniform(-1.5, 1.5)
                    #p2_y = (point_last[0][1])+random.uniform(-1.5, 1.5)
                    
                    #h1_x = (h1[0])+random.uniform(-1.5, 1.5)
                    #h1_y = (h1[1])+random.uniform(-1.5, 1.5)
                    #h2_x = (h2[0])+random.uniform(-1.5, 1.5)
                    #h2_y = (h2[1])+random.uniform(-1.5, 1.5)
                    
                    
                    p1_x = (points[0][0])
                    p1_y = (points[0][1])
                    p2_x = (point_last[0][0])
                    p2_y = (point_last[0][1])
                    
                    h1_x = (h1[0])
                    h1_y = (h1[1])
                    h2_x = (h2[0])
                    h2_y = (h2[1])
                    
                    if p1_y!=p2_y:
                                                
                            ex, inters_point= seg_intersect(array([p1_x, p1_y]), array([p2_x, p2_y]),\
                                                            array([h1_x,h1_y]),array([h2_x,h2_y]))
                                                   
                            if ex==1:# add to array if intersect
                                inters_array.append(inters_point)
                                       
                    point_last=points
                
        inters_array_sorted=sorted(inters_array,key=lambda l:l[0])      
        inters_num=len(inters_array)
        count=0
        
        inters_array_sorted_list=list(inters_array_sorted)
        
        #print "before",inters_num  
         
        if inters_num%2==1:
                #print "eme....",inters_array_sorted_list[3][0]
                offset=0
                for p in range(1,inters_num):
                        if abs(inters_array_sorted_list[p-offset][0]-inters_array_sorted_list[p-1-offset][0])<0.00001:  
                                #print p
                                #print "before inters", inters_array_sorted_list
                                #print "pop", inters_array_sorted_list[p-offset]                
                                inters_array_sorted_list.pop(p-1-offset)
                                #print "after inters", inters_array_sorted_list   ######################
                                offset=offset+1
                                #break
                                
            #print "list",inters_array_sorted_list
                                
        inters_num=len(inters_array_sorted_list)
        #print "after",inters_num    
        #count=0
        if inters_num>1 and inters_num%2==0:
            #print inters_array_sorted
            #hatching_point_last=inters_array_sorted[len(inters_array_sorted)-1]
            while count < inters_num-1:
                if count%2==0:
                                        line_color=(0,0,0)
                else:
                    line_color=(255,255,255)
                cv2.line(temp_image, (int(inters_array_sorted_list[count][0]), \
                                       int(inters_array_sorted_list[count][1])), \
                                      (int(inters_array_sorted_list[count+1][0]), \
                                       int(inters_array_sorted_list[count+1][1])), line_color, 1)
                
                #print count    
                count=count+1
            
            #print inters_array_sorted[0]

        #elif inters_num>1 and inters_num%2==1:# some points are at the same position  ##########################
            #print inters_array_sorted
            
        #print inters_num,"......................................"    
        inters_array=[]
        inters_array_sorted_list=[] 
        
    temp_image=rotateImage(temp_image, -line_angle)
    blank_image = cv2.multiply(blank_image, temp_image)


    
##########################################################################
inters_xpos_array=[] 
#inters_array=[]

img = cv2.imread('test.jpg',0)

#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.equalizeHist(img)

cv2.imshow("img",img)

#img_rot=rotateImage(img, 45)
#cv2.imshow("img",img_rot)

##img_edge = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
##            cv2.THRESH_BINARY,11,2)
##cv2.imshow("edge",img_edge)

blur = cv2.blur(img,(3,3))
height, width= img.shape

blur = cv2.bitwise_not(blur)




blank_image = zeros((height,width,3), uint8)
blank_image[:]=(255,255,255)



#ret,thresh = cv2.threshold(blur,100,255,0)
#hatching( thresh,2,45)

##############################################
ret,thresh = cv2.threshold(blur,5,255,0)
hatching( thresh,1500,0)

ret,thresh = cv2.threshold(blur,35,255,0)
#cv2.imshow("bin",thresh)
hatching( thresh,6,13)

#ret,thresh = cv2.threshold(blur,45,255,0)
#cv2.imshow("bin",thresh)
#hatching( thresh,6,23 )

ret,thresh = cv2.threshold(blur,65,255,0)
#cv2.imshow("bin",thresh)
hatching( thresh,5,20)

ret,thresh = cv2.threshold(blur,100,255,0)
#cv2.imshow("bin1",thresh)
hatching( thresh,4,-20 )
#blank_image=rotateImage(blank_image, 25)

ret,thresh = cv2.threshold(blur,130,255,0)
#cv2.imshow("bin2",thresh)
hatching( thresh,4,-15 )
#blank_image=rotateImage(blank_image, 35)

ret,thresh = cv2.threshold(blur,160,255,0)
#cv2.imshow("bin2",thresh)
hatching( thresh,3,-5 )
#blank_image=rotateImage(blank_image, 35)

ret,thresh = cv2.threshold(blur,200,255,0)
#cv2.imshow("bin2",thresh)
hatching( thresh,2,8)

ret,thresh = cv2.threshold(blur,220,255,0)
#cv2.imshow("bin2",thresh)
hatching( thresh,2,-35)

####################################################
##blank_image=cv2.multiply(blank_image, img_edge )

cv2.imshow("poly",blank_image)
cv2.waitKey(0)
cv2.imwrite("hatching.jpg", blank_image)
