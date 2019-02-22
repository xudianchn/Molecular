import numpy as np
import copy

global Connect
global Atom_num
global Txt

"""
写出字典格式，类似1:C 2:O 查询
"""
Atom_temp = []
f = open("C7H6O3.txt")
line = f.readline()
while line:
    s = line[:1]
    for line in s:
        Atom_temp.append(s)
    line = f.readline()
Atom = Atom_temp[2:-1]
n = len(Atom)
Num = list(range(1, n))
Atom_num = dict(zip(Num, Atom))
f.close()

"""
从txt中读取二维数组
"""
Connect_temp = []
f = open("C7H6O3.txt")
line = f.readline()
while line:
    t = line[3:-2]
    t_array = list(t)
    for i in t_array:
        if ' ' in t_array:
            t_array.remove(' ')

    for i in t_array:
        if ',' in t_array:
            t_array.remove(',')
    Connect_temp.append(t_array)
    Connect = Connect_temp[2:-1]
    line = f.readline()
Connect = np.array(Connect)
f.close()

Txt = []
f = open("C7H6O3.txt")
line = f.readline()
while line:
    line = line.strip()
    line = list(line)
    Txt.append(line)
    line = f.readline()
f.close()


class atom_link:
    def __init__(self, mid, link = None, alpha_pos = None,Tx = None):
        self.mid = mid
        self.link = []
        self.alpha_pos = []
        self.Tx = []

    def mid_link(self):
        for col in range(n):
            if int(Connect[self.mid-1, col]):
                self.link.append([self.mid, col+1])
        for row in range(n):
            if int(Connect[row, self.mid-1]):
                self.link.append([self.mid, row+1])
        print(self.link)

    def alpha(self):
        for num in range(len(self.link)):
            for col in range(n):
                if int(Connect[self.link[num][1]-1, col]) == 1 and col != self.mid-1:
                    self.alpha_pos.append([self.link[num][1], col+1])
            for row in range(n):
                if int(Connect[row, self.link[num][1]-1]) == 1 and row != self.mid-1:
                    self.alpha_pos.append([self.link[num][1], row+1])
        print(self.alpha_pos)

    def product(self):
        for num in range(len(self.alpha_pos)):
            Txtnum = copy.deepcopy(Txt)
            a = 0
            for col in range(len(self.link)):
                if int(Connect[self.link[col][0]-1, self.link[col][1]-1]) == 2 and a < 1:
                    Txtnum[self.link[col][0]+1][(self.link[col][1]-1) * 3+3] = '1'
                    a = a+1
            for row in range(len(self.link)):
                if int(Connect[self.link[row][1]-1, self.link[row][0]-1]) == 2 and a < 1:
                    Txtnum[self.link[row][0]+1][(self.link[row][1]-1) * 3+3] = '1'
                    a = a+1

            if self.alpha_pos[num][0] <= self.alpha_pos[num][1]:
                Txtnum[self.alpha_pos[num][0] + 1][(self.alpha_pos[num][1]-1) * 3 + 3] = '0'
            else:
                Txtnum[self.alpha_pos[num][1] + 1][(self.alpha_pos[num][0]-1) * 3 + 3] = '0'

            if self.alpha_pos[num][0] <= self.mid:
                Txtnum[self.alpha_pos[num][0] + 1][(self.mid-1) * 3 + 3] = '2'
            else:
                Txtnum[self.mid+1][(self.alpha_pos[num][0]-1) * 3 + 3] = '2'
            for m in Txtnum:
                m = ''.join(m)
                print(m)
            print()



mid1 = atom_link(11)
mid1.mid_link()
mid1.alpha()
mid1.product()

# Mid = [2, 5]
# for num in range(len(Mid)):
#     Midnum = Atom_link(Mid[num])
#     Midnum.midlink()


# if __name__ == '__main__':



















