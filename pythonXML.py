import xml.etree.ElementTree as ET
import os
import time
from datetime import datetime
import getpass


# NECESSARY to take care of namespaces in XML file, program won't work without this
# Use "ns" dictionarty to parse XML file
ET.register_namespace("", "http://www.tea.state.tx.us/tsds")
ns = {"":"http://www.tea.state.tx.us/tsds"}

# File name where student ID's are found as user input
name = input("Enter file name: ")
fileName = name
name = name + ".xml"
#name = "108913_000_2021TSDS_202106160705_InterchangeStudentAssessment.xml"

# Only those with access to this path will be able to run this program
path = "//934nas01/Technology/PEIMS/"

# Looks for the full path of user inputted file name. If file is found, 
# function will return full file path. If not, then program will fail.
def find(name, path):
   for root, dirs, files in os.walk(path):
      for name1 in files:
         # Get python File location
         if name1 == name:  
               #print(os.path.abspath(os.path.join(root, name1)))
               return os.path.abspath(os.path.join(root, name1))
   return("Couldn't find file location \n")

# "x" will contain full file path 
x = find(name, path)

# Verification to user to make sure file path is correct
print("Full Path: " + x)

# Parse the tree by the created path
#tree = ET.parse('test.xml')
tree = ET.parse(x)
root = tree.getroot()

# List to hold all elements from XML file that contain the ID attribute
elementList = []
elementList2 = []
# list that holds all user inputted ID's
stu_id = []

# number of elements as input
n = int(input("Enter number of Student ID's : "))
 
# iterating till the range
for i in range(0, n):
    ele = int(input())
 
    stu_id.append(ele) # adding the element

# Start at the "root" of the tree and loop based on key and value in XML file
# Looks and stores all children of root and stores any element that has a matching ID attribute
for child in root.findall(".//",ns):
   #print(child.text + "-", end="", flush=True)
   for k,v in child.attrib.items():
      for i in range(len(stu_id)):
         if str(stu_id[i]) in v:
            #print(child.attrib)
            elementList.append(child)
            elementList2.append(child.attrib)
         else:
            print("Root: " + str(root))
            print("K: " + str(k))
            print("V: " + str(v))
            print("CHILD: " + str(child))
            print("Att: " + str(child.attrib))
            print("Tag: " + str(child.tag))

# Gets list of elements that have the "ID" attribute and removes from XML file
print('\n')
notInFile = []

username = getpass.getuser()

# Opens "Data_Log" and appends to it every time the program runs successfully.
# Used to timstamp "Data_Log" file exery time its run with current date and time.
now = datetime.now()
currentDate = datetime.today().strftime('%m.%d.%Y')
currentTime = now.strftime('%I:%M:%S %p')

# Data_Log stuff
f = open("Data_Log.txt", "a")
f.write('\n-------------------------------------------------------------------------------------- \n\n')
f.write("File Used: " + x + '\n\n')
f.write(username)
f.write('\t')
f.write(currentDate)
f.write('\t')
f.write(currentTime)
f.write('\n\n')
f.write("Deleted Student Info: \n")

for i in elementList:   
   try:
      root.remove(i)
      print(i.attrib)
      f.write(str(i.attrib) + "\n")
   except:
      #print("Not Found: " + str(i.attrib)[9:19])
      if str(i.attrib)[9:19] not in notInFile:
         print("")#notInFile.append(str(i.attrib)[9:19])#str(i.attrib)[9:19])
      else:
         continue

# Timestamps Student ID's found that don't apply to the XML file being edited
f.write("\nStudent ID's Not Found: \n")
print("\nStudent ID's Not Found: ")
# f.write(username)
# f.write('\t')
# f.write(currentDate)
# f.write('\t')
# f.write(currentTime)

# Gets list of elements that have the "ID" attribute and removes from XML file
print('\n')
notInFile = []
notInFile2 = []

for c in range(len(elementList2)):
    for r in range(len(stu_id)):
        if str(stu_id[r]) in str(elementList2[c]):
            #print("Element: " + str(elementList2[c]) + "   :   " + str(stu_id[r]))
            if str(stu_id[r]) not in notInFile:
                notInFile.append(str(stu_id[r]))            
print('\n')
for t in range(len(notInFile)):
    for y in range(len(stu_id)):
         if str(stu_id[y]) not in str(notInFile[t]) and str(stu_id[y]) not in notInFile:
            notInFile2.append(str(stu_id[y]))
            # if str(stu_id[y]) not in notInFile:
            #     print(str(stu_id[y]))

notInFile2 = set(notInFile2)
len_Not = print(len(notInFile2))
if len_Not != 0:
   for q in notInFile2:
      f.write(q + '\n')
      print(q)
else:
   f.write("No unused ID's")

# Creates a new XML file without those with the passed sutdent "ID" value.=
tree.write(fileName + "_py.xml")
f.close()