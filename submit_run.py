# Import required libraries
import itertools
import os
import numpy as np
import subprocess
from multiprocessing import Pool

# Define a function to submit commands
def submit_command(cmd, cwd=None):
    try:
        subprocess.call(cmd, shell=True, cwd=cwd)
    except Exception, e:  # Catching exception in Python 2.6 style
        print("Failed to execute command: %s. Error: %s" % (cmd, str(e)))

# Define a function to run simulations
def run_simulation(jobs_directory, job_name, temperatures, num_nodes, num_subunits, hostlist, project_name):
    # Create a list of temperatures within the given range
    commands = []
    # Create a process pool (manually join in Python 2.6)
    p = Pool(num_nodes)

    for i, temp in enumerate(temperatures):
        # Construct the command string
        command = '%s %.1f %s %d %s ' % (job_name, int(temp), hostlist[i % len(hostlist)], num_subunits, project_name)
        #command ='pwd'
        #print(command)
        commands.append(command)
        p.apply_async(submit_command, args=(command, jobs_directory))
        #print(command)
    # Close the process pool to prevent new tasks from being added
    p.close()

    # Wait for all child processes to complete
    p.join()



# Define a function to group and print temperatures
def group_and_print_temperatures(T_subunit):
    """
    Groups temperature subunits with their corresponding numbers and prints the results.
    
    :param T_subunit: A list of temperature subunits
    """
    
    # Generate subunit numbers
    subunit_num = range(1, len(T_subunit) + 1)

    # Pair temperature subunits with subunit numbers to create a new tuple list
    paired_list = zip(T_subunit, subunit_num)

    # Sort the pairs by temperature subunit in ascending order
    sorted_pairs = sorted(paired_list, key=lambda x: x[0], reverse=False)

    # Group the sorted data using itertools.groupby and assign a number to each group
    grouped_pairs = []
    current_group_key = None
    for key, group in itertools.groupby(sorted_pairs, key=lambda x: x[0]):
        group_list = list(group)
        group_nums = [pair[1] for pair in group_list]
        
        if current_group_key == key:
            grouped_pairs[-1][1].extend(group_nums)
        else:
            grouped_pairs.append((key, group_nums))
        current_group_key = key

    # Output the results
    for num, nums in grouped_pairs:
        print("Temperature %dK: %s" % (num, nums))

# Assuming you have your temperatures list defined


# Example usage
T_min = 300  #min temperature
T_max = 500  #max temperature
n = 7     #the number of subunits(chains)
Pro_name = 'arp23'  #the name of proteins
hostlist = [ 'node17', 'node18', 'node19']   # the hostlists



# Run the setup simulations with room temperature
Tc = [300]
run_simulation('Input','../submit_em.sh', Tc, 1, n, hostlist, Pro_name)
print("first simulation is done")

try:
    os.mkdir('run')
except OSError, e:  # Catching OSError in Python 2.6
    if e.errno == 17:  # Check error code for directory already exists
        print("Directory 'run' already exists.")
os.chdir('run')

# Run the simulations
temps = np.linspace(T_min,T_max,len(hostlist))
run_simulation('.', '../submit_run.sh', temps, len(hostlist), n, hostlist, Pro_name)
print("first simulation is done")

# Main loop is also simplified and not updated for Python 2.6 compatibility.
# Additional code for Python 2.6 could be included here, but since the original snippet didn't contain 

# specific parts requiring changes for Python 2.6 compatibility, they have been left out.

# mian loop
T_subunit = np.zeros(n) 
while True:
    T_list = [] # T_list is a list of temperature
    T_lists = [] # T_list is a list of temperature pairs
    deltaT = [] # deltaT is a list of temperature differences
    deltaSub = [] # deltaSub is a list of subunit differences
    sub_num = [] # sub_num is a list of subunit numbers
    T_list0 = os.listdir('.') 
    T_list0.sort()
    subunit_matrix = [] 
    
    # T_list is the temperature list of finished simulation
    for T in T_list0:
        try:
            subunit_matrix.append(np.loadtxt(os.path.join('.', T, 'subunit.txt')))
            T_list.append(float(T)) 
            #T_list.append(T) 
        except Exception:
            continue

    subunit_matrix = np.array(subunit_matrix) # subunit_matrix is a matrix of subunit numbers
   # print(subunit_matrix)
    sub_num = np.sum(subunit_matrix, axis=1) # sub_num is the number of dissociated subunits at each temp

    # Group and print temperatures
    m = len(T_list)
    for j in range(n):
        for i in range(m-1):
            if subunit_matrix[i, j] != subunit_matrix[i + 1, j]:
                T_subunit[j] = T_list[i + 1]
                delta_Sub = sub_num[i + 1] - sub_num[i] 
                delta_T = T_list[i + 1] - T_list[i] 
                if delta_T > 1.0 and delta_Sub > 1.0: 
                    T_lists.append([T_list[i], T_list[i + 1]]) 
                    deltaT.append(delta_T) 
                    deltaSub.append(delta_Sub)
                else: 
                    break
    if not T_lists:
        group_and_print_temperatures(T_subunit)
        print("work is done")
        break

    # Sort the temperatures by temperature difference and subunit difference    
    tem_sorted = []
    for i in range(len(deltaT)): 
        tem_sorted.append([T_lists[i], deltaSub[i], deltaT[i]])
    tem_sorted = sorted(tem_sorted, key=lambda x : (-x[2], -x[1])) 

    # Unique the temperature pairs
    tem_uniq=[]
    sort_T=[]
    sort_temp=[]
    for i in tem_sorted:
        if i not in tem_uniq :
            tem_uniq.append(i)

    # Assign subunit numbers to each temperature
    node_sub = np.zeros(len(tem_uniq), dtype=int) 
    for i in range(len(hostlist)):
        for j in range(len(tem_uniq)):
            temp = tem_uniq[j][2]
            if temp / (i + 1) > 1.0 and sum(node_sub) < len(hostlist):
                node_sub[j] = i + 1 
            else:
                break

    # Assign temperature numbers to each host
    temp_l = []
    for i in range(len(tem_uniq)):
        temp_range = tem_uniq[i][0]
        temp_l.extend(np.linspace(float(temp_range[0]), float(temp_range[1]), node_sub[i] + 2)[1:-1])

    # Round the temperature numbers to the nearest integer
    temp_list = np.unique(np.rint(temp_l))

    # Generate commands
    run_simulation('.', '../submit_run.sh', temp_list, len(hostlist), n, hostlist, Pro_name)

