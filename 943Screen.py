import os
import csv

rows = []

# Not necessary, but used as a faster way to create new rows for the output CSV file
# Requires column index and value you want to input into said passed column
def createNewRow(stu_id, fNum, seqNum, fValue):
    newRow = [108913, stu_id, 943, fNum, seqNum, fValue]
    writer.writerow(newRow)

def checkStuID(stuID):
    if len(stuID) <= 5 and len(stuID) > 0:
        return True
    return False

def checkProgram(programName):
    accPrograms = ['Extended Day', 'Saturday School', 'In School Tutoring', 'Bilingual Enrichment']

    if programName in accPrograms:
        return True
    return False

def checkDate(dateEntered):
    if len(dateEntered) <= 10 and len(dateEntered) >= 8:
        return True
    return False

def checkMinutes(min):
    if min <= 999 and min >= 0:
        return True
    return False


def checkSubject(sub):
    accSubjects = ['ELA', 'Math', 'Science', 'SocStu', 'K3']

    if sub in accSubjects:
        return True
    return False


# CSV file the code will be reading from
# Each row found in the CSV file will be stored into "rows" for simpler data manipulation
with open('943Screen.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        rows.append(row)


#print(rows)

breakFlag = False
breakLocation = 0
breakReason = ""
exactProblem = ""

with open('up943.csv', 'w', newline='', encoding='UTF8') as f:
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
            # Program
            elif j == 1: 
                cProgram = checkProgram(rows[i][j])
                if cProgram != True:
                    breakFlag = True
                    breakLocation = i
                    breakReason = "Program"
                    exactProblem = rows[i][j]
                    break
                createNewRow(studentID, j, i, rows[i][j])
            # Date
            if j == 2: 
                cDate = checkDate(rows[i][j])
                if cDate != True:
                    breakFlag = True
                    breakLocation = i
                    breakReason = "Date"
                    exactProblem = rows[i][j]
                    break
                createNewRow(studentID, j, i, rows[i][j])
            # Minutes
            if j == 3: 
                cMinutes = checkMinutes(int(rows[i][j]))
                if cMinutes != True:
                    breakFlag = True
                    breakLocation = i
                    breakReason = "Minutes"
                    exactProblem = rows[i][j]
                    break
                createNewRow(studentID, j, i, rows[i][j])
            # Subject
            if j == 4: 
                cSubject = checkSubject(rows[i][j])
                if cSubject != True:
                    breakFlag = True
                    breakLocation = i
                    breakReason = "Subject"
                    exactProblem = rows[i][j]
                    break
                createNewRow(studentID, j, i, rows[i][j].strip())
    if breakFlag == True:
        print("Fix doc at Line: " + str(breakLocation+1))
        print("Problem Coumn: " + breakReason)
        print("Exact Reason: \" " + exactProblem + " \"")
        
        print("\nPossibly columns are not in correct order" )
        print("\nAnother possibility is that there's extra spaces (\" \") the SUBJECT column" )
    else:
        print("Success")