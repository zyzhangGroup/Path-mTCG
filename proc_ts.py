import subprocess  # Import the subprocess module
from multiprocessing import Pool  # Import the Pool class
import sys  
import numpy as np  # Import the numpy module
import os  # Import the os module


def submit(cmd):  # Define the submit function, accepting one parameter cmd
    subprocess.call(cmd, shell=True)  # Call the call function from the subprocess module to execute a shell command
    return  # Return None



if len(sys.argv) != 2:  # Check if the number of command-line arguments is not equal to 2
    print("Usage: python *.py <number_of_subunits>")
    sys.exit(1)

n = int(sys.argv[1])  # Assign the value from the command line argument to variable n (after converting it to an integer)


file_list = os.listdir('.')  # Get the list of all filenames in the current directory and save it to file_list


all_con = np.loadtxt('all_contact.txt')  # Read data from 'all_contact.txt' file and save it to the all_con variable


for file_name in file_list:  # Iterate through each element in the file_list and assign it to the file_name variable
    if file_name[-3:] == '.ts':  # Check if the last three characters of file_name are '.ts'
        temp = file_name[:-3]  # If so, remove the last three characters and assign them to the temp variable
        cmds = []  # Define an empty list cmds
        cmds += ['./proc_ts.sh %s %d' % (temp, n)]  # Add the formatted string './proc_ts.sh %s %d' to cmds, where %s and %d are replaced by temp and n respectively
        print(cmds)  # Print the cmds list
        pool = Pool(len(temp))  # Create a Pool object with the number of processes specified by the length of temp
        pool.map(submit, cmds)  # Apply the submit function to each element in cmds using the map method of the pool object
        pool.close()  # Close the pool object
        pool.join()  # Wait for all processes in the pool object to complete

        file_ls = os.listdir('.')  # Get the list of all filenames in the current directory and save it to file_ls

        for file_nm in file_ls:  # Iterate through each element in the file_ls and assign it to the file_nm variable
            if file_nm[-7:] == '_qa.txt' and file_nm[:5] == temp:  # Check if the last seven characters of file_nm are '_qa.txt' and the first five characters are temp
                sub_q = file_nm
                sub_nm = file_nm[:-6]  # If so, remove the last six characters and assign them to the sub_nm variable
                SUB = np.loadtxt(sub_q)  # Read data from the sub_q file and save it to the SUB variable
                j = int(sub_q[6:8])  # Convert the 6th to 8th characters of sub_q to an integer and assign it to the j variable
                i = j - 1  
                sub_con = np.delete(all_con[i], i, axis=0)  # Remove the i-th column from the i-th row of all_con and assign it to the sub_con variable
                sub_qc = np.sum(SUB * sub_con, axis=1)  # Calculate the sum of the element-wise product of SUB and sub_con along axis 1 and assign it to sub_qc
                sum_con = np.sum(sub_con)  # Calculate the sum of sub_con and assign it to the sum_con variable
                ave_con = sub_qc / sum_con  # Calculate the quotient of sub_qc divided by sum_con and assign it to the ave_con variable
                save_sub = (sub_nm.zfill(7) + 'avecon.txt')  # Pad sub_nm with zeros to 7 characters and append 'avecon.txt', assigning the result to the save_sub variable
                np.savetxt(save_sub, ave_con, fmt='%.2f')  # Save ave_con to the file save_sub with two decimal places
                print(save_sub, "has been saved")  # Print save_sub followed by "has been saved"
            else:
                continue

    else:
        continue

print("works is done")  # Print "works is done"
