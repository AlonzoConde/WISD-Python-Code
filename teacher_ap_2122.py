import xml.etree.ElementTree as ET
import csv


tree = ET.parse('app_not_equal_teacher.xml', ET.XMLParser(encoding='utf-8'))
root = tree.getroot()

final = []
final2 = []
tmp = []
tmp2 = []
tmp4 = []
x = 2


final3 = [['appraiser', 'teacher', 'EvaluationId', 'StartDate', 'EndDate', 'Comment', 'Comment2', 'Comment3', 'Comment4', 'Comment5', 'Comment6', 'Comment7', 'Comment8', 'Comment9', 'Comment10', 'Comment11', 'Comment12',
           'Comment13', 'Comment14', 'Comment15', 'Comment16', 'Comment17', 'Comment18', 'Comment19', 'Comment20', 'Comment21', 'Comment22', 'Comment23', 'Comment24', 'Comment25', 'Comment26', 'Comment27', 'Comment28']]


for child in root:
    tmp = []
    tmp2 = []
    x = 2
    for elem in child.iter():
        if str(elem.tag) == 'Comment' and str(elem.tag) in tmp:
            tmp.append(str(elem.tag) + str(x))

            x += 1
        else:
            tmp.append(str(elem.tag))
        tmp2.append(str(elem.text))

    final.append(tmp)
    final2.append(tmp2)


for i in range(0, len(final)):
    tmp4 = []
    for j in range(0, len(final[i])):
        for k in range(0, len(final3[0])):
            if final[i][j] == final3[0][k]:
                tmp4.append(final2[i][j])
    final3.append(tmp4)


with open('appraisals_21_22.csv', 'w', newline = '',encoding='utf-8') as fp:
    writer = csv.writer(fp, delimiter = ',')
    for row in final3:
        writer.writerow(row)