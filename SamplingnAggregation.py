class Point:
  def __init__(self,x,y):
    self.longitude,self.latitude = x,y

class LeafNode:
  def __init__(self, x, y):
    self.left = None
    self.right = None
    self.point = Point(x,y)
    
class InternalNode:
  def __init__(self, l1,l2,l3,l4):
    self.left = None
    self.right = None
    self.MMBR = []
    self.MMBR.append(l1)
    self.MMBR.append(l2)
    self.MMBR.append(l3)
    self.MMBR.append(l4)

# Data List is generally taken from pre-processed RawData from the file "processedData.pkl"
# The below list is used only for testing
dataList = [[1,5],[3,5],[2,4],[5,7],[4,2],[2,3],[3,8],[4,6]]

# Constructing leaf Nodes
NodeList = []
for i in range(len(dataList)):
  node = LeafNode(dataList[i][0],dataList[i][1])
  NodeList.append(node)

# Building starting from internal Nodes
n = len(NodeList)//2
p = 0
LeavesFlag = True
root = None
while(True):
  if(len(NodeList) == 1):
    break
  while(len(NodeList) > n):
    print(n,len(NodeList))
    if(LeavesFlag):
      leftLeafNode = NodeList[p].point
      rightLeafNode = NodeList[p+1].point
      internalNode = InternalNode(leftLeafNode,Point(leftLeafNode.longitude,rightLeafNode.latitude),rightLeafNode,Point(rightLeafNode.longitude,leftLeafNode.latitude))
      internalNode.left = NodeList[p]
      internalNode.right = NodeList[p+1]
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
      NodeList.pop(0)
      NodeList.pop(0)
      NodeList.append(internalNode)
  n = n//2
  LeavesFlag = False


# Below code is used for testing purpose i.e., level order of the tree
def printLevelOrder(root):
    h = height(root)
    for i in range(1, h+1):
        printCurrentLevel(root, i)


def printCurrentLevel(root, level):
    if root is None:
        return
    if level == 1:
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
    if node is None:
        return 0
    else:
        lheight = height(node.left)
        rheight = height(node.right)
 
        if lheight > rheight:
            return lheight+1
        else:
            return rheight+1

# printing levelOrder (Used for testing the code)
#printLevelOrder(NodeList[0])
import sys

def Querydiagonals(query):
  return InternalNode(Point(query[0][0],query[0][1]),Point(query[0][0],query[1][1]),Point(query[1][0],query[1][1]),Point(query[1][0],query[0][1]))

def nodeDiagonals(curr):
  longitudeList = []
  latitudeList = []
  for i in range(len(curr.MMBR)):
    longitudeList.append(curr.MMBR[i].longitude)
    latitudeList.append(curr.MMBR[i].latitude)
  return min(longitudeList), min(latitudeList), max(longitudeList), max(latitudeList)

def doOverlap(l1, r1, l2, r2):
  print(r2.longitude,r2.latitude,l2.longitude,l2.latitude)
  if l1.longitude == r1.longitude or l1.latitude == r1.latitude or r2.longitude == l2.longitude or l2.latitude == r2.latitude:
    return False
  if l1.longitude > r2.longitude or l2.longitude > r1.longitude:
    return False
  if r1.latitude > l2.latitude or r2.latitude > l1.latitude:
    return False
  else:
    return True

def processQuery(query,curr,overlapList):
  if curr == None:
    return
  if curr.left == None:
    return
  if curr.right == None:
    return
  longitudeLeftMin, latitudeLeftMin, longitudeLeftMax, latitudeLeftMax = nodeDiagonals(curr.left)
  longitudeRightMin, latitudeRightMin, longitudeRightMax, latitudeRightMax = nodeDiagonals(curr.right)
  longitudeMin, latitudeMin, longitudeMax, latitudeMax = nodeDiagonals(query)
  if(doOverlap(Point(longitudeLeftMin,latitudeLeftMax),Point(longitudeLeftMax,latitudeLeftMin),Point(longitudeMin,latitudeMax),Point(longitudeMax,latitudeMin))):
      print(curr.left.MMBR[0].longitude, curr.left.MMBR[0].latitude, end = " ")
      print(curr.left.MMBR[1].longitude, curr.left.MMBR[1].latitude, end = " ")
      print(curr.left.MMBR[2].longitude, curr.left.MMBR[2].latitude, end = " ")
      print(curr.left.MMBR[3].longitude, curr.left.MMBR[3].latitude)
      overlapList.append(curr.left)
      processQuery(query,curr.left,overlapList)
  if(doOverlap(Point(longitudeRightMin,latitudeRightMax),Point(longitudeRightMax,latitudeRightMin),Point(longitudeMin,latitudeMax),Point(longitudeMax,latitudeMin))):
      print(curr.right.MMBR[0].longitude, curr.right.MMBR[0].latitude, end = " ")
      print(curr.right.MMBR[1].longitude, curr.right.MMBR[1].latitude, end = " ")
      print(curr.right.MMBR[2].longitude, curr.right.MMBR[2].latitude, end = " ")
      print(curr.right.MMBR[3].longitude, curr.right.MMBR[3].latitude)      
      overlapList.append(curr.right)
      processQuery(query,curr.right,overlapList)

query = [[2,2],[3,3]]
curr = NodeList[0]
overlapList = []
query = Querydiagonals(query)
processQuery(query,NodeList[0],overlapList)
print(overlapList)
