import warnings
warnings.filterwarnings("ignore")
import numpy as np

Images = 4140
# Images = 11*3

def find_accu(prd_points,gt__points,pixel_acc,ii):
    all_distance=[]
    lft_prd = prd_points
    lft__gt = gt__points
    # Left Lane Check
    # print('\tSolving Left Lane Points')
    image_total_points=0
    image_matched_points=0
    for j,pnt in enumerate(lft_prd):
        
        # if int(j/6)==0:
        #     pxl_acc = pixel_acc+1
        # else:
        #     pxl_acc = pixel_acc
        
        # pxl_acc = pixel_acc+len(lft_prd)-j+1
        pxl_acc = pixel_acc+len(lft_prd)-int(j*0.9)-2
        

        
        # pxl_acc = pixel_acc+5-int(j/2)
        # if ii==0:
        #     print(pxl_acc)


        if j >0:
            distance = abs(pnt[1]-lft_prd[0][1])
            # print('\tPoint No',0,' : ',lft_prd[0],"\t&   Point No",j," : ",pnt,'\t  has a Vertical Distance is\t',distance)
            all_distance.append(distance)
        else:
            # print('\tPoint No',j,' : ',pnt)
            pass
        image_total_points+=1
        positive=0
        matching=[]
        cur_dis, prv_dis = 0, pxl_acc+1 
        # Check if predicted point is in vertical range of grouth truth points
        for k,gt_pnt in enumerate(lft__gt):
            if pnt[1] in range(gt_pnt[1]-pxl_acc,gt_pnt[1]+pxl_acc):
                cur_dis = abs(pnt[1]-gt_pnt[1])
                if cur_dis<prv_dis:
                    matched_point = gt_pnt
                    matching.append(gt_pnt)
                    prv_dis = cur_dis
                positive+=1

        # Predicted point is not in vertical range of any ground truth points
        if positive==0:
            # print('\t\t Point',pnt,' has no matching point in GT Data',lft__gt)
            pass
         
        # Predicted point is in vertical range of any ground truth points
        if positive>0:
            # print("Point",pnt,"matched with",positive,"points. ",matching)
            # If predicted point is in horizontal range
            if pnt[0] in range(matched_point[0]-pxl_acc,matched_point[0]+pxl_acc):
                # print('\t\t Point',pnt,' is matched with ',matched_point)
                # total_accuracy +=1
                image_matched_points +=1
            # If predicted point is not in horizontal range
            else:
                # print('\t\t Point',pnt,' is not in X Range of ',matched_point)
                pass

    return(image_total_points,image_matched_points,all_distance)


# f = open("lane_result_tusimple", "r")
f = open("All_Images.txt", "r")
lines = f.readlines()
f.close()

img_no = 0
all_data, img_data = [], []
lft_prd, rgt_prd, lft__gt, rgt__gt = [], [], [], []
# lft_prd, rgt_prd, lft__gt, rgt__gt = {},{},{},{}

full_data = {}

# print('\tProcessing Started')
# for i in range(Images):
for i in range(len(lines)):
    img_div = 11
    if i % img_div==0:
        img_data = []
        lin=0  


    # print("\t Line No",i%img_div," : ",lines[i])  
    img_data.append(lines[i])

    if i%img_div == 3-1: #Left Lane Predicted Data
        points = lines[i].split(',,')
        points = [s.strip(' [[]]\n') for s in points]
        points = [np.fromstring(s,sep=',').astype(int)  for s in points]
        lft_prd.append(np.array(points))
    if i%img_div == 4-1: #Left Lane Ground Truth Data
        points = lines[i][14:].split(',,')
        points = [s.strip(' [[]]\n') for s in points]
        points = [np.fromstring(s,sep=',').astype(int)  for s in points]
        lft__gt.append(np.array(points))
    if i%img_div == 8-1: #Right Lane Predicted Data
        points = lines[i].split(',,')
        points = [s.strip(' [[]]\n') for s in points]
        points = [np.fromstring(s,sep=',').astype(int)  for s in points]
        rgt_prd.append(np.array(points))
    if i%img_div == 9-1: #Right Lane Ground Truth Data
        points = lines[i][14:].split(',,')
        points = [s.strip(' [[]]\n') for s in points]
        points = [np.fromstring(s,sep=',').astype(int)  for s in points]
        rgt__gt.append(np.array(points))

    if i % img_div==0:
        img_no +=1
        img_name = lines[i]      
        if i!=0:
            all_data.append(img_data)
            full_data[img_no] =img_data  
#         print("\n\nImage No",img_no)
#         print('New Image Data at line no',i," ==> ",lines[i])
# print('\tProcessing Completed\n')
# print('\tNumber of Images = ',len(all_data),'\n')
print("\n\n\n\n\tTotal Number of Left Lane Points  = ",len(lft_prd))
print("\tTotal Number of Left Lane Grouth Truth Points = ",len(lft__gt),'\n')
print("\tTotal Number of Right Lane Points = ",len(rgt_prd))
print("\tTotal Number of Right Lane Grouth Truth  Points = ",len(rgt__gt),'\n')
print('\n\n\tCalculating Accuracy\n\n')

pixel_accuracy = [1,3,5,7,9,11]
# pixel_accuracy = [19,21]
for pxl_acc in pixel_accuracy:
    matched_points, total_points, max_left, min_left, max_right, min_right = 0, 0, [], [], [], []        
    for i in range(len(lft_prd)):
        
        # print('\nImage No',i)

        # if i==60:
        #     print('here')

        left_image_total_points,    left_image_matched_points,  left_all_distance   = find_accu(lft_prd[i],lft__gt[i],pxl_acc,i)
        right_image_total_points,   right_image_matched_points, right_all_distance  = find_accu(rgt_prd[i],rgt__gt[i],pxl_acc,i)

        left_accuracy   = (left_image_matched_points/left_image_total_points)*100
        right_accuracy  = (right_image_matched_points/right_image_total_points)*100

        max_left.append(  max(left_all_distance ))
        min_left.append(  min(left_all_distance ))
        max_right.append( max(right_all_distance))
        min_right.append( min(right_all_distance))
        # print('\nleft_all_distance',left_all_distance)
        # print('right_all_distance',right_all_distance)

        #print('\n\tLeft  Lane\n\t\tAccuracy = ',left_accuracy ,'\n\t\tMaximum Distance =',max(left_all_distance) ,'\n\t\tMinimum Distance =',min(left_all_distance ) ,'\n')
        #print('\n\tRight Lane\n\t\tAccuracy = ',right_accuracy,'\n\t\tMaximum Distance =',max(right_all_distance),'\n\t\tMinimum Distance =',min(right_all_distance ),'\n')
        
        
        matched_points  = right_image_matched_points + left_image_matched_points + matched_points
        total_points    = right_image_total_points   + right_image_total_points  + total_points


    # print('max_left  :' , max_left)
    # print('min_left  :' , min_left)
    # print('max_right :' , max_right)
    # print('min_right :' , min_right)    

    # FP = total / Npred

    print("\t",pxl_acc,"pixel accuracy is",round((matched_points/total_points)*100,2),'%')
print('\n\n\n\n\n\n\n')