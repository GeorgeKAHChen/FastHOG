#DBSCAN demo

eps = 4
minS = 25

Table = []

def Initial():
	import math
	AreaTable = [[0 for n in range(2 * eps + 1)] for n in range(2 * eps + 1)]
	Total = 0
	for i in range(0, 2 * eps + 1):
		for j in range(0, 2 * eps + 1):
			if i == eps and j == eps:
				continue
			if math.sqrt(pow(i - eps, 2) + pow(j - eps, 2)) <= eps:
				Total += 1
				AreaTable[i][j] = 1

	Table = [[0, 0] for n in range(Total)]
	Val = 0
	for i in range(0, 2 * eps + 1):
		for j in range(0, 2 * eps + 1):
			if AreaTable[i][j] == 1:
				Table[Val][0] = i - eps
				Table[Val][1] = j - eps
				Val += 1

	return Table



def DBSCAN(height, width, InpImg, Table):
	LabelImg = [[0 for n in range(width)] for n in range(height)]
	OuterNode = []
	ClusterVal = 0
	for i in range(0, height):
		for j in range(0, width):
			if InpImg[i][j] == 0:
				continue

			Point = 0
			Inner = 0
			willCluster = 0
			for k in range(0, len(Table)):
				ValY = i + Table[k][0]
				ValX = j + Table[k][1]
				if ValY < 0 or ValY >= height or ValX < 0 or ValX >= width:
					continue

				if InpImg[ValY][ValX] == 1:
					Point += 1

				if Point >= minS:
					Inner = 1
					if LabelImg[i][j] == 0:
						willCluster = 1
						break
					else:
						break

			if not Inner:
				OuterNode.append([i, j])
				continue

			if willCluster:
				ClusterSet = []
				ClusterSet.append([i, j])
				ClusterVal += 1
				while 1:
					Node = ClusterSet.pop()
					iNew = Node[0]
					jNew = Node[1]
					LabelImg[iNew][jNew] = ClusterVal
					for k in range(0, len(Table)):
						ValY = iNew + Table[k][0]
						ValX = jNew + Table[k][1]
					
						if ValY < 0 or ValY >= height or ValX < 0 or ValX >= width:
							continue

						if LabelImg[ValY][ValX] != 0:
							continue

						if InpImg[ValY][ValX] == 1:
							ClusterSet.append([ValY, ValX])
					
					if len(ClusterSet) == 0:
						break

	return LabelImg, OuterNode, ClusterVal
			









