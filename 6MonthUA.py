import os
import csv
import copy
from datetime import date


def checkKey(dict, key):
    
    keyFlag = False

    if key in dict.keys():
        keyFlag = True
        return keyFlag
    
    return keyFlag

def giveValue(idList, finalList):
    sizeF = len(idList)
    value = {}
    
    for i in range(0, sizeF):
        if idList[i] in finalList:
            value[idList[i]] = 'Y'
        else:
            value[idList[i]] = 'N'
    
    #print(value)
    print(len(value))
    return value
        

def sixMonthRange(datesList, idsList):
    stuList = []
    tenOrMore = []
    startList = copy.deepcopy(datesList)
    datesList.reverse()
    breakOut = False

    numAbsences = len(datesList)
    lengthList = numAbsences
    tmpAbsences = numAbsences
    #print("Total Absences: ")
    #print(tmpAbsences)

    start = date(int(startList[0][:4]), int(startList[0][5:7]), int(startList[0][8:]))
    end = date(int(datesList[0][:4]), int(datesList[0][5:7]), int(datesList[0][8:]))
    diff = (end - start).days
    diff = abs(diff)

    # #print(idsList[0].strip())
    # #print(start)
    # #print(end)
    # #print(diff)
    # #print(tmpAbsences)
    # #print('\n')
    for x in range(1, lengthList):
        if breakOut == True:
            break
        # #print(diff)
        # #print(idsList[x].strip())
        # #print(start)
        # #print(end)
        # #print(diff)
        # #print(tmpAbsences)
        # #print('\n')
        for y in range(1, lengthList):
            

            if tmpAbsences >= 10:
                if diff > 183 and tmpAbsences > 10:
                    # Student has 10+ absences in more than 6 month period
                    # END is too big, make END = next biggest date
                    end = date(int(datesList[y][:4]), int(datesList[y][5:7]), int(datesList[y][8:]))
                elif diff <= 183 and tmpAbsences >= 10:
                    # Student has 10+ absences in a 6 month period
                    # Add ID to stuList
                    # if diff > 0:
                    #print(diff)
                    #print(idsList[x].strip())
                    #print(start)
                    #print(end)
                    #print(diff)
                    #print(tmpAbsences)
                    #print('\n')
                    tenOrMore.append(idsList[x].strip())
                    #print("INSDIE FUNC: ")
                    #print(tenOrMore)
                    breakOut = True
                    break

                tmpAbsences -= 1
            # else:
            #     breakOut = True
            #     break

            diff = (end - start).days
            diff = abs(diff)
            

            tmpAbsences = numAbsences
        #start = date(int(startList[x][:4]), int(startList[x][5:7]), int(startList[x][8:]))
            
    #print("ABOUT TO RETURN: ")
    #print(tenOrMore)
    return tenOrMore

rows = []
dates = []
ids = []
allIds = []
tenOrMore = []

#unexcusedabsences
with open('unexcusedabsences.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        rows.append(row)

stu_id = rows[0][4]
for i in range(0, len(rows)):
    SID = stu_id
    stu_id = rows[i][4]

    if SID != stu_id or i == len(rows) -1:
        # ID is about to change, do something with the dates list
        if sixMonthRange(dates, ids) != None:
            tenOrMore.extend(sixMonthRange(dates, ids))

        dates.clear()
        ids.clear()

    dates.append(rows[i][5][:10])
    ids.append(rows[i][4])
    allIds.append(rows[i][4].strip())

    # if i == len(rows) - 1:
    #     # ID is about to change, do something with the dates list
    #     #print(dates)
    #     if sixMonthRange(dates, ids) != None:
    #         tenOrMore.append(sixMonthRange(dates, ids))
    #     dates.clear()
    #     ids.clear()

#tenOrMore = list(set(i for j in tenOrMore for i in j))

#print(tenOrMore)

setAllIds = set(allIds)
setTenorMore = set(tenOrMore)

diff = setAllIds - setTenorMore
diff = list(diff)
print(len(diff))
allIds = list(set(allIds))
valueYN = giveValue(allIds, tenOrMore)

with open('final.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    for u in range(0, len(tenOrMore)):
        newRow = [108913, tenOrMore[u], 726, 50, 1, valueYN[tenOrMore[u]]]
        writer.writerow(newRow)
    for v in range(0, len(diff)):
        newRow = [108913, diff[v], 726, 50, 1, valueYN[diff[v]]]
        writer.writerow(newRow)

print(len(tenOrMore))


