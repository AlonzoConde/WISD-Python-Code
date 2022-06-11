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



def makeInt(lst):
    a = []
    for i in range(0, len(lst)):
        a.append(int(lst[i]))
    return a

def consecutive(lst):
    a = []
    b = []

    for i in range(len(lst) - 1):
        b.clear()
        if lst[i] + 1 == lst[i+1]:
            b.append(lst[i])
            b.append(lst[i+1])
            for j in range(len(lst) - 1):
                try:
                    if j >= 2:
                        if lst[i] + j == lst[i+j]:
                            b.append(lst[i+j])
                except:
                    break
            a.append(list(b))
    return a

def createDict(lstDate, lstNum):

    dicts = {}
    sameLen = len(lstDate)

    for i in range(0, sameLen):
        dicts[int(lstNum[i])] = lstDate[i]
    return [dicts]

def xDaysAbsent(userInput, lst):
    tmp = []
    tmp2 = []
    final = []

    for i in range(0, len(lst)):
        tmp.clear()
        for j in range(0, len(lst[i][-1])):
            if len(lst[i][-1][j]) >= userInput:
                tmp.append(lst[i][2])
                tmp.append(lst[i][0])
                tmp.append(lst[i][3])
                tmp.append(lst[i][4])
                tmp.append(lst[i][-1][j])
                break
        if len(tmp) > 0:
            final.append(list(tmp))
            
    for u in range(0, len(final)):
        tmp2.clear()
        for v in range(0, len(final[u][4])):
            for x in range(0, len(lst)):
                for y in range(0, len(lst[x][3])):
                    my_dict = lst[x][1]
                    for key, value in my_dict.items():
                        if key in final[u][4]:

                            tmp2.append(value)
            
        if len(tmp2) > 0:
            final[u].append(sorted(list(set(tmp2))))

    return final



userConsec = int(input("Enter number of conseutive days : "))
userAbsCode = input("Enter the Absence code : ")


# Consectuive date Ex- rows[i][12]
combined = []
consecutiveNums = []
consecutiveDates = []
consecutiveIds = []
consecutiveBuilding = []
consecutiveGrade = []
consecutiveAbsenceCode= []
tmp = []

stu_id = rows[1][0]
for i in range(1, len(rows)):
    SID = stu_id
    stu_id = rows[i][0]

    # Student ID is about to change
    if SID != stu_id or i == len(rows) - 1:
        tmp.extend(list(set(consecutiveIds)))
        tmp.extend(list(createDict(consecutiveDates, consecutiveNums)))
        tmp.extend(list(set(consecutiveBuilding)))
        tmp.extend(list(set(consecutiveGrade)))
        tmp.extend(list(set(consecutiveAbsenceCode)))
        tmp.append(list(consecutive(makeInt(consecutiveNums))))
        combined.append(list(tmp))
        
        consecutiveIds.clear()
        consecutiveDates.clear()
        consecutiveNums.clear()
        consecutiveBuilding.clear()
        consecutiveGrade.clear()
        consecutiveAbsenceCode.clear()
        tmp.clear()

    consecutiveIds.append(stu_id)
    consecutiveDates.append(rows[i][5])
    consecutiveNums.append(rows[i][12])
    consecutiveBuilding.append(rows[i][3])
    consecutiveGrade.append(rows[i][4])
    consecutiveAbsenceCode.append(rows[i][10].strip(' '))
 
def createNewRow(building, stu_id, grade, abs_code, consec_abs, dates):
    newRow = [building, stu_id, grade, abs_code, consec_abs]
    for i in range(0, len(dates)):
        newRow.append(dates[i])
    
    writer.writerow(newRow)


finalAbs = xDaysAbsent(userConsec, combined)

heading = ['Building', 'Student ID', 'Grade', 'Absence Code', 'Consec Absenses']

for i in range(1, userConsec+1):
    heading.append('Day ' + str(i))

finalAbs.insert(0, heading)

with open('consecAbs.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    for j in range(0, len(finalAbs[0])):
        
        f.write(str(finalAbs[0][j]) + ', ')
    f.write('\n')


    for i in range(1, len(finalAbs)):
            createNewRow(finalAbs[i][0], finalAbs[i][1], finalAbs[i][2], finalAbs[i][3], userConsec, finalAbs[i][5])
