import matplotlib.pyplot as plt
import math
import copy
import numpy as np
from utils import buildTopology


class chemistryDraw:

    def __init__(self):
        plt.figure(figsize=(6, 6))
        plt.xticks(())
        plt.yticks(())

        plt.xlim((-300, 300))
        plt.ylim((-300, 300))

    #typ是画线种类, single单线, double双键, triple三键
    #只有双键需要指定方向(第二键是在哪个方向画出,对于环必须正确指定)
    def drawLine(self, x0, y0, x1, y1, typ, direction=None):
        if typ == 'single':
            x = np.asarray([x0, x1])
            y = np.asarray([y0, y1])
            plt.plot(x, y, color='black')

        elif typ == 'double' :
            self.drawLine(x0, y0, x1, y1, 'single')

            #减短双键长度, 画第二条键
            theta = math.atan2((y1 - y0), (x1 - x0))
            x2 = x0 + 1/20 * (x1 - x0)
            y2 = y0 + 1/20 * (y1 - y0)
            x3 = x1 - 1/20 * (x1 - x0)
            y3 = y1 - 1/20 * (y1 - y0)

            if (direction == 'up' and x3>=x2) or (direction == 'down' and x3<x2):
                x2 = x2 - math.sin(theta) * 6
                x3 = x3 - math.sin(theta) * 6
                y2 = y2 + math.cos(theta) * 6
                y3 = y3 + math.cos(theta) * 6
            else:
                x2 = x2 + math.sin(theta) * 6
                x3 = x3 + math.sin(theta) * 6
                y2 = y2 - math.cos(theta) * 6
                y3 = y3 - math.cos(theta) * 6
            plt.plot([x2, x3], [y2, y3], color='black')
        elif typ == 'triple':
            self.drawLine(x0, y0, x1, y1, 'double', 'up')
            self.drawLine(x0, y0, x1, y1, 'double', 'down')



    def show(self):
        plt.show()

if __name__ == '__main__':
    draw = chemistryDraw()
    draw.drawLine(0, 0, 50, 0, 'single')
    draw.drawLine(50, 0, 75, -43, 'double')
    draw.drawLine(75, -43, 75, -93, 'triple')
    draw.show()