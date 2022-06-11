import os
import time
from datetime import datetime
import pandas as pd
import csv
import copy

# Get and store today;s current date and time
now = datetime.now()

# Store todays date in dd/mm/yyyy format
# Store timestamp in hh:mm:ss am/pm format
currentDate = datetime.today().strftime('%m.%d.%Y')
currentTime = now.strftime('%I:%M:%S %p')

# Directories that need to be checked located from ip address:
directoryF = '///f/'
directoryG = '///g/'
directoryH = '///h/'
directoryI = '///i/'


def returnCameraIP(fileLocation):

    # Directory that will be seached stored in 'dirs'
    dirs = get_information(fileLocation)

    # Create a list of all directories (Camera ip address)
    # final_list will house all camers that don't have a recording for today
    directory_list = list()
    final_list = list()

    # Find all recording dates in each camera's IP address and put into a List
    for file in dirs:
        # Remove recycle bin
        if(file[0] != '$RECYCLE.BIN'):
            directory_list.append(file)

    #Remove "System Volume Information/" file
    directory_list.pop()

    # #print(directory_list)
    i = 0
    length = len(directory_list)

    for i in range(length):
        # Set our current directory to one camera IP address at a time
        dirs2 = os.listdir(fileLocation + directory_list[i][0] + '/')
        # #print(dirs2)

        # Get length of directory folder name
        list_length = len(directory_list[i][0])
        #print(directory_list[i][0])

        # If todays date is not in camera's IP, add the IP to 'final_list'
        # Since we only want camera ip, delete anything found after hyphen in directory name
        if currentDate not in dirs2:
            tmp = ""
            for j in range(0, list_length):
                # Copy ip address to 'tmp'
                # As soon as you find '-', break out of loop
                size = 0
                for path, dirs, files in os.walk(fileLocation + directory_list[i][0] + '/'):
                    for f in files:
                        fp = os.path.join(path, f)
                        size += os.path.getsize(fp)
                    # Format the size ouput to MBs with commas and 2 decimal places
                    size = size / 1000000.0
                    size = round(size, 2)
                    number_with_commas = "{:,}".format(size)

                directory_list[i][3] = number_with_commas
                if directory_list[i][0][j] != '-':
                    tmp += directory_list[i][0][j]
                else:
                    break

            final_list.append([tmp, directory_list[i][1],
                              directory_list[i][2], directory_list[i][3]])

    # Return list of all camera IP addresses that don't have a recoding for today
    #print(final_list)
    return final_list

# Will be used to get and store the initial information of each camera IP
# Info will be stored in a List that is formatted as: ['camera_ip', 'last_access_date', 'last_access_time', 'file_size']
# Returns that list for a single camera IP
def get_information(directory):
    file_list = []
    size = 0

    for i in os.listdir(directory):
        file_list.append([i, time.strftime(
            "%m/%d/%Y", time.localtime(os.path.getmtime(directory + i))), time.strftime("%I:%M:%S %p", time.localtime(
                os.path.getmtime(directory + i))), size])  # [file,last_access_date, last_access_time, file_size]
    return file_list


def sortCameraIP(listName):
    length = len(listName)
    # Make a copy of the passed list
    tmp = listName

    # Get the Camera IP and split it by the '.' to get the 2nd numbers value
    for i in range(0, length):
        tmp[i][0] = listName[i][0].split('.', 4)

    # 
    tmp.sort(key=lambda tmp: int(tmp[0][1]))
    glue = '.'

    for j in range(0, length):
        listName[j][0] = glue.join(tmp[j][0])

        #print(listName[j])

    return listName


def increasePandaV2(allFiles, todaysDate, timestamp):
    allFilesLength = len(allFiles)

    for i in range(0, allFilesLength):
        my_df.loc[len(my_df)] = [allFiles[i][0], allFiles[i][1],
                                 allFiles[i][2], allFiles[i][3], todaysDate, timestamp]

    my_df
    #print(my_df)

def swapIP(listName):
    size = len(listName)
    newList = listName
    
    for i in range(0, size):

        newIP = listName[i][0] + '     '
        newTime = listName[i][2][:5]+ ' '
        newDate = listName[i][1] + '  '
        newAMPM = listName[i][2][9:] + '                   '

        newList[i][0] = newDate
        newList[i][1] = newTime
        newList[i][2] = newAMPM
        newList[i][3] = newIP

    return newList


# Call function on all files (F through I) to find cameras that don't have a recording for today
# along with their file size amd  last date/time modified
print("Looking for Cameras in Folder F...")
try:
    fileF = returnCameraIP(directoryF)
    print("Done looking in forlder F.")
except:
    print("Cannot connect to ")
    print(directoryF)
    os.system("pause")
    system.exit()
    print('\n')
print("Looking for Cameras in Folder G...")
try:
    fileG = returnCameraIP(directoryG)
    print("Done looking in forlder G.")
except:
    print("Cannot connect to ")
    print(directoryG)
    os.system("pause")
    system.exit()
    print('\n')
print("Looking for Cameras in Folder H...")
try:
    fileH = returnCameraIP(directoryH)
    print("Done looking in forlder H.")
except:
    print("Cannot connect to ")
    print(directoryH)
    os.system("pause")
    system.exit()
    print('\n')
print("Looking for Cameras in Folder I...")
try:
    fileI = returnCameraIP(directoryI)
    print("Done looking in forlder I.")
    os.system("pause")
    system.exit()
    print('\n')
except:
    print("Cannot connect to ")
    print(directoryI)


# Combine all info into one giant list to make things easier. Formatted as:
# allCameraIP = [['ip_address', 'last_date_modified', 'last_time_modified', 'directory_size'],[],[]]
allCameraIP = fileF + fileG + fileH + fileI
 
# Sort all the info by the 2nd number of the Camera's IP
allCameraIP = sortCameraIP(allCameraIP)

#print(allCameraIP)
size1 = len(allCameraIP)
size2 = 0
newCamIP = copy.deepcopy(allCameraIP)
tmp = ''

# for x in range(0, len(newCamIP)):
#     newCamIP[x].pop()

newCamIP = swapIP(newCamIP)

title = ["Date", "Time", "AM/PM", "IP"]
with open('cameraIP.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(title)

    # write multiple rows
    writer.writerows(newCamIP)

for i in range(0, size1):
    tmp = ''
    size2 = len(newCamIP[i])
    for j in range(0, size2):
        tmp += newCamIP[i][j]
    newCamIP[i].pop()
    newCamIP[i].pop()
    newCamIP[i].pop()
    newCamIP[i].pop()
    newCamIP[i].append(tmp[:51])

textfile = open("camIPtxt1.txt", "w")
for element in newCamIP:
    textfile.write(str(element) + "\n")
textfile.close()
textfile = open("camIPtxt2.txt", "w")
for element in newCamIP:
    textfile.write(str(element) + "\n")
textfile.close()

textfile = open("camIPtxt3.txt", "w")
for element in newCamIP:
    textfile.write(str(element))
textfile.close()
textfile = open("camIPtxt4.txt", "w")
for element in newCamIP:
    textfile.write(str(element))
textfile.close()

###########################################################

# Read in the file
with open("camIPtxt2.txt", 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('[', '')
filedata = filedata.replace(']', '')
filedata = filedata.replace('\'', '')

# Write the file out again
with open("camIPtxt2.txt", 'w') as file:
  file.write(filedata)

with open("camIPtxt4.txt", 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('[', '')
filedata = filedata.replace(']', '')
filedata = filedata.replace('\'', '')

# Write the file out again
with open("camIPtxt4.txt", 'w') as file:
  file.write(filedata)
    

# Initialize the columns that will be used in the Dataframe
col_names = ['Cameras', 'Date', 'Time',
             'Size in MBs', 'Todays Date', 'Timestamp']
my_df = pd.DataFrame(columns=col_names)

# CReate Dataframe with all info gathered
increasePandaV2(allCameraIP, currentDate, currentTime)

print("Creating CSV and HTML files...")

# Create csv file
my_df.to_csv("Cameras_Down.csv", index=False)

# Create HTML file that right justifies the 'Size in MBs' column
my_df.to_html("Cameras_Down.html", formatters={
              'Cameras': lambda a: '<p style="text-align: right">' + a + '</p>',
              'Date': lambda b: '<p style="text-align: right">' + b + '</p>',
              'Time': lambda c: '<p style="text-align: right">' + c + '</p>',
              'Size in MBs': lambda d: '<p style="text-align: right">' + d + '</p>',
              'Todays Date': lambda e: '<p style="text-align: right">' + e + '</p>',
              'Timestamp': lambda f: '<p style="text-align: right">' + f + '</p>'}, escape=False)

os.system("pause")