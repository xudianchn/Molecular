import copy
import matplotlib.pyplot as plt
import math
from utils import buildTopology, getCircles, splitCircles, breakCircles, getGroupRepeatLine
from graphDraw import chemistryDraw
import time

class AtomNode:
    def __init__(self,element, ID):
        # X坐标, Y坐标, 是否已经确定位置
        self.ID = ID
        self.element = element
        self.coordinate = [0, 0, False]
        # [(node, bondingNum, direction)]
        self.edges = []

    def connect(self, node, direction, topology):
        assert type(AtomNode) == type(AtomNode)
        edge = [node, topology[self.ID][node.ID], direction]
        self.edges.append(edge)

    def setCoordinate(self, x, y):
        self.coordinate = [x, y, True]

    def showInfo(self):
        print('----- {} ----- '.format(self.ID))
        print('元素: {}  坐标: {}'.format(self.element, self.coordinate))
        print('连接节点:')
        for edge in self.edges:
            node = edge[0]
            print('  ID {}  元素 {}'.format(node.ID, node.element))


def buildMolecularMap(elements):
    molecularMap = {}
    for i, element in enumerate(elements):
        molecularMap[i] = AtomNode(element, i)
    return molecularMap


def shiftMolecularMap(index, x, y ,theta, molecularMap):
    '''
    将图旋转theta角度，将index的node设置到x, y
    :param index:
    :param x:
    :param y:
    :param theta:
    :param molecularMap:
    :return:
    '''
    molecularMap = copy.deepcopy(molecularMap)
    for key in molecularMap.keys():
        node = molecularMap[key]
        x_ori = node.coordinate[0]
        y_ori = node.coordinate[1]

        r = math.sqrt(x_ori*x_ori + y_ori*y_ori)
        theta_new = math.atan2(y_ori, x_ori) + theta
        x_new = r*math.cos(theta_new)
        y_new = r*math.sin(theta_new)

        node.setCoordinate(x_new, y_new)

    node = molecularMap[index]
    x_ = node.coordinate[0]
    y_ = node.coordinate[1]
    dx = x - x_
    dy = y - y_

    for key in molecularMap.keys():
        node = molecularMap[key]
        x_ori = node.coordinate[0]
        y_ori = node.coordinate[1]

        x_new = x_ori + dx
        y_new = y_ori + dy

        node.setCoordinate(x_new, y_new)
    return  molecularMap


def setCircleNodesCoordinate(circleNodes, molecularMap, topology):
    '''
    检测得到基准环后，设定基准环的坐标
    :param circleNodes: Node index list
    :param molecularMap: 原子连接表
    :param topology: 元素list
    :return: molecularMap
    '''
    angle = (len(circleNodes) - 2 - 1) / (len(circleNodes) - 1) * 180 / 180 * math.pi
    length = 50

    x0 = 0
    y0 = 0
    theta = angle / 2
    x1 = length * math.cos(theta) + x0
    y1 = length * math.sin(theta) + y0

    for i, node in enumerate(circleNodes[:-1]):
        molecularMap[node].setCoordinate(x0, y0)

        x0, y0 = x1, y1
        theta = -(math.pi - theta - angle)
        x1 = length * math.cos(theta) + x0
        y1 = length * math.sin(theta) + y0

    if len(circleNodes) == 7:
        for i, node in enumerate(circleNodes[:-1]):
            if i < 2 or i > 4:
                molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'down', topology)
            else:
                molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'up', topology)
                # print('down')
    else:
        raise ('To do: 未设定{}个节点正多边形'.format(len(circleNodes)))

    return molecularMap


def setLinkNodesCoordinate(startNodes, molecularMap, topology, elements):
    layerIndex = 0
    layers = []
    layers.append(startNodes)

    #nextLayer = []
    layerNodes = startNodes

    checkedNodes = []

    while layerNodes:
        print('\n----- layer {} layerNodes {} -----'.format(layerIndex, layerNodes))
        for l in layers:
            checkedNodes += l
        checkedNodes = list(set(checkedNodes))

        nextLayerNodes = []
        for node in layerNodes:
            nodeID = molecularMap[node].ID
            nodeElement = molecularMap[node].element
            nodeCoord = molecularMap[node].coordinate
            x0 = molecularMap[node].coordinate[0]
            y0 = molecularMap[node].coordinate[1]

            settleNodes = []
            freeNodes = []

            connections = [i for i, _ in enumerate(topology[nodeID]) if int(_) > 0]
            for nextLayerNodeIndex in connections:
                if nextLayerNodeIndex in checkedNodes:
                    settleNodes.append(
                        (nextLayerNodeIndex, elements[nextLayerNodeIndex], topology[node][nextLayerNodeIndex]))
                else:
                    freeNodes.append(
                        (nextLayerNodeIndex, elements[nextLayerNodeIndex], topology[node][nextLayerNodeIndex]))

            # print('\nCurrent Node {} {} {}'.format(nodeID, nodeElement, nodeCoord))
            # print('SettleNodes {}  FreeNodes {}'.format(settleNodes, freeNodes))

            if len(freeNodes) == 1:
                x1 = 0
                y1 = 0
                for node2 in settleNodes:
                    x1 += molecularMap[node2[0]].coordinate[0]
                    y1 += molecularMap[node2[0]].coordinate[1]
                x1 = x1 / len(settleNodes)
                y1 = y1 / len(settleNodes)
                theta = math.atan2((y1 - y0), (x1 - x0)) + math.pi

                x_tar = x0 + math.cos(theta) * 50
                y_tar = y0 + math.sin(theta) * 50

                molecularMap[freeNodes[0][0]].setCoordinate(x_tar, y_tar)
                molecularMap[node].connect(molecularMap[freeNodes[0][0]], 'down', topology)

                nextLayerNodes.append(freeNodes[0][0])
            elif len(freeNodes) == 2:
                x1 = 0
                y1 = 0
                for node2 in settleNodes:
                    x1 += molecularMap[node2[0]].coordinate[0]
                    y1 += molecularMap[node2[0]].coordinate[1]
                x1 = x1 / len(settleNodes)
                y1 = y1 / len(settleNodes)
                theta = math.atan2((y1 - y0), (x1 - x0)) + math.pi

                x1_tar = x0 + math.cos(theta + math.pi / 3) * 50
                y1_tar = y0 + math.sin(theta + math.pi / 3) * 50
                molecularMap[freeNodes[0][0]].setCoordinate(x1_tar, y1_tar)
                molecularMap[node].connect(molecularMap[freeNodes[0][0]], 'up', topology)
                nextLayerNodes.append(freeNodes[0][0])

                x2_tar = x0 + math.cos(theta - math.pi / 3) * 50
                y2_tar = y0 + math.sin(theta - math.pi / 3) * 50
                molecularMap[freeNodes[1][0]].setCoordinate(x2_tar, y2_tar)
                molecularMap[node].connect(molecularMap[freeNodes[1][0]], 'up', topology)
                nextLayerNodes.append(freeNodes[1][0])

        print('nextLayerNodes {}'.format(nextLayerNodes))
        layerNodes = nextLayerNodes
        layers.append(layerNodes)
        layerIndex += 1

    return molecularMap

class Draw():
    def __init__(self):
        pass
        self.dr = chemistryDraw()

    def draw(self, molecularMap, topology, info = None):
        dire = ['single', 'double', 'triple']

        for i in range(len(topology[0])):
            start = (molecularMap[i].coordinate[0], molecularMap[i].coordinate[1])

            startElement = molecularMap[i].element
            if startElement != 'C':
               plt.text(start[0] - 7, start[1] - 7, startElement)

            plt.text(start[0] + 3, start[1] + 3, i)

            for edge in molecularMap[i].edges:
                endElement = edge[0].element
                #if endElement == 'H':
                #    continue
                end = (edge[0].coordinate[0], edge[0].coordinate[1])
                theta = math.atan2(end[1] - start[1], end[0] - start[0])
                if startElement != 'C':
                    x0 = start[0] + 10 * math.cos(theta)
                    y0 = start[1] + 10 * math.sin(theta)
                else:
                    x0 = start[0]
                    y0 = start[1]

                if endElement != 'C':
                    x1 = end[0] - 10 * math.cos(theta)
                    y1 = end[1] - 10 * math.sin(theta)
                else:
                    x1 = end[0]
                    y1 = end[1]

                # print('edge\t{}'.format(edge))
                bondingNum = dire[int(edge[1]) - 1]
                direction = edge[2]
                self.dr.drawLine(x0, y0, x1, y1, bondingNum, direction)

        if info:
            plt.text(-50, 200, info)

    def show(self):
        self.dr.show()


def getBreakTopology(topology, group):
    topology = copy.deepcopy(topology)
    rowLength = len(topology)
    columnLength = len(topology[0])

    for row in range(rowLength):
        for column in range(columnLength):
            if (row not in group) or (column not in group):
                topology[row][column] = 0
    return topology


def getNodeCoordinatefromMaps(molecularMaps, node):
    x_base = 0
    y_base = 0
    for m in molecularMaps:
        x_temp = m[node].coordinate[0]
        y_temp = m[node].coordinate[1]
        if x_temp: x_base = x_temp
        if y_temp: y_base = y_temp
    return x_base, y_base

def getCircleCenter(molecularMaps, circle):
    '''
    计算环中心，用于计算不同环连接时需不需要翻转
    :param molecularMap:
    :param circle:
    :return:
    '''

    coord = []

    mole = None
    for molecularMap in molecularMaps:
        flag = True
        for node in circle:
            if molecularMap[node].coordinate not in coord:
                coord.append(molecularMap[node].coordinate)
            else:
                flag = False
        if flag:
            mole = molecularMap
            break

    x = 0
    y = 0
    for node in circle:
        x += molecularMaps[node].coordinate[0]
        y += molecularMaps[node].coordinate[1]

    x = x/len(circle)
    y = y/len(circle)
    return x, y


def getLinkNode(settledGroups, settleCircles, newGroup, newCircle, molecularMap, molecularMaps, topology):
    nodeIndex = 0
    x_base = 0
    y_base = 0

    cir_cirNodes, cir_groupNodes, indirectNodes = getGroupRepeatLine(settleCircles, settledGroups, newCircle, newGroup)
    removeNodes = indirectNodes

    if len(cir_groupNodes) == 1:
        #找连接线，删除新circle中与已设定重复部分
        linkNode = cir_groupNodes[0]

        x_base, y_base = getNodeCoordinatefromMaps(molecularMaps, linkNode)

    if len(cir_cirNodes) == 2:

        connectCircle = None
        for circle in settleCircles:
            flag = True
            for node in cir_cirNodes:
                if node not in circle:
                    flag = False
            if flag:
                connectCircle = circle
                break

        print('connectCircle\t{}'.format(connectCircle))
        anchor_centerx, anchor_centery = getCircleCenter(molecularMaps, connectCircle)


        x1, y1 = getNodeCoordinatefromMaps(molecularMaps, cir_cirNodes[0])
        x2, y2 = getNodeCoordinatefromMaps(molecularMaps, cir_cirNodes[1])

    print(x_base)
    print(y_base)
    print('settleGroup {}'.format(settledGroups))
    print('cir_cirLinkNodes {}'.format(cir_cirNodes))
    print('cir_groupLinkNodes {}'.format(cir_groupNodes))
    print('indirectConnectNodes {}'.format(indirectNodes))
    return nodeIndex, x_base, y_base, removeNodes


def setGroupsCoordinate(circles, groups, elements, topology, molecularMap):
    if not circles:
        raise ('No circles')

    print('\n开始设定环组的坐标')

    dr = Draw()
    settledNodes = []
    molecularMaps = []
    settledCircles = []

    count = 0
    for circle, group in zip(circles, groups):
        print('\t设定环 {} 组 {}'.format(circle, group))
        mole_temp = copy.deepcopy(molecularMap)

        nodeIndex, x_base, y_base, removeNodes = getLinkNode(settledNodes, settledCircles, group, circle, molecularMap, molecularMaps,topology)
        for removeNode in removeNodes:
            group.remove(removeNode)

        topo_temp = getBreakTopology(topology, group)
        mole_temp = setCircleNodesCoordinate(circle, mole_temp, topo_temp)
        mole_temp = setLinkNodesCoordinate(circle, mole_temp, topo_temp, elements)

        index = circle[0]

        #ToDo
        if count == 1:
            pass

        mole_temp = shiftMolecularMap(index, x_base, y_base, -math.pi/3, mole_temp)

        settledNodes += group
        settledCircles += circle
        molecularMaps.append(mole_temp)
        dr.draw(mole_temp, topo_temp)

        count += 1
    dr.show()


def drawGroup(originalFomularPath, outFomularPath):

    #反应物
    topology, elements = buildTopology(originalFomularPath)
    circles = getCircles(topology)
    cleanCircles = splitCircles(circles, topology)
    groups = breakCircles(cleanCircles, topology)
    print('组')
    for i in range(len(cleanCircles)):
        print('\t环{} 组{}'.format(cleanCircles[i], groups[i]))

    molecularMap = buildMolecularMap(elements)

    #平铺各最小组
    setGroupsCoordinate(cleanCircles, groups, elements, topology, molecularMap)



if __name__ == '__main__':
    drawGroup('arrayInputs/C7H6O3.txt', 'arrayInputs/C7H6O3.txt')