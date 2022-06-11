import os
import csv

# Open the Key-Value files created from "Index" file shared from Google Drive 
# rows9_11 = []
# with open('cd.csv') as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=',')
#     # Update "row" youre looping through
#     for row in readCSV:
#         # Update "rowS" and "row" -> "row" is appending to "rowS" (row and rowS are different)
#         rows9_11.append(row)

rows12 = []
#Update "open" to correct file youre going to open 
with open('cd.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    # Update "row" youre looping through
    for row12 in readCSV:
        # Update "rowS" and "row" -> "row" is appending to "rowS" (row and rowS are different)
        rows12.append(row12)

# Update directory to the one with the correct photos (make sure to include double '\' - thats just the way this works)
os.chdir('C:\\tmp\\Python Projects\\Rename JPG\\photos\\all')


for photo in os.listdir():
    # Update "i" range
    for i in range(1, len(rows12)):
        # Update "j" range
        for j in range(0, len(rows12[i])): 
            # Update "row" cname
            if photo == rows12[i][1]:
                src = photo
                # Update "dst"
                dst = rows12[i][2]
                # "SRC" is original file name - "DST" is new file name
                try:
                    os.rename(src, dst)
                except:
                    continue
                # Wont work without break - after name is changed we need to jump to the next picture name
                # Without it, code will try to change the file name even tho its already been changed
                break
