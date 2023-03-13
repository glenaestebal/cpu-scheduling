
"""
scheduling algorithm        value of x
FCFS                            0
SJF                             1
SRTF                            2
RR                              3

"""

def FCFS (x, y, z, arr):
    pass

def SJF (x, y, z, arr):
    pass

def SRTF (x, y, z, arr):
    pass

def RR (x, y, z, arr):
    pass


# main
x, y, z = list(map(int,input().strip().split(" ")))

# arr[i] contains a, b, c
arr = [list(map(int,input().strip().split(" "))) for _ in range(y)]

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

