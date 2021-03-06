import numpy as np
import copy
import matplotlib.pyplot as plt
import math
from utils import buildTopology, getCircles
from graphDraw import chemistryDraw


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
            if i < 3:
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

            #print('\nCurrent Node {} {} {}'.format(nodeID, nodeElement, nodeCoord))
            #print('SettleNodes {}  FreeNodes {}'.format(settleNodes, freeNodes))

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
                molecularMap[node].connect(molecularMap[freeNodes[0][0]], 'up', topology)

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


def draw(molecularMap, topology, info = None):
    dire = ['single', 'double', 'triple']

    dr = chemistryDraw()
    for i in range(len(topology[0])):
        start = (molecularMap[i].coordinate[0], molecularMap[i].coordinate[1])

        startElement = molecularMap[i].element
        if startElement != 'C':
            plt.text(start[0] - 7, start[1] - 7, startElement)

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
            bondingNum = dire[int(edge[1]) - 1]
            direction = edge[2]
            dr.drawLine(x0, y0, x1, y1, bondingNum, direction)

    dr.show()


def drawReaction(originalFomularPath, outFomularPath):

    #反应物
    topology, elements = buildTopology(originalFomularPath)
    circles = getCircles(topology)
    print('Elements {}'.format(elements))
    if circles:
        print('Circles {}'.format(circles))
    else:
        print('无环')

    molecularMap = buildMolecularMap(elements)
    startLayer = None
    if circles:
        molecularMap = setCircleNodesCoordinate(circles[0], molecularMap, topology)
        startLayer = circles[0]
    else:
        startNode = None
        for i, element in enumerate(elements):
            if element == 'C':
                startNode = i
                break
        molecularMap[startNode].setCoordinate(0, 0)
        secondNode = None
        for i, b in enumerate(topology[startNode]):
            if b: secondNode = i
        molecularMap[secondNode].setCoordinate(50, 0)
        molecularMap[startNode].connect(molecularMap[secondNode], 'up', topology)
        startLayer = [startNode, secondNode]

    molecularMap = setLinkNodesCoordinate(startLayer, molecularMap, topology, elements)
    draw(molecularMap, topology)

    #生成物
    outTopology, outelements = buildTopology(outFomularPath)
    outMolecularMap = copy.deepcopy(molecularMap)
    for i in range(len(outelements)):
        outMolecularMap[i].edges = []
        connects = [index for index, b in enumerate(outTopology[i]) if b]
        for connect in connects:
            if topology[i][connect] == outTopology[i][connect]:
                edges = molecularMap[i].edges
                direction = None
                for edge in edges:
                    if edge[0].ID == connect:
                        direction = edge[2]
                if direction:
                    outMolecularMap[i].connect(outMolecularMap[connect], direction, outTopology)
            elif topology[i][connect] > 0:
                outMolecularMap[i].connect(outMolecularMap[connect], 'up', outTopology)
            else:
                pass
    outMolecularMap1 = shiftMolecularMap(0, 0, 0, 0, outMolecularMap)
    draw(outMolecularMap1, outTopology)
    '''
    outMolecularMap2 = shiftMolecularMap(0, 0, 100, 0, outMolecularMap)
    draw(outMolecularMap2, outTopology)
    outMolecularMap3 = shiftMolecularMap(0, 0, 0,  -math.pi/3, outMolecularMap)
    draw(outMolecularMap3, outTopology)
    outMolecularMap4 = shiftMolecularMap(0, 100, 100, -math.pi/3, outMolecularMap)
    draw(outMolecularMap4, outTopology)
    '''


if __name__ == '__main__':
   drawReaction('arrayInputs/C7H6O3.txt', 'arrayInputs/C7H6O3Out2.txt')
