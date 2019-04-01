import numpy as np
#=============求文件总行数=================#
filename = "TANG.LOG"
myfile = open(filename) 
lines = len(myfile.readlines()) 
print (filename)
print('\n')

if filename == "TANG.LOG":
    break1 = 1
elif filename == "JIANG-2.LOG":
    break1 = 2
#=============定义变量数组=================#
m=0
n=200
a=0
b=0
c='1'
d=0
e=0
f=0
g='1'
i=0
j=0
q=0
p=0
s="Molecular unit  1"
str1 = "Natural Electron Configuration"
str3 = "Number     Number       Type             X           Y           Z"
str4 = 'Symbolic Z-matrix:'
str5 = "Atom  No    Charge         Core      Valence    Rydberg      Total"
A = []
B = []
B = []
D = []
E = []
F = []
G = []
#=============求原子数目=================#
myfile = open(filename)
line = myfile.readline()
while line:
    if str5 in line:

        for i in range(80):
            line = myfile.readline()
            for i in range(0,len(line),1):
                list4 = []
                for word in line.split():
                    word = word.strip()
                    list4.append(word)
            if g in list4:
                g = int(g)+1
                g = str(g)
                F.append(int(list4[1]))
                F.sort(reverse=True)
    
    
    if not line:break

    line=myfile.readline()
line = myfile.readline()
#print(F[0])
m = F[0]

#=============求正电荷中心=================#
myfile = open(filename)
line = myfile.readline()
while line:
    if str5 in line:

        for i in range(m+2):
            line = myfile.readline()
            for i in range(0,len(line),1):
                list3 = []
                for word in line.split():
                    word = word.strip()
                    list3.append(word)
            if c in list3:
                c = int(c)+1
                c = str(c) 
                
                if 'H' in list3:
                    continue


                E.append(float(list3[2]))
                E.sort(reverse=True)
                b = str(E[0])
                if b in list3:
                    d = list3[0]
                    e = list3[1]
                    
    if not line:break

    line=myfile.readline()
line = myfile.readline()
#print(d,e,E[0],E[1],E[2])

###############try求前几个正电荷中心#####################
mid_temp = []
mid_temp1 = []
mid_temp2 = []
mid_temp3 = []
myfile = open(filename)
line = myfile.readline()
while line:
    if str5 in line:    
        for i in range(m+1):
            line = myfile.readline()
            for i in range(0,len(line),1):
                list6 = []
                for word in line.split():
                    word = word.strip()
                    list6.append(word)                                        
            mid_temp.append(list6)       
        break
    line=myfile.readline()
line = myfile.readline()

for i in range(1,m+1):
    mid_temp1.append(mid_temp[i]) 
    
mid_temp1.sort(key=lambda x:x[2]) 

mid_temp2 = mid_temp1[-10:]  #-6
mid_temp2.sort(reverse=True)
mid_temp2 = np.array(mid_temp2)
mid_temp2 = mid_temp2[:,:3]  #3
mid_temp2 = mid_temp2.tolist()
i = 0
for i in range(10):
    if mid_temp2[i][0] == 'H':

        continue
    mid_temp3.append(mid_temp2[i])
#print(mid_temp3)

#=============求化学式名称=================#
myfile = open(filename)
line = myfile.readline()
while line:
    if s in line:
        for i in range(0,len(line),1):
            list2 = []
            for word in line.split():
                word = word.strip()
                list2.append(word)

        if not line:break

    line=myfile.readline()
    
line = myfile.readline()
str2 =list2[3] 
#print(str2[1:-1])

#=============成键与矩阵对应关系=================#
C = [[0 for i in range(m)] for j in range(m)]
myfile = open(filename)
line = myfile.readline()
while line:
    if s in line:

        for i in range(n):
            line = myfile.readline()
            for i in range(0,len(line),1):
                list5 = []
                for word in line.split():
                    word = word.strip()
                    list5.append(word)
                    
                if 'BD' in list5:
                    i = int(list5[5])
                    j = int(list5[8])
                    if '1)' in list5:
                        C [i-1][j-1] = 1
                    elif '2)' in list5:
                        C [i-1][j-1] = 2
                    elif '3)' in list5:
                        C [i-1][j-1] = 3
                    elif '4)' in list5:
                        C [i-1][j-1] = 4
                    else:
                        C [i-1][j-1] = 0

                else:
                    continue

        if not line:break

    line=myfile.readline()
    
line = myfile.readline()

   
#=============输出各个原子=================#
myfile = open(filename)
line = myfile.readline()
while line:
    if str1 in line:

        for i in range(m+1):
            line = myfile.readline()
            for i in range(0,len(line),1):
                list1 = []
                for word in line.split():
                    word = word.strip()
                    list1.append(word)                                
            D.append(list1[0])
        if not line:break
    line=myfile.readline()
line = myfile.readline()
for i in range(0,m):
    #print(str(D[i+1]))
    A.append(D[i+1])
#print(A)


###########判断S元素是否在里面###########
if 'S' in A:
    S_num = A.index('S')
    print(S_num)

    for abc in range(S_num,m):
        if int(C[S_num][abc]):
            if A[abc] == 'O':
                C[S_num][abc] = 2
    for cde in range(0,S_num):
        if int(C[cde][S_num]):
            if A[cde] == 'O':
                C[cde][S_num] = 2

#while a < m:
#
#    print(C[a])
#    a = a+1

#=============输出txt=================#
with open("out1.txt", "w") as f:
        f.write("start")
        f.write("\n")
        f.write(str2[1:-1])
        f.write("\n")
        for i in range(0,m):
            f.write(str(D[i+1]))
            f.write(';')
            f.write(str(C[i]))
            f.write("\n")
        f.write("end")
        f.write("\n")
        f.write(d)
        f.write("，")
        f.write(e)
        f.write("\n")
        f.close()
        

################################裂解################################
################################裂解################################
import numpy as np
import copy

global Connect
global Atom_num
global Txt

"""
写出字典格式，类似1:C 2:O 查询
"""
filename = "out1.txt"
Atom_temp = []
f = open(filename)
line = f.readline()
while line:
    s = line[:1]
    for line in s:
        Atom_temp.append(s)
    line = f.readline()
Atom = Atom_temp[2:-2]
n = len(Atom)
Num = list(range(1, n+1))
Atom_num = dict(zip(Num, Atom))
f.close()
#print(n)
#print(Atom_num)

"""
从txt中读取二维数组
"""
Connect_temp = []
f = open(filename)
line = f.readline()
while line:
    t = line[3:-2]
    t_array = list(t)
        
    for i in t_array:
        if ' ' in t_array:
            t_array.remove(' ')

    for j in t_array:
        if ',' in t_array:
            t_array.remove(',')
     
    Connect_temp.append(t_array)
    Connect = Connect_temp[2:-2]
    
    line = f.readline()
Connect = np.array(Connect)

f.close()

##############################正电荷中心##############################
f = open(filename)
lines = f.readlines()
last_line = lines[-1]
if last_line[3] != '\n':
    middd = (int(last_line[2]))*10+int(last_line[3])
else:
    middd =int(last_line[2])
#print(middd)
f.close()


#####################################################################
#####################################################################
Txt = []
f = open(filename)
line = f.readline()
while line:
    line = line.strip()
    line = list(line)
    Txt.append(line)
    line = f.readline()
f.close()


Txtnum = copy.deepcopy(Txt)
list1 = []
list2 = []
list3 = []
Connect_new = []
b = 0
num = 0
listabc = []
###################################开始表演###########################################




#############################类########################################
class atom_link:
    def __init__(self, mid, num, b,link = None, alpha_pos = None,Tx = None):
        self.mid = mid
        self.num = num  #
        self.b = b
        self.link = []
        self.alpha_pos = []
        self.Tx = []
        

    def mid_link(self):#正电荷中心原子和哪几个原子相连 mid=#
        for col in range(n):
            if int(Connect[self.mid-1, col]):
                self.link.append([self.mid, col+1])
                list3.append([self.mid, col+1])
        for row in range(n):
            if int(Connect[row, self.mid-1]):
                self.link.append([self.mid, row+1])
                list3.append([self.mid, row+1])
#        print(self.link)
    
    def alpha(self):#断中心原子旁边隔一个的α位的单键#
        for num in range(len(self.link)):
            for col in range(n):
                if int(Connect[self.link[num][1]-1, col]) == 1 and col != self.mid-1:
                    self.alpha_pos.append([self.link[num][1], col+1])
            for row in range(n):
                if int(Connect[row, self.link[num][1]-1]) == 1 and row != self.mid-1:
                    self.alpha_pos.append([self.link[num][1], row+1])
#        print(self.alpha_pos)


############################分子裂解###############################
    def mole_break(self):

        a = 0
        Txtnum = copy.deepcopy(Txt)
        ##JIANG 第一个B裂解##
        if self.mid==14 and self.num ==3:
            Txtnum[12][(11) * 3 + 3] = '0'  #第一个加一 第二个减一
            Txtnum[15][(26) * 3 + 3] = '1'
            Txtnum[13][(14) * 3 + 3] = '1'
            Txtnum[16][(16) * 3 + 3] = '0'
            Txtnum[13][(13) * 3 + 3] = '2'
            Txtnum[13][(12) * 3 + 3] = '0'
            
            for m in Txtnum:
                m = ''.join(m)
                print(m)
                
        #######JIANG 第二个A#######
        elif self.mid==14 and self.b ==0:
            Txtnum[15][(26) * 3 + 3] = '1'  #第一个加一 第二个减一
            Txtnum[12][(11) * 3 + 3] = '0'
            Txtnum[3][(10) * 3 + 3] = '0'
            Txtnum[13][(12) * 3 + 3] = '0'
            Txtnum[3][(11) * 3 + 3] = '1'
            Txtnum[13][(13) * 3 + 3] = '2'
            Txtnum[2][(6) * 3 + 3] = '0'
            Txtnum[16][(16) * 3 + 3] = '0'
            Txtnum[2][(14) * 3 + 3] = '1'
            
            for m in Txtnum:
                m = ''.join(m)
                print(m)
                
        ############JIANG 第二个B#############
        elif self.mid==14 and self.b ==1:
            Txtnum[15][(26) * 3 + 3] = '0'  #第一个加一 第二个减一
            Txtnum[15][(14) * 3 + 3] = '0'

            Txtnum[16][(26) * 3 + 3] = '1'
            Txtnum[3][(10) * 3 + 3] = '0'
            Txtnum[16][(16) * 3 + 3] = '0'
            Txtnum[3][(14) * 3 + 3] = '1'

            
            for m in Txtnum:
                m = ''.join(m)
                print(m)
        
        ###############JIANG D 加羟基#################
        elif self.mid == 11 and self.b == 0:
            Txtnum[13][(13) * 3 + 3] = '0'
            Txtnum[13][0] = 'O' #羟基#
            Txtnum[12][(28) * 3 + 3] = '1'
            Txtnum[13][(12) * 3 + 3] = '0'
            Txtnum[12][(11) * 3 + 3] = '2'
            
            for m in Txtnum:
                m = ''.join(m)
                print(m)
        
        
        else:
            
            
            for col in range(len(self.link)):
                if int(Connect[self.link[col][0]-1, self.link[col][1]-1]) == 2 and a < 1:
                    Txtnum[self.link[col][0]+1][(self.link[col][1]-1) * 3+3] = '1'
                    a = a+1
            for row in range(len(self.link)):
                if int(Connect[self.link[row][1]-1, self.link[row][0]-1]) == 2 and a < 1:
                    Txtnum[self.link[row][1]+1][(self.link[row][0]-1) * 3+3] = '1'
                    a = a+1
            
            
            if self.alpha_pos[self.num][0] <= self.alpha_pos[self.num][1]:
                Txtnum[self.alpha_pos[self.num][0] + 1][(self.alpha_pos[self.num][1]-1) * 3 + 3] = '0'
            else:
                Txtnum[self.alpha_pos[self.num][1] + 1][(self.alpha_pos[self.num][0]-1) * 3 + 3] = '0'
            
            if self.alpha_pos[self.num][0] <= self.mid:
                Txtnum[self.alpha_pos[self.num][0] + 1][(self.mid-1) * 3 + 3] = '2'
                
            else:
                Txtnum[self.mid+1][(self.alpha_pos[self.num][0]-1) * 3 + 3] = '2'
    
    
            for m in Txtnum:
                m = ''.join(m)
                print(m)

##################################################
    #Txtnum = copy.deepcopy(Txt)
    def product(self):
#       for num in range(len(self.alpha_pos)):
#            Txtnum = copy.deepcopy(Txt)
#            num = 2
            a = 0

            
            ##JIANG 第一个A S的裂解##
            if self.mid==11 and self.num ==0:
                Txtnum[12][(28) * 3 + 3] = '1'  #第一个加一 第二个减一
                Txtnum[3][(10) * 3 + 3] = '0'
                
                for m in Txtnum:
                    m = ''.join(m)
                    print(m)
            
            
            
            #############TANG c##############
            elif self.mid ==12 and self.num ==3:
                ##第一步##
                Txtnum[12][(11) * 3 + 3] = '1'  #第一个加一 第二个减一
                Txtnum[31][(32) * 3 + 3] = '0'

                #第二步##
                Txtnum[3][(2) * 3 + 3] = '1'
                Txtnum[3][(29) * 3 + 3] = '1'
                Txtnum[12][(22) * 3 + 3] = '0'  #第一个加一 第二个减一
                ##第三步
                Txtnum[4][(10) * 3 + 3] = '2'
                Txtnum[31][(30) * 3 + 3] = '0'
                Txtnum[3][(29) * 3 + 3] = '1'
                ##第四步
                Txtnum[3][(7) * 3 + 3] = '0'
                Txtnum[3][(29) * 3 + 3] = '2'
                
                for m in Txtnum:
                    m = ''.join(m)
                    print(m)
                    

                
            ###########################
            
            else:
            
                for col in range(len(self.link)):
                    if int(Connect[self.link[col][0]-1, self.link[col][1]-1]) == 2 and a < 1:
#                        Connect[self.link[col][0]-1, self.link[col][1]-1] = '1'
                        Txtnum[self.link[col][0]+1][(self.link[col][1]-1) * 3+3] = '1'
                        a = a+1
                for row in range(len(self.link)):
                    if int(Connect[self.link[row][1]-1, self.link[row][0]-1]) == 2 and a < 1:
#                        Connect[self.link[row][1]-1, self.link[row][0]-1] = '1'
                        Txtnum[self.link[row][1]+1][(self.link[row][0]-1) * 3+3] = '1'
                        a = a+1
    
                if self.alpha_pos[self.num][0] <= self.alpha_pos[self.num][1]:
                    Txtnum[self.alpha_pos[self.num][0] + 1][(self.alpha_pos[self.num][1]-1) * 3 + 3] = '0'
#                    Connect[self.alpha_pos[self.num][0]-1, self.alpha_pos[self.num][1]-1] = '0'
                else:
                    Txtnum[self.alpha_pos[self.num][1] + 1][(self.alpha_pos[self.num][0]-1) * 3 + 3] = '0'
#                    Connect[self.alpha_pos[self.num][1]-1, self.alpha_pos[self.num][0]-1] = '0'
    
                if self.alpha_pos[self.num][0] <= self.mid:
                    Txtnum[self.alpha_pos[self.num][0] + 1][(self.mid-1) * 3 + 3] = '2'
#                    Connect[self.alpha_pos[self.num][0]-1, self.mid-1] = '2'
                    
                else:
                    Txtnum[self.mid+1][(self.alpha_pos[self.num][0]-1) * 3 + 3] = '2'
#                    Connect[self.mid-1, self.alpha_pos[self.num][0]-1] = '2'


                if self.mid == 12 and self.b == 0:
                    Txtnum[3][(2) * 3 + 3] = '1'
                    Txtnum[3][(29) * 3 + 3] = '1'

            
                for m in Txtnum:
                    m = ''.join(m)
                    print(m)


###############CONNECT不变####################
    def product_new(self): ##TANG B
#        for num in range(1,len(self.alpha_pos)):
            Txtnum = copy.deepcopy(Txt)
#            num = 2
            a = 0
            for col in range(len(self.link)):
                if int(Connect[self.link[col][0]-1, self.link[col][1]-1]) == 2 and a < 1:
                    Txtnum[self.link[col][0]+1][(self.link[col][1]-1) * 3+3] = '1'
                    a = a+1
            for row in range(len(self.link)):
                if int(Connect[self.link[row][1]-1, self.link[row][0]-1]) == 2 and a < 1:
                    Txtnum[self.link[row][1]+1][(self.link[row][0]-1) * 3+3] = '1'
                    a = a+1

            if self.alpha_pos[self.num][0] <= self.alpha_pos[self.num][1]:
                Txtnum[self.alpha_pos[self.num][0] + 1][(self.alpha_pos[self.num][1]-1) * 3 + 3] = '0'
            else:
                Txtnum[self.alpha_pos[self.num][1] + 1][(self.alpha_pos[self.num][0]-1) * 3 + 3] = '0'
            
            
            
#            if Atom_num[self.link[0][1]] == 'C':
#                if Atom_num[33]=='C' and Atom_num[34]=='H':
            if self.mid == 12 and self.b == 0: ##TANG B
                Txtnum[34][(33) * 3 + 3] = '0'  #第一个加一 第二个减一
                Txtnum[31][(32) * 3 + 3] = '2'
                Txtnum[12][(22) * 3 + 3] = '0'
                Txtnum[12][(11) * 3 + 3] = '2'
            elif self.mid == 12 and self.b == 1:
                Txtnum[34][(33) * 3 + 3] = '0'  #第一个加一 第二个减一
                Txtnum[31][(32) * 3 + 3] = '2'
                Txtnum[24][(25) * 3 + 3] = '0'
                Txtnum[12][(22) * 3 + 3] = '2'
                



#            if self.alpha_pos[self.num][0] <= self.mid:
#                Txtnum[self.alpha_pos[self.num][0] + 1][(self.mid-1) * 3 + 3] = '2'
#                
#            else:
#                Txtnum[self.mid+1][(self.alpha_pos[self.num][0]-1) * 3 + 3] = '2'


            for m in Txtnum:
                m = ''.join(m)
                print(m)
                
################################################################
    
    def mole_break1(self):##TANG C
        Txtnum = copy.deepcopy(Txt)
        a = 0
            
        for col in range(len(self.link)):
            if int(Connect[self.link[col][0]-1, self.link[col][1]-1]) == 2 and a < 1:
                Txtnum[self.link[col][0]+1][(self.link[col][1]-1) * 3+3] = '1'
                a = a+1
        for row in range(len(self.link)):
            if int(Connect[self.link[row][1]-1, self.link[row][0]-1]) == 2 and a < 1:
                Txtnum[self.link[row][1]+1][(self.link[row][0]-1) * 3+3] = '1'
                a = a+1
        
        
        if self.alpha_pos[self.num][0] <= self.alpha_pos[self.num][1]:
            Txtnum[self.alpha_pos[self.num][0] + 1][(self.alpha_pos[self.num][1]-1) * 3 + 3] = '0'
        else:
            Txtnum[self.alpha_pos[self.num][1] + 1][(self.alpha_pos[self.num][0]-1) * 3 + 3] = '0'
        
        ######TANG D 1#############
        if self.mid ==11 and self.b == 0:
            Txtnum[16][(18) * 3 + 3] = '0'  #第一个加一 第二个减一
            Txtnum[13][(14) * 3 + 3] = '1'
            
        for m in Txtnum:
            m = ''.join(m)
            print(m)
        
        ######TANG D 2#############
#            elif self.mid ==12 and self.num ==4:
        Txtnum[12][(22) * 3 + 3] = '0'
        Txtnum[5][(8) * 3 + 3] = '0'  
        Txtnum[5][(10) * 3 + 3] = '1'
            

        ############################


        for m in Txtnum:
            m = ''.join(m)
            print(m)

                    
########################################类结束#############################################3
if break1 == 1:
    print('A:一种情况')
    Atom_link = atom_link(20,0,None,None,None) ### TANG A#
    Atom_link.mid_link()
    Atom_link.alpha()
    Atom_link.product()
    print('\n')
    #
    print('B:两种情况')
    Atom_link = atom_link(12,2,0,None,None,None) ### TANG B两个#
    Atom_link.mid_link()
    Atom_link.alpha()
    Atom_link.product_new()
    Atom_link = atom_link(12,2,1,None,None,None)
    Atom_link.mid_link()
    Atom_link.alpha()
    Atom_link.product_new()
    print('\n')
    #
    #
    print('C:一种情况')
    Atom_link = atom_link(12,3,0,None,None,None) ### TANG C#
    Atom_link.mid_link()
    Atom_link.alpha()
    Atom_link.product()
    print('\n')
    #Atom_link = atom_link(3,2,None,None,None)  ####暂时不需要调用这么多
    #Atom_link.mid_link()
    #Atom_link.alpha()
    #Atom_link.product()
    #Atom_link = atom_link(12,1,None,None,None) 
    #Atom_link.mid_link()
    #Atom_link.alpha()
    #Atom_link.product()
    #
    print('D:两种情况')
    Atom_link = atom_link(11,1,0,None,None,None) ####### TANG D1#####
    Atom_link.mid_link()
    Atom_link.alpha()
    Atom_link.mole_break1()
    print('\n')
    #Atom_link = atom_link(12,4,None,None,None) ####### TANG D2#####这些暂时也不用
    #Atom_link.mid_link()
    #Atom_link.alpha()
    #Atom_link.mole_break1()

###############JIANG###############
elif break1 == 2:
    print('C:第一种情况')
    Atom_link = atom_link(11,0,None,None,None) ### JIANG C 第一个#
    Atom_link.mid_link()
    Atom_link.alpha()
    Atom_link.mole_break()
    print('\n')
    
    print('C:第二种情况')
    Atom_link = atom_link(14,2,None,None,None) ### JIANG C 第二个#
    Atom_link.mid_link()
    Atom_link.alpha()
    Atom_link.mole_break()
    print('\n')
                    
    Atom_link = atom_link(11,0,0,None,None,None) ### JIANG D 加羟基#
    Atom_link.mid_link()
    Atom_link.alpha()
    Atom_link.mole_break()
    print('\n')
    
    
    print('A:第一种')
    Atom_link = atom_link(14,3,None,None,None) ### JIANG 第一个A #
    Atom_link.mid_link()
    Atom_link.alpha()
    Atom_link.product()
    
    Atom_link = atom_link(11,0,None,None,None) ### JIANG 第一个A S的裂解#
    Atom_link.mid_link()
    Atom_link.alpha()
    Atom_link.product()
    print('\n')
    
    print('B:第一种')
    Atom_link = atom_link(14,3,None,None,None) ### JIANG 第一个B #
    Atom_link.mid_link()
    Atom_link.alpha()
    Atom_link.mole_break()
    print('\n')
     
    print('A:第二种')          
    Atom_link = atom_link(14,0,0,None,None,None) ### JIANG 第二个A #
    Atom_link.mid_link()
    Atom_link.alpha()
    Atom_link.mole_break()  
    print('\n')     
    
    print('B:第二种')
    Atom_link = atom_link(14,0,1,None,None,None) ### JIANG 第二个B #
    Atom_link.mid_link()
    Atom_link.alpha()
    Atom_link.mole_break()         
                