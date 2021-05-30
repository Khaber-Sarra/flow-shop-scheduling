import queue

def Makespan(cost,sol):
    n,m=cost.shape
    qTime = queue.PriorityQueue()
    
    qMachines = []
    for i in range(m):
        qMachines.append(queue.Queue())
    
    for i in range(n):
        qMachines[0].put(sol[i])
    
    busyMachines = []
    for i in range(m):
        busyMachines.append(False)
    
    time = 0
    
    job = qMachines[0].get()
    qTime.put((time+cost.iloc[job,0], 0, job))
    busyMachines[0] = True
    
    while True:
        time, mach, job = qTime.get()
        if job == sol[n-1] and mach == m-1:
            break
        busyMachines[mach] = False
        if not qMachines[mach].empty():
                j = qMachines[mach].get()
                qTime.put((time+cost.iloc[j,mach], mach, j))
                busyMachines[mach] = True
        if mach < m-1:
            if busyMachines[mach+1] == False:
                qTime.put((time+cost.iloc[job,mach+1], mach+1, job))
                busyMachines[mach+1] = True
            else:
                qMachines[mach+1].put(job)
    return time
