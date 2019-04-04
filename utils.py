import time
import copy
import numpy as np

def buildTopology(path):
    topology = None
    with open(path, 'r') as f:
        lines = f.readlines()
        elementNum = len(lines) - 3
        topology = np.zeros((elementNum, elementNum))
        elements = []

        count = 0
        for i, line in enumerate(lines):
            if ';' in line:
                elements.append(line.split(';')[0])
                topology[count] = np.asarray(eval(line.split(';')[1]))
                count += 1
        topology = topology + topology.T

    return topology, elements

#联通表
class AdjGraph:
    def __init__(self, num):
        self.adjList = [[] for i in range(num)]

    def addEdge(self, start, end):
        if end not in self.adjList[start]:
            self.adjList[start].append(end)
        if start not in self.adjList[end]:
            self.adjList[end].append(start)

    def buildGraph(self, topology):
        for i, row in enumerate(topology):
            for j, value in enumerate(row):
                if value:
                    self.addEdge(i, j)

    def getAdjList(self):
        return self.adjList

class Graph:
    def __init__(self, topology):
        self.num = len(topology)
        self.adjGraph = AdjGraph(self.num)
        self.adjGraph.buildGraph(topology)
        self.adjList = self.adjGraph.getAdjList()

    def showGraph(self):
        for i, l in enumerate(self.adjList):
            print('{} : {}'.format(i, l))

    def showVisited(self, visited):
        vs = []
        for v, _ in enumerate(visited):
            if _: vs.append(v)
        print(vs)

    def step(self, layer):
        nextLayer = []
        for li in layer:
            lastNode = li[-1]
            connectNodes = copy.deepcopy(self.adjList[lastNode])
            if len(li) >= 2:
                connectNodes.remove(li[-2])

            for node in connectNodes:
                temp = copy.deepcopy(li)
                temp.append(node)
                nextLayer.append(temp)

        return nextLayer

    def findCirles(self, start):
        layer = [[start]]

        circles = []
        for i in range(8):
            layer = self.step(layer)
            #print(layer)
            temp = []
            for li in layer:
                if li[-1] == start:
                    if len(li) == len(set(li))+1:
                        circles.append(li)
                else:
                    temp.append(li)
            layer = temp
        return circles


def getCircles(topology):
    '''
    将不同顺序但是元素相同的circle合并只取第一个
    :param topology:
    :return: circle:list
    '''

    print('检测连接中的环：')
    graph = Graph(topology)
    circles = []
    for anchor in range(len(topology)):
        circles += graph.findCirles(anchor)
        #print(circles)

    circleIndex = []
    for i, circle in enumerate(circles):

        ifInsert = True
        for index in circleIndex:
            if set(circle) == set(circles[index]):
                ifInsert = False
                break
        if ifInsert and len(circle) >= 4:
            circleIndex.append(i)

    circles = [circles[i] for i in circleIndex]

    print('\t检测到{}个环'.format(len(circles)))
    #for circle in circles:
    #    print('\t{}'.format(circle))
    return circles


def splitCircles(circles, topology):
    '''
    找到将circle拆开的方式
    :param circles:
    :return:
    '''
    print('拆分多环 ：')
    if len(circles) == 0 or len(circles) == 1:
        print('\t无多环结构，不需拆分')
        return circles

    print("\t存在{}个不同环".format(len(circles)))

    #递推的寻找在与库中连接最少、大小最小的环
    #寻找最小环
    circles.sort(key=lambda circle:len(circle))

    cleanCircles = []
    cleanCircles.append(circles[0])
    settledNodes = []
    settledNodes += circles[0]


    for circle in circles[1:]:
        for node in circle:
            if node not in settledNodes:
                cleanCircles.append(circle)
                settledNodes += circle
                continue

    print('无重复环:')
    for circle in cleanCircles:
        print('\t{}'.format(circle))
    return cleanCircles


def dfs(topology, curNode, visited = None):
    if not visited:
        visited = []
    connects = topology[curNode]
    connects = [i for i, b in enumerate(connects) if b]

    visited.append(curNode)
    for node in connects:
        if node not in visited:
            visited = dfs(topology, node, visited)

    return visited


def breakCircles(cleanCircles, topology):
    cleanCircles.sort(key= lambda circle:len(circle))

    groups = []
    for circle in cleanCircles:
        tempTopology = copy.deepcopy(topology)
        otherCircles = copy.deepcopy(cleanCircles)
        otherCircles.remove(circle)
        for otherCircle in otherCircles:
            for i in range(len(otherCircle)-1):
                if (otherCircle[i] not in circle) or (otherCircle[i+1] not in circle):
                    tempTopology[otherCircle[i]][otherCircle[i+1]] = 0
                    tempTopology[otherCircle[i+1]][otherCircle[i]] = 0

        group = dfs(tempTopology, circle[0])
        groups.append(group)

    return groups

def getConnectNodes(node, topology):
    row = topology[node]
    connects = [index for index, b in enumerate(row) if b]
    return connects


def getGroupRepeatLine(settleCircles, settleGroups, circle, group):
    #将所有环压缩到不重复的一维
    settleCircles = list(set(settleCircles))

    group = copy.deepcopy(group)
    group = set(group)

    settleGroups = set(settleGroups)

    nodes = list(group&settleGroups)
    #print('Line:{}'.format(nodes))

    cir_cirNodes = []
    cir_groupNodes = []
    indirectNodes = []
    for node in nodes:
        if node in circle and node in settleCircles:
            cir_cirNodes.append(node)
        elif node in circle and node not in settleCircles:
            cir_groupNodes.append(node)
        else:
            indirectNodes.append(node)
    # "这三个判断添加 指的是什么情况"
    #cir_cir:环和环直接相连的点
    #cir_group:环和组连接的点(不包含环和环直接相连)
    #indirectNodes:不直接相连的点，即出现在新组里，但是没有出现在前面已经固定的组里的树枝节点

    return cir_cirNodes, cir_groupNodes, indirectNodes


if __name__ == '__main__':
    topology, elements = buildTopology('./arrayInputs/JIANG.txt')
    print(topology)
    initt = time.time()
    circles = getCircles(topology)
    cleancircles = splitCircles(circles, topology)

    groups = breakCircles(cleancircles, topology)
    print('组')

    settleCircles = []
    settleGroups = []
    for circle, group in zip(cleancircles, groups):
        cir_cirNodes, cir_groupNodes, indirectNodes = getGroupRepeatLine(settleCircles, settleGroups, circle, group)

        settleCircles += circle
        settleGroups += group

        print('cir_cirNodes {}'.format(cir_cirNodes))
        print('cir_groupNodes {}'.format(cir_groupNodes))
        print('indirectNodes {}'.format(indirectNodes))
    # for top in circles:
    #     print(top)