import os
import csv

rows = []

# Not necessary, but used as a faster way to create new rows for the output CSV file
# Requires column index and value you want to input into said passed column
def createNewRow(stu_id, fNum, seqNum, fValue):
    newRow = [stu_id, fNum, seqNum, fValue]
    writer.writerow(newRow)

def checkStuID(stuID):
    if len(stuID) <= 5 and len(stuID) > 0:
        return True
    return False

def checkAppCode(appCode):
    codes = ['01', '02']

    if appCode in codes:
        return True
    return False

def checkDate(dateEntered):
    if len(dateEntered) <= 10 and len(dateEntered) >= 6:
        return True
    return False

def checkAppType(appType):
    types = ['FAFSA', 'TAFSA' ,'']

    if appType in types:
        return True
    return False


# CSV file the code will be reading from
# Each row found in the CSV file will be stored into "rows" for simpler data manipulation
with open('PEIMSFAFSA.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        rows.append(row)


#print(rows)

breakFlag = False
breakLocation = 0
breakReason = ""
exactProblem = ""

with open('upPFI.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    for i in range(1, len(rows)):
        if breakFlag == True:
            break
        for j in range(0, len(rows[0])):
            # Student ID
            if j == 0:
                cID = checkStuID(rows[i][j])
                if cID != True:
                    breakFlag = True
                    breakLocation = i
                    breakReason = "Student ID"
                    exactProblem = rows[i][j]
                    break
                studentID = rows[i][j]
            # Application Code
            elif j == 1: 
                cProgram = checkAppCode(rows[i][j])
                if cProgram != True:
                    breakFlag = True
                    breakLocation = i
                    breakReason = "Application Code"
                    exactProblem = rows[i][j]
                    break
                createNewRow(studentID, j, i, rows[i][j])
            # Application Type
            if j == 2: 
                cDate = checkAppType(rows[i][j])
                if cDate != True:
                    breakFlag = True
                    breakLocation = i
                    breakReason = "Application Type"
                    exactProblem = rows[i][j]
                    break
                try:
                    createNewRow(studentID, j, i, rows[i][j][0])
                except:
                    createNewRow(studentID, j, i, rows[i][j])
                #createNewRow(studentID, j, i, rows[i][j][0])
            # Application Met Date
            if j == 3: 
                cSubject = checkDate(rows[i][j])
                if cSubject != True:
                    breakFlag = True
                    breakLocation = i
                    breakReason = "Application Met Date"
                    exactProblem = rows[i][j]
                    break
                createNewRow(studentID, j, i, rows[i][j])
    if breakFlag == True:
        print("Fix doc at Line: " + str(breakLocation+1))
        print("Problem Coumn: " + breakReason)
        print("Exact Reason: \" " + exactProblem + " \"")
        
        print("\nPossibly columns are not in correct order" )
    else:
        print("Success")