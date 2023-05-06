#!/usr/bin/env python
# coding: utf-8

# # Reading preprocessed data




import pickle
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import sys
import csv
import numpy as  np
import math
    
# Rounding off the length to the nearest power of 2 so that a binary tree can be constructed
def highestPowerof2( n):
    if (n < 1):
        return 0
    res = 1
    for i in range(8*sys.getsizeof(n)):   
        curr = 1 << i
        if (curr > n):
             break
        res = curr
    return res
 
# Reading the data from the preprocessed pkl file and scaling the values 
# Converting longitudes and latitudes using the x,y formula
def populatePreprocessedData(fileName):
    file = open(fileName,'rb')
    data = pickle.load(file)
    scaler = MinMaxScaler(feature_range=(0, 10000))
    data['longtitude'] = scaler.fit_transform(data[['longtitude']])
    data['latitude'] = scaler.fit_transform(data[['latitude']])
    finalData = []
    for i in range(data.shape[0]):
        finalData.append([(data['longtitude'][i] + 180) * 1000 / 360 , (data['latitude'][i] + 90) *  1000/ 180])
    length = highestPowerof2(len(finalData))
    return finalData[:length],scaler


# # LS-Tree 

# In[11]:


import random

# Node class for linkedList implementation
class Node:
    def __init__(self, x,y):
        self.longitude,self.latitude = x,y
        self.next = None
# Point class for storing longitudes and latitudes
class Point:
    def __init__(self,x,y):
        self.longitude,self.latitude = x,y

# LeafNode with no MMBR 
class LeafNode:
    def __init__(self, x, y):
        self.left = None
        self.right = None
        self.point = Point(x,y)
        self.MMBR = []
        self.totalLeafNodes = []

# InternalNode class for storing Minimum Bounding region (MMBR)
class InternalNode:
    def __init__(self, l1,l2,l3,l4):
        self.left = None
        self.right = None
        self.MMBR = []
        self.MMBR.append(l1)
        self.MMBR.append(l2)
        self.MMBR.append(l3)
        self.MMBR.append(l4)
        self.totalLeafNodes = []

# LSTree construction with sampling the nodes exactly half at each level
def LSTreeSampling(data):
    pHead = None
    for i in range(len(data)):
        if(pHead is None):
            pHead = Node(data[i][0],data[i][1])
            curr = pHead
        else:
            pTemp = Node(data[i][0],data[i][1])
            curr.next = pTemp
            curr = pTemp
    levels = []
    levels.append(pHead)
    randomList = ['.next','.next.next']
    while(True):
        DummyHead = Node('#','$')
        DummyHead.next = pHead
        curr = DummyHead
        lHead = None
        if pHead.next is None:
            break
        while(curr.next is not None):
            randomVal = random.randint(0, 1)
            curr = eval('curr' + randomList[randomVal])
            if lHead is None:
                lHead = Node(curr.longitude,curr.latitude)
                currLevel = lHead
            else:
                pTemp = Node(curr.longitude,curr.latitude)
                currLevel.next = pTemp
                currLevel = pTemp
            if randomVal == 0:
                curr = curr.next
        levels.append(lHead)
        pHead = lHead
    return (levels)

# Used for testing(for printing the levels)
def printingLevels(levels):
    for i in range(len(levels)):
        curr = levels[i]
        while(curr is not None):
            print(curr.longitude,curr.latitude)
            curr = curr.next  
        print("-------")

# For building R Trees for each level in the LS-Tree
def buildingRTrees(levels):
    RTrees = []
    for k in range(len(levels)):
        currL = levels[k]
        NodeList = []
        while(currL is not None):
            node = LeafNode(currL.longitude,currL.latitude)
            NodeList.append(node)
            currL = currL.next
        n = len(NodeList)//2
        p = 0
        count = 0
        LeavesFlag = True
        root = None
        while(True):
            if(len(NodeList) == 1):
                break
            while(len(NodeList) > n):
                if(LeavesFlag):
                    leftLeafNode = NodeList[p].point
                    rightLeafNode = NodeList[p+1].point
                    internalNode = InternalNode(leftLeafNode,Point(leftLeafNode.longitude,rightLeafNode.latitude),rightLeafNode,Point(rightLeafNode.longitude,leftLeafNode.latitude))
                    internalNode.left = NodeList[p]
                    internalNode.right = NodeList[p+1]
                    internalNode.totalLeafNodes.append(leftLeafNode)
                    internalNode.totalLeafNodes.append(rightLeafNode)
                    count+=1
                    NodeList.pop(0)
                    NodeList.pop(0)
                    NodeList.append(internalNode)
                else:
                    longitudeList = []
                    latitudeList = []
                    leftInternalNode = NodeList[p]
                    rightInternalNode = NodeList[p+1]
                    for i in range(0,len(leftInternalNode.MMBR)):
                        longitudeList.append(leftInternalNode.MMBR[i].longitude)
                        latitudeList.append(leftInternalNode.MMBR[i].latitude)
                    for i in range(0,len(rightInternalNode.MMBR)):
                        longitudeList.append(rightInternalNode.MMBR[i].longitude)
                        latitudeList.append(rightInternalNode.MMBR[i].latitude)
                    internalNode = InternalNode(Point(min(longitudeList),max(latitudeList)),Point(max(longitudeList),max(latitudeList)),Point(min(longitudeList),min(latitudeList)),Point(max(longitudeList),min(latitudeList)))
                    internalNode.left = leftInternalNode
                    internalNode.right = rightInternalNode
                    for ind in leftInternalNode.totalLeafNodes:
                        internalNode.totalLeafNodes.append(ind)
                    for ind in rightInternalNode.totalLeafNodes:
                        internalNode.totalLeafNodes.append(ind)
                    NodeList.pop(0)
                    NodeList.pop(0)
                    NodeList.append(internalNode)
            n = n//2
            LeavesFlag = False
        RTrees.append(NodeList[0])
    return RTrees

# used for testing the R-trees by going in a levelorder fashion
def printLevelOrder(root):
    h = height(root)
    for i in range(1, h+1):
        printCurrentLevel(root, i)

def printCurrentLevel(root, level):
    if root is None:
        return
    if level == 1:
        for i in root.totalLeafNodes:
            print(i.longitude,i.latitude, end = " | ")
        print("",end= "--")
        if len(root.MMBR) > 0:
            print(root.MMBR[0].longitude,root.MMBR[0].latitude, end = " ")
            print(root.MMBR[1].longitude,root.MMBR[1].latitude, end = " ")
            print(root.MMBR[2].longitude, root.MMBR[2].latitude, end = " ")
            print(root.MMBR[3].longitude, root.MMBR[3].latitude)
    elif level > 1:
        print("left")
        printCurrentLevel(root.left, level-1)
        print("right")
        printCurrentLevel(root.right, level-1)

def height(node):
    if node is None :
        return 0
    else:
        lheight = height(node.left)
        rheight = height(node.right)
 
        if lheight > rheight:
            return lheight+1
        else:
            return rheight+1


# # Query Processing in LS-Tree

# In[12]:

# For Creating a InternalNode with query provided 
def Querydiagonals(query):
    return InternalNode(Point(query[0][0],query[0][1]),Point(query[0][0],query[1][1]),Point(query[1][0],query[1][1]),Point(query[1][0],query[0][1]))

# Retrieving the top left value and right bottom value which is used for computing overlapping rectangles logic
def nodeDiagonals(curr):
    longitudeList = []
    latitudeList = []
    for i in range(len(curr.MMBR)):
        longitudeList.append(curr.MMBR[i].longitude)
        latitudeList.append(curr.MMBR[i].latitude)
    return min(longitudeList), max(latitudeList), max(longitudeList), min(latitudeList)

# Returns if two rectangles overlap 
def Isoverlap(l1,r1,l2,r2):
    if (l1.longitude > r2.longitude) or (l2.longitude > r1.longitude):
        return False
    if (r1.latitude > l2.latitude) or (r2.latitude > l1.latitude):
        return False
    return True

# Returns if the point lies inside a given MMBR rectangle
def doPointOverlap(x1, y1, x2, y2, x, y) :
    if (x >= x1 and x <= x2 and y <= y1 and y >= y2) :
        return True
    else :
        return False
    

