import os
import csv

# open csv file to read date

# store stu id

# write to new csv file line by line, keeping stu id, but updating info as i go

# delete first line of csv file (because not necessary for upload)



# Flags will be used to check if the CSV file bing read contins the necessary columns to process student data.
# "finalFlag" will not be a boolean value, it will be used to determine mor than two different situations 
newFlag = False
returnFlag = False
finalFlag = 0
sizeFlag = True

# Rows list will contain the entire CSV file being read. List will be formatted as a 2D list with the first index always containg the column headers:
# [
#   [student id, first name, last name, ADD, allergies, . . .],
#   [12345, john, smith, 'Y', 'N', . . .],
#   [],
# ]
rows = []

# Lists used along with flags in helping to find out if CSV file being read is acceptable or not
value1 = []
value2 = []
value3 = []

# Stores the indexes of new lines ('\n') found in the 'stu_LongtermMedExplain' column. If not dealt with, output CSV file will be unusable
# 'why' is used for Returning Student data
# 'why1' list is used for New Student data 
why = []
why1 = []

# List that stores the Required columns necessary from Powerschool Enrollment New Student extract. 
# Code will not execute if any of these columns are missing
# Notes: 1. 'stu_HomeShared' column can only be selected for New Student extract
#        2. 'stu_InsuranceGroup' and 'stu_InsurancePolicy' are never stored/used, but its easier to include when extracting from Powerschool
#        3. For New Student extract, columns MUST be in this order for code to properly execute
newRequiredFields = ['stu_HomeShared', 'stu_PKMilitary', 
    'stu_Insurance', 'stu_InsuranceCompany', 'stu_InsuranceGroup', 
    'stu_InsurancePolicy', 'stu_ADD', 'stu_Allergies', 'stu_Asthma', 
    'stu_Autism', 'stu_CerebralPalsy', 'stu_Diabetes', 'stu_DownsSyndrome', 
    'stu_Ear', 'stu_Epilepsy', 'stu_EyeGlasses', 'stu_FoodAllergies', 
    'stu_HeartDisease', 'stu_SpeechDisorder', 'stu_Epipen', 'stu_LongtermMed', 
    'stu_LongtermMedExplain', 'stu_TransportationAM', 'stu_TransportationPM', 
    'stu_CorporalPunishment']

# List that stores the Required columns necessary from Powerschool Enrollment Rturning Student extract.
# Code will not execute if any of these columns are missing
# Notes: 1. 'stu_HomeShared' is not available for Returning Student extract, so its ommitted in the extract 
#        2. 'stu_InsuranceGroup' and 'stu_InsurancePolicy' are never stored/used, but its easier to include when extracting from Powerschool
#        3. For Returning Student extract, columns MUST be in this order for code to properly execute
returnRequiredFields = ['stu_PKMilitary', 'stu_Insurance', 'stu_InsuranceCompany', 'stu_InsuranceGroup', 
    'stu_InsurancePolicy', 'stu_ADD', 'stu_Allergies', 'stu_Asthma', 
    'stu_Autism', 'stu_CerebralPalsy', 'stu_Diabetes', 'stu_DownsSyndrome', 
    'stu_Ear', 'stu_Epilepsy', 'stu_EyeGlasses', 'stu_FoodAllergies', 
    'stu_HeartDisease', 'stu_SpeechDisorder', 'stu_Epipen', 'stu_LongtermMed', 
    'stu_LongtermMedExplain', 'stu_TransportationAM', 'stu_TransportationPM', 
    'stu_CorporalPunishment']

# Lists that are used when determining whether input CSV file is a New Student or Returning student extract
# Note: Every extract will automatically include these fields, but we only care about the Student ID
returnIgnoreFields= [
    'Tags', 'Grade', 'Student ID', 'First Name', 'Submitted', 'Notes', 'Last Name', 'School', 'stu_HomeShared', 'Enroll Status'
]
newIgnoreFields= [
    'Tags', 'Grade', 'Student ID', 'First Name', 'Submitted', 'Notes', 'Last Name', 'School','Enroll Status'
]

# Dictionary used to connect column name with appropriate location in eSchool. Refer to eSchool for proper column matching:
# eSchool > Menu > Administration > General Setup > District > District Defined > 300-HAC Prereg Answers > Under the "Fields" section
position = {
    'stu_HomeShared':37, 
    'stu_PKMilitary':31, 
    'stu_InsuranceCompany':1, 
    'stu_Insurance':2, 
    'stu_ADD':4, 
    'stu_Allergies':7, 
    'stu_Asthma':10, 
    'stu_Autism':17, 
    'stu_CerebralPalsy':16, 
    'stu_Diabetes':13, 
    'stu_DownsSyndrome':5, 
    'stu_Ear':14, 
    'stu_Epilepsy':11, 
    'stu_EyeGlasses':8, 
    'stu_FoodAllergies':9, 
    'stu_HeartDisease':6, 
    'stu_SpeechDisorder':15, 
    'stu_Epipen':12, 
    'stu_LongtermMedExplain':40, 
    'stu_TransportationAM':25, 
    'stu_TransportationPM':26, 
    'stu_CorporalPunishment':28
}

# Not necessary, but used as a faster way to create new rows for the output CSV file
# Requires column index and value you want to input into said passed column
def createNewRow(index, value):
    newRow = [108913, stu_id, 300, index, 1, value]
    writer.writerow(newRow)

# Used to remove any new line ('\n') characters found given: the CSV input list (rows) and list of indexes where '\n' characters are found
# Example to follow:
# [
#   ["1234","John","Doe", ... , "asthma'\n'inhaler'\n'daily"]
# ]
# We will be focusing on this section: "asthma'\n'inhaler'\n'daily"
def iso(rij, k1):
    tmp = ''
    if len(k1) != 0:
        # Gets beginning of any item up to the first '\n' found. Adds space because thats what user intended to do.
        # From beginning of item to the first '\n': "asthma "
        tmp += str(rij[:k1[0]]) + ' '
        # Loops every time a '\n' is found and adds that to what we have so far up to the second to last index
        # What we found in loop: "inhaler "
        # What happens within loop after finding '\n': "asthma " + "inhaler "
        # What we have at end of loop: "asthma inhaler "
        for k in range(0, len(k1)-1):
            tmp += rij[[k1[k]+1][0]:[k1[k+1]][0]] + ' '
        # Once out of loop, add the final part of the intended item
        # Last part of item: "daily"
        # What final output will return: "asthma inhaler daily"
        tmp += rij[k1[len(k1)-1]+1:]
    return tmp

# CSV file code will be reading from
# Each row found in the CSV file will be stored into "rows" for simpler data manipulation
with open('300.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        rows.append(row)

# Checking to see 
for y in range(0, len(rows)):
    if len(rows[0]) != len(rows[y]):
        sizeFlag = False
        break

if sizeFlag is True:
    try:
        startIndexNew = 0
        missing = []
        extra = []
        startIndexNew = rows[0].index(newRequiredFields[0])
        for x in range(startIndexNew, len(newRequiredFields)+startIndexNew):
            if rows[0][x] != newRequiredFields[x - startIndexNew]:
                newFlag = False
                break
            newFlag = True
        value1 = list(set(rows[0]).difference(newIgnoreFields))
        value1 = list(set(newRequiredFields).difference(value1))
    except:
        print("")

    try:
        startIndexRet = 0
        startIndexRet = rows[0].index(returnRequiredFields[0])
        for x in range(startIndexRet, len(returnRequiredFields)+startIndexRet):
            if rows[0][x] != returnRequiredFields[x - startIndexRet]:
                returnFlag = False
                break
            returnFlag = True
        value2 = list(set(rows[0]).difference(returnIgnoreFields))
        value2 = list(set(returnRequiredFields).difference(value2))
    except:
        print("")
    
if newFlag is True:
    finalFlag = 1
elif returnFlag is True:
    finalFlag = 2


if finalFlag == 1:
    print("New Student")
    with open('up300.csv', 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        for i in range(1, len(rows)):
            stu_id = rows[i][0]       
            startIndex = 0 
            startIndex = rows[0].index(newRequiredFields[0])

            for j in range(startIndex, len(newRequiredFields)+startIndex):
                if stu_id != '':
                    if rows[0][j] == 'stu_CorporalPunishment': 
                        if rows[0][j] == 'stu_CorporalPunishment' and 'Y' in rows[i][j]:
                            createNewRow(position[rows[0][j]], 'Y')
                        else:
                            createNewRow(position[rows[0][j]], 'N')
                    elif rows[0][j] == 'stu_PKMilitary':
                        if rows[0][j] == 'stu_PKMilitary' and 'Y' in rows[i][j]:
                            createNewRow(position[rows[0][j]], 'Y')
                        else:
                            createNewRow(position[rows[0][j]], 'N')
                    elif rows[0][j] == 'stu_HomeShared':
                        if rows[0][j] == 'stu_HomeShared' and 'Y' in rows[i][j]:
                            createNewRow(position[rows[0][j]], 'Y')
                        else:
                            createNewRow(position[rows[0][j]], 'N')
                    elif rows[0][j] == 'stu_Insurance' or rows[0][j] == 'stu_InsuranceCompany' or rows[0][j] == 'stu_InsuranceGroup' or rows[0][j] == 'stu_InsurancePolicy':
                        if rows[0][j] == 'stu_InsuranceCompany':
                            rows[i][j] = rows[i][j].lower()
                        if 'medicaid' in rows[i][j] or 'Medicaid' in rows[i][j] or 'chip' in rows[i][j]:
                            createNewRow(1, 'Y')
                        elif rows[i][j] == 'y' or rows[i][j] == 'Y':
                            createNewRow(2, 'Y')
                        else:
                            continue
                    elif rows[0][j] == 'stu_LongtermMed' :
                        if 'y' in rows[i][j] or 'Y' in rows[i][j]:
                            if rows[0][j+1] == 'stu_LongtermMedExplain' and rows[i][j+1] != '':
                                if '\n' in rows[i][j+1] or ' ' in rows[i][j+1]:
                                    for k in range(0, len(rows[i][j+1])):
                                        if rows[i][j+1][k] == '\t' or rows[i][j+1][k] == '\n' or rows[i][j+1][k] == '' or rows[i][j+1][k] == ' ' or rows[i][j+1][k] == '\r':
                                            why1.append(k)
                                    r1 = iso(rows[i][j+1], why1)
                                    createNewRow(40, r1)
                                    why1.clear()
                        else:
                            continue
                    elif rows[0][j] == 'stu_TransportationAM':
                        if rows[0][j] == 'stu_TransportationAM':
                            if rows [i][j] == 'Bus':
                                createNewRow(position[rows[0][j]], 'Bus')
                            elif rows [i][j] == 'Drop Off':
                                createNewRow(position[rows[0][j]], 'Drop Off')
                            elif rows [i][j] == 'Walk':
                                createNewRow(position[rows[0][j]], 'Walk')
                    elif rows[0][j] == 'stu_TransportationPM':
                            if rows [i][j] == 'Bus':
                                createNewRow(position[rows[0][j]], 'Bus')
                            elif rows [i][j] == 'Pick Up':
                                createNewRow(position[rows[0][j]], 'Pick Up')
                            elif rows [i][j] == 'Walk':
                                createNewRow(position[rows[0][j]], 'Walk')  
                    else:
                        if 'y' in rows[i][j] or 'Y' in rows[i][j] and rows[0][j] != 'stu_LongtermMedExplain':
                            if rows[0][j] == 'stu_CorporalPunishment':
                                continue
                            elif rows[0][j] == 'stu_PKMilitary':
                                continue
                            elif rows[0][j] == 'stu_LongtermMedExplain':
                                continue
                            elif rows[0][j] == 'stu_LongtermMed':
                                continue
                            else:
                                createNewRow(position[rows[0][j]], 'Y')
                        else:
                            if rows[0][j] == 'stu_CorporalPunishment':
                               continue
                            elif rows[0][j] == 'stu_PKMilitary':
                                continue
                            elif rows[0][j] == 'stu_HomeShared':
                                continue 
elif finalFlag == 2:
    print("Returning Student")
    with open('up300.csv', 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        for i in range(1, len(rows)):
            stu_id = rows[i][0]
            startIndex = 0
            startIndex = rows[0].index(returnRequiredFields[0])

            for j in range(startIndex, len(returnRequiredFields)+startIndex):
                if stu_id != '':
                    if rows[0][j] == 'stu_CorporalPunishment': 
                        if rows[0][j] == 'stu_CorporalPunishment' and 'Y' in rows[i][j]:
                            createNewRow(position[rows[0][j]], 'Y')
                        else:
                            createNewRow(position[rows[0][j]], 'N')
                    elif rows[0][j] == 'stu_PKMilitary':
                        if rows[0][j] == 'stu_PKMilitary' and 'Y' in rows[i][j]:
                            createNewRow(position[rows[0][j]], 'Y')
                        else:
                            createNewRow(position[rows[0][j]], 'N') 
                    elif rows[0][j] == 'stu_Insurance' or rows[0][j] == 'stu_InsuranceCompany' or rows[0][j] == 'stu_InsuranceGroup' or rows[0][j] == 'stu_InsurancePolicy':
                        if rows[0][j] == 'stu_InsuranceCompany':
                            rows[i][j] = rows[i][j].lower()
                        if 'medicaid' in rows[i][j] or 'Medicaid' in rows[i][j] or 'chip' in rows[i][j]:
                            createNewRow(1, 'Y')
                        elif rows[i][j] == 'y' or rows[i][j] == 'Y':
                            createNewRow(2, 'Y')
                        else:
                            continue
                    elif rows[0][j] == 'stu_LongtermMed':
                        if 'y' in rows[i][j] or 'Y' in rows[i][j]:
                            if rows[0][j+1] == 'stu_LongtermMedExplain' and rows[i][j+1] != '':
                                if '\n' in rows[i][j+1] or ' ' in rows[i][j+1]:
                                    for k in range(0, len(rows[i][j+1])):
                                        if rows[i][j+1][k] == '\t' or rows[i][j+1][k] == '\n' or rows[i][j+1][k] == '' or rows[i][j+1][k] == ' ' or rows[i][j+1][k] == '\r':
                                            why.append(k)
                                    r = iso(rows[i][j+1], why)
                                    createNewRow(40, r)
                                    why.clear()
        #############################################################################################
                        else:
                            continue
                    elif rows[0][j] == 'stu_TransportationAM':
                        if rows[0][j] == 'stu_TransportationAM':
                            if rows [i][j] == 'Bus':
                                createNewRow(position[rows[0][j]], 'Bus')
                            elif rows [i][j] == 'Drop Off':
                                createNewRow(position[rows[0][j]], 'Drop Off')
                            elif rows [i][j] == 'Walk':
                                createNewRow(position[rows[0][j]], 'Walk')
                    elif rows[0][j] == 'stu_TransportationPM':
                            if rows [i][j] == 'Bus':
                                createNewRow(position[rows[0][j]], 'Bus')
                            elif rows [i][j] == 'Pick Up':
                                createNewRow(position[rows[0][j]], 'Pick Up')
                            elif rows [i][j] == 'Walk':
                                createNewRow(position[rows[0][j]], 'Walk')  
                    else:
                        if 'y' in rows[i][j] or 'Y' in rows[i][j] and rows[0][j] != 'stu_LongtermMedExplain':
                            if rows[0][j] == 'stu_CorporalPunishment':
                                continue
                            elif rows[0][j] == 'stu_PKMilitary':
                                continue
                            elif rows[0][j] == 'stu_LongtermMedExplain':
                                continue
                            elif rows[0][j] == 'stu_LongtermMed':
                                continue
                            else:
                                createNewRow(position[rows[0][j]], 'Y')
                        else:
                            if rows[0][j] == 'stu_CorporalPunishment':
                               continue
                            elif rows[0][j] == 'stu_PKMilitary':
                                continue                   
else:
    print("Error: Missing required fields from powerschool extract")
    value3 = list(set(rows[0]).difference(newIgnoreFields))
    value3 = list(set(returnRequiredFields).difference(value3))

    if value1 != [] and sizeFlag is False:
        print("Columns are misaligned")
        print(value1)
    elif value2 != [] and sizeFlag is False:
        print("Columns are misaligned")
        print(value2)
    elif value3 != [] and sizeFlag is False:
        print("Columns are misaligned")
        print(value3)
    elif value1 != []:
        print(value1)
    elif value2 != []:
        print(value2)
    elif value3 != []:
        print(value3)
    else:
        print("Columns are misaligned")
    os.system("pause")
