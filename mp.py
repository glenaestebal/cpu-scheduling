
"""
scheduling algorithm        value of x
FCFS                            0
SJF                             1
SRTF                            2
RR                              3

"""

def FCFS (x, y, a, b, c):
    pass

def SJF (x, y, a, b, c):
    pass

def SRTF (x, y, a, b, c):
    pass

def RR (x, y, a, b, c):
    pass


# main
x, y, z = list(map(int,input().strip().split(" ")))

for i in range(y):
    a, b, c = list(map(int,input().strip().split(" ")))

if x == 0:
    print("0")
    z = 1   #  𝑍 denotes a time slice value. If the CPU scheduling algorithm indicated by the value of 𝑋 is not RR, this value must be set to 1 but ignored.    
elif x == 1:
    print("1")
    z = 1    
elif x == 2:
    print("2")
    z = 1    
elif x == 3:
    print("3")
else:
    print("Invalid input")

