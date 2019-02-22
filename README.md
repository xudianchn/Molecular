# chemistryDraw



### utils 基础工具函数

```python
def buildTopology(path)
	'''
	读取连接矩阵路径，得到连接矩阵与元素顺序
	path: 连接矩阵文件路径 './arrayInputs/C13.txt'
	
	topology:连接矩阵(numpy)
	elements:元素顺序表, 如['H', 'C', 'O']
	'''
	return topology, elements
```

```python
class AdjGraph:
	'''
	中国连接矩阵建立连接表
	'''
	def addEdge（self, start, end）:
		#输入两个点序号，判断连通性并连接
    def buildGraph (self, topology):
        #topology:buildTopology得到的连通表
        #得到self.adjList即连通表
    def getAdjList (self):
        #外界访问接口
```

```python
class Graph():
	'''
	建立图，主要作用是找到所有的环
	'''
    def step(layer):
    	'''
        从该层的点找到连接到下层的点
        layer: 如[[1,2,3], [2,3,4]]
        连接下一层的时候，排除了向上层的回传(connectNodes.remove(li[-2]))
        '''
    def findCircles(self, start):
        '''
        找的所有的环，具体方法为从某个起始点开始，以0举例
        [[0]]
        0连1,2
        [[0,1]], [0,2]
        1连[0,2,3] 2连[0,1,4]
        [[0,1,2],[0,1,3],[0,2,1],[0,2,4]]
        下一层3,4无其他连接
        返回circles [[0,1,2,0], [0,2,1,0]]
        '''
        return circles
```

```python
def getCircles(topology):
    '''
    利用Graph的findCircles,返回环为无重复环(顺时针逆时针只取一)、较大环(边数大于3)
    '''
    return circles
```

```python
def splitCircles(circles, topology):
    '''
    将找到的circles进行拆分，拆成所有不重复的最小环
    若下图中，会有一个10点大环，该函数处理后只返回两小环
    '''
```

![1](C:\Users\lxd\Desktop\chemistryDraw\documents\1.png)

```python
def breakCircles(cleanCircles, topology):
    '''
    cleanCircles:最小不重复环
    将环拆开，并且环中添加上孤立点，如上图中10, 11
    特别的，环与环的连接线会别两个环的group都添加
    主要方法
    	1.将circles划分成已经设定的合没有设定的(othercircles)
    	2.构建临时的连接表
    	3.使用深度搜索优先算法得到包含孤立点的Group
    '''
    return Groups
	#如上图返回为[[0,1,2,3,4,5,11], [2,3,4,6,7,8,9,11]]
```

```python

```



### graphDraw 根据分析结果画图

```python
class chemistryDraw:
    '''
    根据连接情况与坐标关系进行画图
    '''
    def __init__(self):
        #设定基础图像为600*600大小
    
    def drawLine(self, x0, y0, x1, y1, typ, direction = None):
        #(x0, y0), (x1, y1)画线的起止点，typ为单线(single)，双键(double)，方向(仅在双键时起作用，设定是在直连线上还是下画一条短线)
        #这个做法开始是因为要画C环时，内部需要设定长短，后面不成环沿用了，实际需要区分这两种情况
        
    def show(self):
        #展示该图
        
if __name__ == '__main__':
    '''
    测试代码
    '''
    draw = chemistryDraw()
    draw.drawLine(0, 0, 50, 0, 'single')
    draw.drawLine(50, 0, 75, -43, 'double')
    draw.drawLine(75, -43, 75, -93, 'triple')
    draw.show()
```

> 实际使用时在这个函数基础上重新写了一个在groupDraw中写了一个Draw的类，扩充了其功能



### GroupDraw

```python
class AtomNode
	'''
	图上的基本单位，表示单个点，其具有ID,element, coordnate, edges等属性
	
	coordnate = [x, y, flag] flag是表示该坐标是否已经设定完成
	edges是一个保存edge的list
	edge: [AtomNode, 与当前锚点键数，方向]
	'''
    def connect(self, node, direction, topology):
        #建立当前锚点与某点的连接关系
```

### buildMolecularMap(elements):

```python
def buildMolecularMap(elements):
	'''
	初始化一个NodeMap, Map[Id] = AtomNode
	'''
    return molecularMap
```



### shiftMolecularMap

```python
def shiftMolecularMap(index, x, y, theta, molecularMap):
	'''
	将图旋转theta角度，将index的node设置到X,Y
	'''
    return molecularMap
```

>  这里只有转移函数，需要补充一个翻转函数



###setCircleNodesCoordinate

```python
def setCircleNodesCoordinate(circleNodes, molecularMap, topology):
    '''
    检测基准环后，设定基准环的坐标，其他点位置都为基准环递推
    '''
    return molecularMap
```



### setLinkNodesCoordinate

```python
def setLinkNodesCoordinate(startNodes, molecularMap, topolgy, elements):
    '''
    从基准环开始，层次式的递推坐标位置
    '''
    return molecularMap
```

> 该函数传入的molecularMap不是全图，而是切分后的group，这一步设定后需连接不同组，根据需要计算偏移量和旋转量



### getBreakTopology

```python
def getBreakTopology(topology, group):
    '''
    输入原始连接举证，将不在group中点的连接全部置0，即删除了其他线
    '''
    return topology
```



### getNodeCoordinatefromMaps

```python
def getNodeCoordinatefromMaps(molecularMaps, node):
    '''
    从所有map中，获得某个点设定好的坐标
   	molecularMaps是断开后的map组
    '''
    return x_base, y_base
```



### getCircleCenter

```python
def getCircleCenter(molecularMaps, circle):
    '''
    计算环的中心位置，用于判断不同环连接时需不需要翻转
    下图中需要将molecurlarMaps[1]翻转(改变时针顺序)
    '''
    return x, y
```

![2](C:\Users\lxd\Desktop\chemistryDraw\documents\2.png)



### getLinkNodes

```python
def getLinkNode(settledGroups, settleCircles, newGroup, newCircle, molecularMap, molecularMaps, topology):
    '''
    
    '''
    
    return nodeIndex, x_base, y_base, removeNodes
```

> 该函数作用是找到新group中需要删除的点，目前不是适用所有情况



### setGroupCoordinate:

```python
def setGroupCoordinate(circles, groups, elements, topology, molecurlarMap):
    '''
   	主画图程序
   	定好基准环后，递推式画出环和相应组
    '''
```



### drawGroup(originalFomularPath, outFomularPath)

```python
def drawGroup(originalFomularPath, outFomularPath):
    '''
    主入口程序
    '''
    
```

> 目前该程序没有处理反应物到产物的信息继承关系
>
> 信息继承关系在graphAnalyze中有简单的实现(没有考虑多环情况的)