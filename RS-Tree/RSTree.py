#!/usr/bin/env python
# coding: utf-8

# # Importing Modules


import random
import math
import pandas as pd
import time
from sklearn.preprocessing import MinMaxScaler
import pickle


# # Structure of Point Class and Node



class Point:
    def __init__(self,x,y):
        self.longitude,self.latitude = y,x
        
    def __str__(self):
        return f'{self.latitude},{self.longitude}'

class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.next = None
        self.P = None
        self.sample = None
        self.MBB = None
        
    


# # Generating Point objects from raw data


def generatePointList(array):
    pointList = []
    for lat,long in array:
        pointList.append(Point(lat,long))
    return pointList
        

# # Loading Data



file = open('data.pkl','rb')
data = pickle.load(file)

scaler = MinMaxScaler(feature_range=(0, 10000))
data['longtitude'] = scaler.fit_transform(data[['longtitude']])
data['latitude'] = scaler.fit_transform(data[['latitude']])

finalData = []
for i in range(data.shape[0]):
    finalData.append([(data['longtitude'][i] + 180) * 1000 / 360,(data['latitude'][i]+90)*1000/ 180])

# # Generating Leaf Nodes


def generateLeaves(pointList):
    head = None
    curr = None
    head = Node()
    head.P = [pointList[0]]
    for i in range(1,len(pointList)):
            if(head.next == None):
                head.next = Node()
                curr = head.next
            else:
                curr.next = Node()
                curr = curr.next
            curr.P = [pointList[i]]
            curr.MBB = findMinimumBound(curr.P)
    return head
    


# # Print the Sample Buffer 


def printList(head):
    curr = head
    j=0
    while curr!=None:
        print(f'Node {j}')
        if curr.sample != None:
            array = curr.sample
        else:
            array = curr.P
            
        for i in array:
            print(i)
        j = j+1
        curr = curr.next
        


# # Find the Minimum Bounding Box of the given Point List


def findMinimumBound(pointList):
    minLat = math.inf
    maxLat = -math.inf
    
    minLong = math.inf
    maxLong = -math.inf
    
    for point in pointList:
        minLat = min(point.latitude,minLat)
        maxLat = max(point.latitude,maxLat)
        
        minLong = min(point.longitude,minLong)
        maxLong = max(point.longitude,maxLong)
        
    return [Point(minLat,minLong),Point(minLat,maxLong),Point(maxLat,minLong),Point(maxLat,maxLong)]


# # Check if the MBB of node is overlapping

def overlap(l1,r1,MBB):
    if MBB == None:
        return True
    l2 = MBB[1]
    r2 = MBB[2]
    if (l1.latitude > r2.latitude) or (l2.latitude > r1.latitude):
        return False
    if (r1.longitude > l2.longitude) or (r2.longitude > l1.longitude):
        return False
    return True
    
    


# # Generate a level with the given child head node



def generateLevel(childHead,d):
    currIter = childHead
    currHead = None
    curr = None
    currHead = Node()
    currHead.left = currIter
    currHead.right = currIter.next
    currHead.P = currHead.left.P + currHead.right.P
    currHead.MBB = findMinimumBound(currHead.P)
    
    if len(currHead.P)>d:
        currHead.sample = random.choices(currHead.P,k=d)
        
    currIter = currIter.next.next

    while currIter != None:
        if currHead.next == None:
            currHead.next = Node()
            curr = currHead.next
        else:
            curr.next = Node()
            curr = curr.next

        curr.left = currIter
        curr.right = currIter.next
        curr.P = curr.left.P + curr.right.P
        if len(curr.P) > d:
            curr.sample = random.choices(curr.P,k=d)
        curr.MBB = findMinimumBound(curr.P)
        currIter = currIter.next.next

    return currHead




import sys
def highestPowerof2(n):
    if n < 1:
        return 0
    res = 1
    for i in range(8*sys.getsizeof(n)):
        curr = 1 << i
        if (curr > n):
             break
        res = curr
    return res

length = highestPowerof2(len(finalData))
data = finalData[:length]


# # Preprocessing


start_time = time.time()
headSet = []
pointList = generatePointList(data)
leaves = generateLeaves(pointList)
headSet.append(leaves)
while headSet[-1].next !=None:
    headSet.append(generateLevel(headSet[-1],1000))
print("%s seconds to run preprocessing..."% (time.time()-start_time))




# # Query Processing Function


def queryProcessing(point1 , point2, headSet):
    result = set()
    csv = "Latitude,Longitude"
    count =0
    p = reversed(headSet)
    for head in p:
        csv = "Latitude,Longitude"
        curr = head
        st = time.time()
        while curr.next!=None:
            if overlap(point1,point2,curr.MBB):
                if curr.sample != None:
                    for sample in curr.sample:
                        if pointInside(sample,point1,point2):
                            #Uncomment these lines to get results in csv
                            
                            newLat,newLong = scaler.inverse_transform([[sample.latitude,sample.longitude]])[0]
                            csv = csv + "\n" + str(newLat) +"," + str(newLong)
                            result.add(sample) 
                         
                else:
                    for sample in curr.P:
                        if pointInside(sample,point1,point2):
                            #Uncomment these lines to get results in csv
                            
                            newLat,newLong = scaler.inverse_transform([[sample.latitude,sample.longitude]])[0]
                            csv = csv + "\n" + str(newLat) +"," + str(newLong)
                            result.add(sample) 
            curr = curr.next
        count = count+1
        
        print(f'count of results {len(result)} time = {time.time()-st}')
        
#Uncomment these lines to get results in csv
        
        s1 = f"results{count}.csv"
        with open(s1, 'w') as out:
             out.write(csv)
            
        answer = 'Y'
        
        print("Do you want to continue Y/N")
        
        answer = input()
        
        if answer == 'N':
            return
        
            


# # Checks if Point is inside the Range or not

# In[292]:


def pointInside(point, point1 , point2):
    if (point.latitude > point1.latitude) and (point.longitude < point1.longitude) and (point.latitude < point2.latitude) and (point.longitude > point2.longitude):
        return True
    else:
        return False

print('Welcome to Aggregation and Sampling')
print('Enter query range')
minXVal = math.inf
minYVal = math.inf
maxXVal = -math.inf
maxYVal = -math.inf
for i in range(4):
    print(f'Enter Coordinate-{i+1}')
    print('X-Value',end=":")
    x = (float(input())) 
    print('Y-Value',end=":")
    y = (float(input()))
    minXVal = min(minXVal,x)
    maxXVal = max(maxXVal,x)
    minYVal = min(minYVal,y)
    maxYVal = max(maxYVal,y)

query = [[minXVal,maxYVal],[maxXVal,minYVal]]
point1 = Point(minXVal,maxYVal)
point2 = Point(maxXVal,minYVal)

queryProcessing(point1,point2,headSet)







