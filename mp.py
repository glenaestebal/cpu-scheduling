
"""
scheduling algorithm        value of x
FCFS                            0
SJF                             1
SRTF                            2
RR                              3

"""
import copy

#arr[][0] process id
#arr[][1] AT
#arr[][2] BT

def FCFS (x, y, z, arr):
    arr.sort(key=lambda x:(x[1],x[0])) # sort by arrival time, secondary key PID
    
    arrWT = []         # avgWT
    ID = arr[0][0]     # process ID
    AT = arr[0][1]     # arrival time
    BT = arr[0][2]     # burst time
    CT = AT + BT       # completion time
    WT = (CT - AT - BT)# waiting time
    arrWT.append(WT)

    idle = []           # idle time
    idleST = []         # idle start time
    idleET = []         # idle end time

    
    if AT != 0:
        print("idle start time: 0 end time:", AT)
#       idle.append(AT)
        idleST.append(0)
        idleET.append(AT)
    
    print("1 start time:", AT,"end time:", CT,"| Waiting time:", WT)

    for i in range(1, y):
        ST = arr[i][1] #start time
        AT = arr[i][1]  
        BT = arr[i][2]
        
        if(ST<=CT):    #if next process arrival time is less than or equal to the completion time of the process before it, the next starting time will be the arrival time. 
            ST = CT
            CT = ST + BT
        else:         #if next process arrival time is higher than completion time of the process before it, there will be idle time.
            print("idle start time:", CT, "end time:", AT)
#           idle.append(ST - CT)
            idleST.append(CT)
            idleET.append(AT)
            CT = ST + BT
            
        WT = (CT - AT - BT)
        arrWT.append(WT)
        print(i + 1, "start time:", ST,"end time:", CT,"| Waiting time:", WT)

    if(len(idleST) > 0): #print process of idle time
        print("idle ", end="")
        for i in range(0, len(idleST)-1):
           print("start time:", idleST[i],"end time:", idleET[i], "|", end="") 
        print("start time:", idleST[i-1],"end time:", idleET[i-1])
        
    print("Average waiting time:", sum(arrWT)/y)
    
#   if(len(idle) > 0):
#     print("Total idle time: ", sum(idle))
    

def SJF (x, y, z, arr):
    pass

def SRTF (x, y, z, arr):
    temp_arr = []
    arrived_proc = []
    gantt_chart = []
    output = []
    idle = []
    time = 0

    temp_arr = copy.deepcopy(arr)
    temp_arr.sort(key=lambda x:x[0])

    finish = False
    while(not finish):
        arr.sort(key=lambda x:(x[1]))
        for value in arr.copy():
            if(value[1] <= time and value[2] > 0):
                arrived_proc.append(value)
                arr.remove(value)
            else:
                break
           
        #checks for idle time
        if(len(arrived_proc) == 0 and len(arr) != 0):
            #idle.append([time, arr[0][1]])
            time = arr[0][1]
            for value in arr.copy():
                if(value[1] <= time and value[2] > 0):
                    arrived_proc.append(value)
                    arr.remove(value)
                else:
                    break

        arrived_proc.sort(key=lambda x:(x[2],x[1]))

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
    for i in range(1, len(gantt_chart)):

        if(gantt_chart[i][0] != gantt_chart[i-1][0]):
            e_time = gantt_chart[i-1][2]
            output.append([gantt_chart[i-1][0], s_time, e_time])
            s_time = gantt_chart[i][1]

        if(i == len(gantt_chart)-1):
            e_time = gantt_chart[i][2]
            output.append([gantt_chart[i][0], s_time, e_time])
   
    output.sort(key=lambda x:x[0])

    toPrint = "Idle Time: "
    if(len(idle) != 0):
        for i in range(len(idle)):
            toPrint = toPrint + (f"start time: {idle[i][0]} end time: {idle[i][1]} ")
            if(i < len(idle)-1):
                toPrint = toPrint + ("| ")
        print(toPrint)

    waiting_time = 0
    str_output = (f"{output[0][0]} start time: {output[0][1]} end time: {output[0][2]} ")
    for i in range(1, len(output)):

        if(output[i][0] == output[i-1][0]):
            str_output = str_output + (f"| start time: {output[i][1]} end time: {output[i][2]} ")
            
        elif(output[i][0] != output[i-1][0]):
            str_output = str_output + (f"| Waiting time: {output[i-1][2] - temp_arr[output[i-1][0]-1][1] - temp_arr[output[i-1][0]-1][2]}")
            waiting_time += output[i-1][2] - temp_arr[output[i-1][0]-1][1] - temp_arr[output[i-1][0]-1][2]
            print(str_output)
            str_output = ""
            str_output = (f"{output[i][0]} start time: {output[i][1]} end time: {output[i][2]} ")
        
        if(i == len(output)-1):
            str_output = str_output + (f"| Waiting time: {output[i][2] - temp_arr[output[i][0]-1][1] - temp_arr[output[i][0]-1][2]}")
            waiting_time += output[i][2] - temp_arr[output[i][0]-1][1] - temp_arr[output[i][0]-1][2]
            print(str_output)
        
    print(f"Average waiting time: {round(waiting_time/len(temp_arr), 1)}")

def RR (x, y, z, arr):
    pass


# main
x, y, z = list(map(int,input().strip().split(" ")))

# arr[i] contains a, b, c
arr = [list(map(int,input().strip().split(" "))) for _ in range(y)]

if x == 0:
    FCFS(x, y, z, arr)
    z = 1   #  𝑍 denotes a time slice value. If the CPU scheduling algorithm indicated by the value of 𝑋 is not RR, this value must be set to 1 but ignored.    
elif x == 1:
    print("1")
    z = 1    
elif x == 2:
    arr.sort(key=lambda x:(x[1], x[2]))
    SRTF(x, y, z, arr)
    z = 1    
elif x == 3:
    print("3")
else:
    print("Invalid input")

