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