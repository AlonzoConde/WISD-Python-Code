import os
import csv
from itertools import groupby


rows = []

# CSV file code will be reading from
# Each row found in the CSV file will be stored into "rows" for simpler data manipulation
with open('test.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        rows.append(row)

print(rows)


def findIDs(date):
    a = date + 1

    print(a)


# userConsec = int(input("Enter number of conseutive days : "))
# userAbsCode = input("Enter the Absence code : ")



tmp = []

test_date = rows[1][0]
for i in range(1, len(rows)):
    TDATE = test_date
    test_date = rows[i][0]

    # Test Date is about to change, do something with it
    if TDATE != test_date or i == len(rows) - 1:
        print(list(set(tmp)))
        findIDs(tmp[0])
        tmp.clear()

    tmp.append(test_date)

 
# def createNewRow(building, test_date, grade, abs_code, consec_abs, dates):
#     newRow = [building, test_date, grade, abs_code, consec_abs]
#     for i in range(0, len(dates)):
#         newRow.append(dates[i])
    
#     writer.writerow(newRow)


# finalAbs = xDaysAbsent(userConsec, combined)

# heading = ['Building', 'Student ID', 'Grade', 'Absence Code', 'Consec Absenses']

# for i in range(1, userConsec+1):
#     heading.append('Day ' + str(i))

# finalAbs.insert(0, heading)

# with open('consecAbs.csv', 'w', newline='', encoding='UTF8') as f:
#     writer = csv.writer(f)
#     for j in range(0, len(finalAbs[0])):
        
#         f.write(str(finalAbs[0][j]) + ', ')
#     f.write('\n')


#     for i in range(1, len(finalAbs)):
#             createNewRow(finalAbs[i][0], finalAbs[i][1], finalAbs[i][2], finalAbs[i][3], userConsec, finalAbs[i][5])
