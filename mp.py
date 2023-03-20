
"""
scheduling algorithm        value of x
FCFS                            0
SJF                             1
SRTF                            2
RR                              3

"""
import copy

def FCFS (x, y, z, arr):
    pass

def SJF (x, y, z, arr):
    pass

def SRTF (x, y, z, arr):
    temp_arr = []
    arrived_proc = []
    gantt_chart = []
    output = []
    time = arr[0][1]

    temp_arr = copy.deepcopy(arr)
    temp_arr.sort(key=lambda x:x[0])

    finish = False
    while(not finish):
        arr.sort(key=lambda x:x[1])
    
        if(len(arr) != 0):
            #determines if process arrived
            if(arr[0][1] <= time and arr[0][2] > 0):
                arrived_proc.append(arr[0])
                arr.pop(0)

        arrived_proc.sort(key=lambda x:(x[2], x[1]))

        pid = arrived_proc[0][0]
        start_time = time
        end_time = time + 1 

        arrived_proc[0][2] -= 1
        time += 1
        
        gantt_chart.append([pid, start_time, end_time])

        #determines if burst time is empty already
        if(arrived_proc[0][2] == 0):
            arrived_proc.pop(0)

        if(len(arrived_proc) == 0 and len(arr) == 0):
            finish = True
        else:
            finish = False
    
    s_time = gantt_chart[0][1]
    for i in range(0, len(gantt_chart)-1):
            if(gantt_chart[i][0] != gantt_chart[i+1][0]):
                e_time = gantt_chart[i][2]
                output.append([gantt_chart[i][0], s_time, e_time])
                s_time = gantt_chart[i+1][1]
                
            elif(i == len(gantt_chart)-2):
                if(gantt_chart[i][0] != gantt_chart[i+1][0]):
                    e_time = gantt_chart[i][2]
                    output.append([gantt_chart[i][0], s_time, e_time])
                    s_time = gantt_chart[i+1][1]
                
                else:
                    e_time = gantt_chart[i+1][2]
                    output.append([gantt_chart[i][0], s_time, e_time])
    
    output.sort(key=lambda x:x[0])

    for i in range(0, len(output)-1):
        print("{} start time: {} end time: {}".format(output[i][0], output[i][1], output[i][2]))
        if(output[i][0] != output[i+1][0]):
            waiting_time = output[i][2] - temp_arr[output[i][0]-1][1]
            waiting_time -= temp_arr[output[i][0]-1][2]
            print("Waiting Time: {}".format(waiting_time))

        if(i == len(output)-2):
            print("{} start time: {} end time: {}".format(output[i+1][0], output[i+1][1], output[i+1][2]))
            waiting_time = output[i+1][2] - temp_arr[output[i+1][0]-1][1]
            waiting_time -= temp_arr[output[i+1][0]-1][2]
            print("Waiting Time: {}".format(waiting_time))
                    
            
        
       
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
    arr.sort(key=lambda x:x[1])
    SRTF(x, y, z, arr)
    z = 1    
elif x == 3:
    print("3")
else:
    print("Invalid input")

