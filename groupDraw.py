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

    # "edge指的是什么"
    #Edge指连接的边，不用管叫什么，要弄清楚edge里面包含的是什么:连接的Node，键数，方向(二键有用)
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

def setCircleNodesCoordinate(circleNodes, molecularMap, topology, shiftangel):
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
            print(circleNodes)
            if shiftangel == math.pi:
                if i < 3:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'down', topology)
                else:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'up', topology)

            elif shiftangel == math.pi*7/6:
                if i < 3 or i > 4:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'down', topology)
                else:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'up', topology)

            elif shiftangel == math.pi*2/3:
                if i < 2 or i > 4:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'down', topology)
                else:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'up', topology)

            elif shiftangel == math.pi*5/6:
                if i < 3 or i > 4:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'down', topology)
                else:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'up', topology)

            elif shiftangel == math.pi/3:
                if i < 1 or i > 3:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'down', topology)
                else:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'up', topology)

            elif shiftangel == math.pi/2:
                if i < 3 or i > 4:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'down', topology)
                else:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'up', topology)

            elif shiftangel == 0:
                if i < 3:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'up', topology)
                else:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'down', topology)

            elif shiftangel == math.pi/6:
                if i < 3 or i > 4:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'down', topology)
                else:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'up', topology)

            elif shiftangel == -math.pi/3:
                if i < 2 or i > 4:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'up', topology)
                else:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'down', topology)

            elif shiftangel == -math.pi/6:
                if i < 3 or i > 4:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'down', topology)
                else:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'up', topology)

            elif shiftangel == -math.pi*2/3:
                if i < 1 or i > 3:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'up', topology)
                else:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'down', topology)

            elif shiftangel == -math.pi/2:
                if i < 3 or i > 4:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'down', topology)
                else:
                    molecularMap[node].connect(molecularMap[circleNodes[i + 1]], 'up', topology)

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
            # "这两个判断指的是什么，checkednodes，nextLayerNodeIndex指的是什么"
            #检测过的点，下一层中点标号(对应txt中的顺序)
            #你应该看checkedNodes是什么时候生成的，什么时候变化的，就知道它的作用是干嘛了
            #checkedNodes被放入了settleNodes，即坐标已经定位好的点集，为定位的点依靠定位好的点定位，所以要做这个区分

            print('\nCurrent Node {} {} {}'.format(nodeID, nodeElement, nodeCoord))
            print('SettleNodes {}  FreeNodes {}'.format(settleNodes, freeNodes))

            if len(freeNodes) == 1 and layerIndex == 0:
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
            elif len(freeNodes) == 1 and layerIndex != 0:
                x1 = 0
                y1 = 0
                for node2 in settleNodes:
                    x1 += molecularMap[node2[0]].coordinate[0]
                    y1 += molecularMap[node2[0]].coordinate[1]
                x1 = x1 / len(settleNodes)
                y1 = y1 / len(settleNodes)
                theta = math.atan2((y1 - y0), (x1 - x0)) + math.pi

                x3_tar = x0 + math.cos(theta + math.pi / 3) * 50
                y3_tar = y0 + math.sin(theta + math.pi / 3) * 50

                molecularMap[freeNodes[0][0]].setCoordinate(x3_tar, y3_tar)
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

                if freeNodes[0][1] == 'C':
                    freeNodes[0], freeNodes[1] = freeNodes[1], freeNodes[0]

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
            elif len(freeNodes) == 3:
                x1 = 0
                y1 = 0
                for node2 in settleNodes:
                    x1 += molecularMap[node2[0]].coordinate[0]
                    y1 += molecularMap[node2[0]].coordinate[1]
                x1 = x1 / len(settleNodes)
                y1 = y1 / len(settleNodes)
                theta = math.atan2((y1 - y0), (x1 - x0)) + math.pi

                x4_tar = x0 + math.cos(theta - math.pi / 2) * 50
                y4_tar = y0 + math.sin(theta - math.pi / 2) * 50
                molecularMap[freeNodes[0][0]].setCoordinate(x4_tar, y4_tar)
                molecularMap[node].connect(molecularMap[freeNodes[0][0]], 'up', topology)

                x5_tar = x0 + math.cos(theta) * 50
                y5_tar = y0 + math.sin(theta) * 50
                molecularMap[freeNodes[1][0]].setCoordinate(x5_tar, y5_tar)
                molecularMap[node].connect(molecularMap[freeNodes[1][0]], 'up', topology)

                x6_tar = x0 + math.cos(theta + math.pi / 2) * 50
                y6_tar = y0 + math.sin(theta + math.pi / 2) * 50
                molecularMap[freeNodes[2][0]].setCoordinate(x6_tar, y6_tar)
                molecularMap[node].connect(molecularMap[freeNodes[2][0]], 'up', topology)

                nextLayerNodes.append(freeNodes[0][0])
                nextLayerNodes.append(freeNodes[1][0])
                nextLayerNodes.append(freeNodes[2][0])

        print('nextLayerNodes {}'.format(nextLayerNodes))
        layerNodes = nextLayerNodes
        if layerNodes not in layers:
            layers.append(layerNodes)
        layerIndex += 1

    return molecularMap

class Draw():
    def __init__(self):
        pass
        self.dr = chemistryDraw()

    def draw(self, molecularMap, group, info = None):
        dire = ['single', 'double', 'triple']

        for t in range(len(group)):
            i = group[t]
            start = (molecularMap[i].coordinate[0], molecularMap[i].coordinate[1])

            startElement = molecularMap[i].element
            if startElement != 'C':
                plt.text(start[0] - 7, start[1] - 7, startElement)

            plt.text(start[0] + 3, start[1] + 3, i)

            for edge in molecularMap[i].edges:
                endElement = edge[0].element
                # if endElement == 'H' and startElement == 'C':
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
    for node in circle[:-1]:
        x += molecularMap[node].coordinate[0]
        y += molecularMap[node].coordinate[1]


    x = x/(len(circle)-1)
    y = y/(len(circle)-1)
    return x, y


def getLinkNode(settledGroups, settleCircles, newGroup, newCircle, molecularMap, molecularMaps, topology, circles):
    nodeIndex = 0
    x_base = 0
    y_base = 0
    connectCircle = None
    # "这个函数的作用"
    #找不同Groups间的连接线(group可能有重复部分)，为枝或者环上的点
    cir_cirNodes, cir_groupNodes, indirectNodes = getGroupRepeatLine(settleCircles, settledGroups, newCircle, newGroup)
    removeNodes = indirectNodes

    if len(cir_groupNodes) == 1:
        #找连接线，删除新circle中与已设定重复部分
        linkNode = cir_groupNodes[0]

        x_base, y_base = getNodeCoordinatefromMaps(molecularMaps, linkNode)

    if len(cir_cirNodes) == 2:

        for circle in circles:
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

        x_base = x2
        y_base = y2
    print(x_base)
    print(y_base)
    print('settleGroup {}'.format(settledGroups))
    print('cir_cirLinkNodes {}'.format(cir_cirNodes))
    print('cir_groupLinkNodes {}'.format(cir_groupNodes))
    print('indirectConnectNodes {}'.format(indirectNodes))
    return nodeIndex, x_base, y_base, removeNodes, connectCircle, cir_cirNodes, cir_groupNodes


def setGroupsCoordinate(circles, groups, elements, topology, molecularMap):
    if not circles:
        raise ('No circles')

    print('\n开始设定环组的坐标')

    dr = Draw()
    settledNodes = []
    molecularMaps = []
    settledCircles = []
    createcoordinate = []
    shiftangel = math.pi
    signtimes = []
    # 记录更改双环连接处的双键是否触发
    count = 0

    for circle, group in zip(circles, groups):
        mole_temp = copy.deepcopy(molecularMap)
        nodeIndex, x_base, y_base, removeNodes, connectCircle, cir_cirNodes, cir_groupnodes = getLinkNode(settledNodes, settledCircles, group, circle, molecularMap, molecularMaps,topology,circles)
        for removeNode in removeNodes:
            group.remove(removeNode)
        print('\t设定环 {} 组 {}'.format(circle, group))
        topo_temp = getBreakTopology(topology, group)
        if connectCircle != None:
            if circle[0] not in connectCircle or circle[1] not in connectCircle:
                circle.reverse()

        index = circle[0]

        sign = 0

        if len(molecularMaps) > 0 and len(cir_groupnodes) > 0:
            for i in range(len(molecularMaps[count-1])):
                if len(molecularMaps[count-1][i].edges):
                    for j in range(len(molecularMaps[count-1][i].edges)):
                        if molecularMaps[count-1][i].edges[j][0].ID == cir_groupnodes[0] or molecularMaps[count-1][i].edges[j][0].ID == cir_groupnodes[0]:
                            connectnodes = i

                            x21 = molecularMaps[count - 1][connectnodes].coordinate[0]
                            y21 = molecularMaps[count - 1][connectnodes].coordinate[1]

                            x22 = molecularMaps[count-1][cir_groupnodes[0]].coordinate[0]
                            y22 = molecularMaps[count-1][cir_groupnodes[0]].coordinate[1]

                            shiftangel = math.atan2((y21-y22), (x21-x22))

        mole_temp = setCircleNodesCoordinate(circle, mole_temp, topo_temp, shiftangel)
        mole_temp = setLinkNodesCoordinate(circle, mole_temp, topo_temp, elements)

        if count == 0:
            mole_temp = shiftMolecularMap(index, x_base, y_base, 0, mole_temp)
        if count > 0:
            mole_temp = shiftMolecularMap(index, x_base, y_base, shiftangel - math.pi, mole_temp)

        if connectCircle != None:
            for i in range(len(cir_cirNodes)):
                for j in range(len(mole_temp[cir_cirNodes[i]].edges)):
                    if mole_temp[cir_cirNodes[i]].edges[j][1] == 2.0 and mole_temp[cir_cirNodes[i]].edges[j][0].ID in cir_cirNodes:
                        mole_temp[cir_cirNodes[i]].edges[j][1] = 1.0
                        sign = count

        settledNodes += group
        settledCircles += circle
        molecularMaps.append(mole_temp)
        createcoordinate.append([x_base, y_base])
        if len(cir_cirNodes) != 0:
            signtimes.append([sign, cir_cirNodes[0], cir_cirNodes[1]])
        dr.draw(mole_temp, group)
        count += 1
    dr.show()
    return molecularMaps, createcoordinate, signtimes

def drawGroup(originalFomularPath, outFomularPath):
    # 反应物
    topology, elements = buildTopology(originalFomularPath)
    circles = getCircles(topology)
    cleanCircles = splitCircles(circles, topology)
    groups = breakCircles(cleanCircles, topology)
    molecularMap = buildMolecularMap(elements)
    molecularMaps, createcoordinate, signtimes = setGroupsCoordinate(cleanCircles, groups, elements, topology, molecularMap)

    dr = Draw()

    # 生成物
    outTopology, outelements = buildTopology(outFomularPath)
    count = 0
    for a in range(len(molecularMaps)):
        outMolecularMap = copy.deepcopy(molecularMaps[a])
        for i in range(len(outelements)):
            outMolecularMap[i].edges = []
            connects = [index for index, b in enumerate(outTopology[i]) if b]
            for connect in connects:
                if topology[i][connect] == outTopology[i][connect]:
                    edges = molecularMaps[a][i].edges
                    direction = None
                    for edge in edges:
                        if edge[0].ID == connect:
                            direction = edge[2]
                    if len(signtimes) != 0:
                        for times in range(len(signtimes)):
                            if signtimes[times][0] == count:
                                if outTopology[signtimes[times][2]][signtimes[times][1]] != 0:
                                    outTopology[signtimes[times][2]][signtimes[times][1]] = 1
                                else:
                                    outTopology[signtimes[times][1]][signtimes[times][2]] = 1
                    if direction:
                        outMolecularMap[i].connect(outMolecularMap[connect], direction, outTopology)
                elif topology[i][connect] > 0 and connect in groups[a]:
                    outMolecularMap[i].connect(outMolecularMap[connect], 'up', outTopology)
                else:
                    pass
        outMolecularMap1 = shiftMolecularMap(0, createcoordinate[a][0], createcoordinate[a][1], 0, outMolecularMap)
        dr.draw(outMolecularMap1, groups[a])

        count +=1
    dr.show()

if __name__ == '__main__':
    drawGroup('arrayInputs/JIANG.txt', 'arrayInputs/JIANG1.txt')