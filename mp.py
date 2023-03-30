
"""
scheduling algorithm        value of x
FCFS                            0
SJF                             1
SRTF                            2
RR                              3

"""
import copy

def FCFS (x, y, z, arr):
    arr.sort(key=lambda x:(x[1],x[0])) # sort by arrival time, secondary key PID
    
    arrWT = []         # avgWT
    ID = arr[0][0]     # process ID
    AT = arr[0][1]     # arrival time
    BT = arr[0][2]     # burst time
    CT = AT + BT       # completion time
    WT = (CT - AT - BT)# waiting time
    arrWT.append(WT)

    idleST = []         # idle start time
    idleET = []         # idle end time

    with open("output-FCFS.txt", "w") as f:
        if AT != 0: #if AT != 0 then it prints idle time, appends 0 to list of idleST and AT to idleET
            print("idle start time: 0 end time:", AT)
            f.write(f"idle start time: 0 end time: {AT}\n")
            idleST.append(0)
            idleET.append(AT)

        print("1 start time:", AT,"end time:", CT,"| Waiting time:", WT)
        f.write(f"1 start time: {AT} end time: {CT} | Waiting time: {WT}\n") #prints first process

        for i in range(1, y):
            ST = arr[i][1] #start time
            AT = arr[i][1]  
            BT = arr[i][2]
            
            if(ST<=CT):    #if next process arrival time is less than or equal to the completion time of the process before it, the next starting time will be the arrival time. 
                ST = CT
                CT = ST + BT
            else:         #if next process arrival time is higher than completion time of the process before it, there will be idle time.
                print("idle start time:", CT, "end time:", AT)
                f.write(f"idle start time: {CT} end time: {AT}\n")
                idleST.append(CT)
                idleET.append(AT)
                CT = ST + BT

            WT = (CT - AT - BT)
            arrWT.append(WT)
            print(i + 1, "start time:", ST,"end time:", CT,"| Waiting time:", WT)
            f.write(f"{i + 1} start time: {ST} end time: {CT} | Waiting time: {WT}\n")

        if(len(idleST) > 0): #print process of idle time
            print("idle ", end="")
            f.write(f"idle ")
            for i in range(0, len(idleST)-1):
                print("start time:", idleST[i],"end time:", idleET[i], "|", end="") 
                f.write(f"start time: {idleST[i]} end time: {idleET[i]} | ")
            print("start time:", idleST[-1],"end time:", idleET[-1])   
            f.write(f"start time: {idleST[-1]} end time: {idleET[-1]}")

        avgWT = sum(arrWT)/y
        print("Average waiting time: %.1f" % avgWT)
        f.write(f"\nAverage waiting time: {avgWT:.1f}")
        
def SJF (x, y, z, arr):
    start_time = 0
    gantt_chart = []

    # [pid, at, bt] dinagdagan ng state {0, 1} -> [pid, at, bt, state]
    # * : spread operator [1, 2, 3] -> 1, 2, 3, di na nagiging array para madagdag yung state
    # [pid, at, bt] -> [pid, at, bt, state]
    arr = list(map(lambda x: [*x, 0], arr))  
    arr.sort(key=lambda x: x[1])
    
    for pid, arrival_time, burst_time, state in arr:
        ready_queue = [] # for processes that have arrived
        normal_queue = [] # for processes that have not yet arrived

        for p, at, bt, s in arr:
            # processes less than start time and not yet executed are stored in ready_queue
            if at <= start_time and s == 0: 
                ready_queue.append([p, at, bt])
            # processes that are not less than the start time but have not yet executed are stored in the normal queue
            elif s == 0:
                normal_queue.append([p, at, bt])

        # if may laman ang ready queue, 
        if len(ready_queue) > 0:
            # kinuha yung minimum burst time
            shortest = min(ready_queue, key=lambda x: x[2]) 
            # end time will be start time + burst time of the process
            end_time = start_time + shortest[2]
            # getting waiting time
            waiting_time = start_time - shortest[1]
            # appending to the gantt chart
            gantt_chart.append([shortest[0], start_time, end_time, waiting_time, 0])
            # setting end time as the start time of the next process
            start_time = end_time
        
            # process that has been executed in the ready queue is set to state 1 or processed state
            for i in range(len(arr)):
                if arr[i][0] == shortest[0]:     
                    arr[i][3] = 1
                    break
            
        # if there are no processes in ready queue, go check normal queue for the processes that have not arrived yet
        else: 
            # if start time is less than the arrival time of the first process sa normal queue
            if start_time < normal_queue[0][1]: 
                # idle time
                idle_start = start_time # at this state start time = to the end time of the previous process
                idle_end = normal_queue[0][1]
                waiting_time = 0
                # appending to the gantt chart, last value: is_idle (1 if yes, 0 if no)
                gantt_chart.append([normal_queue[0][0], idle_start, idle_end, waiting_time, 1])
                # make the start time the arrival time 
                start_time = normal_queue[0][1] 

            end_time = start_time + normal_queue[0][2]
            waiting_time = start_time - normal_queue[0][1]
            gantt_chart.append([normal_queue[0][0], start_time, end_time, waiting_time, 0])
            start_time = end_time

            for i in range(len(arr)):
                if arr[i][0] == normal_queue[0][0]:
                    arr[i][3] = 1
                    break

    # sorting the output by process id
    gantt_chart.sort(key=lambda x:(x[0], x[3]))

    # writing the output to a file
    with open("output-sjf.txt", "w") as f:
        for pid, start_time, end_time, waiting_time, is_idle in gantt_chart:
            _id = pid if not is_idle else "IDLE"
            print(f"{_id} start time: {start_time} end time: {end_time} | Waiting time: {waiting_time}")
            f.write(f"{_id} start time: {start_time} end time: {end_time} | Waiting time: {waiting_time}\n")
        print(f"Average waiting time: {sum(map(lambda x:x[3], gantt_chart))/y:.1f}\n")
        f.write(f"Average waiting time: {sum(map(lambda x:x[3], gantt_chart))/y:.1f}\n")

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
        for value in arr.copy():
            if(value[1] <= time and value[2] > 0):
                arrived_proc.append(value)
                arr.remove(value)
            else:
                break
           
        #checks for idle time
        if(len(arrived_proc) == 0 and len(arr) != 0):
            idle.append([time, arr[0][1]])
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

    with open("output-srtf.txt", "w") as f:
        toPrint = "Idle Time: "
        if(len(idle) != 0):
            for i in range(len(idle)):
                toPrint = toPrint + (f"start time: {idle[i][0]} end time: {idle[i][1]} ")
                if(i < len(idle)-1):
                    toPrint = toPrint + ("| ")
            f.write(toPrint + "\n")
        
        waiting_time = 0
        str_output = (f"{output[0][0]} start time: {output[0][1]} end time: {output[0][2]} ")
        for i in range(1, len(output)):

            if(output[i][0] == output[i-1][0]):
                str_output = str_output + (f"| start time: {output[i][1]} end time: {output[i][2]} ")
                
            elif(output[i][0] != output[i-1][0]):
                str_output = str_output + (f"| Waiting time: {output[i-1][2] - temp_arr[output[i-1][0]-1][1] - temp_arr[output[i-1][0]-1][2]}\n")
                waiting_time += output[i-1][2] - temp_arr[output[i-1][0]-1][1] - temp_arr[output[i-1][0]-1][2]
                f.write(str_output)
                str_output = ""
                str_output = (f"{output[i][0]} start time: {output[i][1]} end time: {output[i][2]} ")
            
            if(i == len(output)-1):
                str_output = str_output + (f"| Waiting time: {output[i][2] - temp_arr[output[i][0]-1][1] - temp_arr[output[i][0]-1][2]}\n")
                waiting_time += output[i][2] - temp_arr[output[i][0]-1][1] - temp_arr[output[i][0]-1][2]
                f.write(str_output)
            
        f.write(f"Average waiting time: {round(waiting_time/len(temp_arr), 1)}")

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
    SJF(x, y, z, arr)
    z = 1    
elif x == 2:
    arr.sort(key=lambda x:(x[1], x[2]))
    SRTF(x, y, z, arr)
    z = 1    
elif x == 3:
    print("3")
else:
    print("Invalid input")

