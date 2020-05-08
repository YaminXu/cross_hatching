
import cv2
from numpy import *



def perp( a ) :
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return 
def seg_intersect(a1,a2,b1,b2) :
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

blank_image = zeros((600,600,3), uint8)

inters_xpos_array=[] 
inters_array=[]
inters_array_sorted_list=[]

polygon1= array([[300.0, 40.0],[550.0, 530.0],[80.0, 550.0],[10.0, 300.0]])
polygon2= array([[300.0, 120.0],[320.0, 500.0],[200.0, 500.0],[80.0, 310.0]])
polygon3= array([[30.0, 120.0],[30.0, 500.0],[240.0, 50.0],[380.0, 230.0]])

polygon_sel=array([polygon1,polygon2,polygon3])

#for loop in polygon array and drawing
for polygon in polygon_sel:    
    point_last=polygon[len(polygon)-1]
    for points in polygon:        
        cv2.line(blank_image, (int(points[0]), int(points[1])), (int(point_last[0]), int(point_last[1])), (0,0,225), 2)
        point_last=points
        
#create and draw scan line 
for scan_y in range(0,150):    
    h1 = array( [0.0, scan_y*4] )
    h2 = array( [600.0, scan_y*4] )   
    #print scan_y
    cv2.line(blank_image, (int(h1[0]), int(h1[1])), (int(h2[0]), int(h2[1])), (100,100,100), 1)
        
    #for loop in polygon array and find intersections
    for polygon in polygon_sel:    
        point_last=polygon[len(polygon)-1]
        for points in polygon:        
            #cv2.line(blank_image, (int(points[0]), int(points[1])), (int(point_last[0]), int(point_last[1])), (0,0,225), 2)
            p1_x = int(points[0])
            p1_y = int(points[1])
            p2_x = int(point_last[0])
            p2_y = int(point_last[1])
            
            h1_x = int(h1[0])
            h1_y = int(h1[1])
            h2_x = int(h2[0])
            h2_y = int(h2[1])
            
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
    
    if inters_num%2==1:
        #print "eme....",inters_array_sorted_list[3][0]
        for p in range(1,inters_num):
            if abs(inters_array_sorted[p][0]-inters_array_sorted[p-1][0])<0.001:                
                inters_array_sorted_list.pop(p)
                
    #print "list",inters_array_sorted_list
                
    inters_num=len(inters_array_sorted_list)
    #print "ok",inters_num
        
    if inters_num>1: #and inters_num%2==0:
        #print "............................................"
        #print inters_array_sorted_list

        while count < inters_num-1:
            if count%2==0:
                line_color=(0,255,0)
            else:
                line_color=(100,100,100)

            cv2.line(blank_image, (int(inters_array_sorted_list[count][0]), \
                                   int(inters_array_sorted_list[count][1])), \
                                  (int(inters_array_sorted_list[count+1][0]), \
                                   int(inters_array_sorted_list[count+1][1])), line_color, 1)

            #print "ints: ", count    
            count=count+1
            
    print "line: ", scan_y, "ints: ", inters_num #count  
    #print "line: ", scan_y
    #print "............................................"
        
    inters_array=[] 
    inters_array_sorted_list=[] 

cv2.imshow("poly",blank_image)
cv2.waitKey(0)
