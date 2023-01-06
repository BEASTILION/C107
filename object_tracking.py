import cv2
import time
import math


p1 = 530
p2 = 300

xs = []
ys = []

video = cv2.VideoCapture("bb3.mp4")
#loader traker 
tracker = cv2.TrackerCSRT_create()


# Read the first frame of videp
returned ,img = video.read()   


# Select the bounding box on the image
bbox= cv2.selectROI("Tracking",img,False)


# Initialise the tracker on the img and the bounding box
tracker.init(img,bbox)

print(bbox)

def drawBox(img,bbox):

    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)
    cv2.putText(img,'Tracking' ,(75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
    

def goal_track(img,bbox):
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])

    # Get the CENTER Points of the Bounding Box
    C1 = x+int(w/2)
    C2 = y+int(h/2)

     # Draw a small circle using CENTER POINTS
    cv2.circle(img,(C1,C2),2,(0,255,0),5)
    
    cv2.circle(img,(int(p1),int(p2)),2,(0,255,0),3)

    #calculate distance
    dist = math.sqrt((C1-p1)**2 +(C2-p2)**2)
    print(dist)

    # Goal is reached if distance is less than 20 pixel points
    
    if (dist <= 20 ):
         cv2.putText(img,"Goal",(300,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
        

    xs.append(C1)
    ys.append(C2)

    #drawing trajectory
    for i in range(len(xs)-1):
        cv2.circle(img, (xs[i],ys[i]),2,(0,0,255),5)
        





    
while True:
    check,img = video.read()   

    # Update the tracker on the img and the bounding box
    success,bbox = tracker.update(img)

    # Call drawBox()
    if success:
         drawBox(img, bbox)
        
    else:
        cv2.putText(img,'LOST' ,(75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        
        
    # Call goal_track()
    goal_track(img, bbox) 

    cv2.imshow("result",img)
            
    key = cv2.waitKey(25)

    if key == 32:
        print("Stopped!")
        break
 

video.release()
cv2.destroyALLwindows()
