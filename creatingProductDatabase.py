import json
import random
import ast
import re
import csv


def returnGender(lines):
    json_as_list = "".join(lines).split('}')
    values = {}
    for elem in json_as_list:
         if len(elem) > 0:
             t = json.loads(json.dumps("{" + elem[::1]+"}"))
             t = eval(t)
             uid=t['uid']
             gender=t['gender']
             pagetype = t['page_type']
             if pagetype == 'product':
                if len(values)==0:
                    values[t['productId']] = [gender]
                elif t['productId'] in values:
                    values[t['productId']].append(gender)
                else:
                    values[t['productId']] = [gender]
    return values

def saveTrainedData(data,namefile):
    m=csv.writer(open(namefile,"wb"))
    for key in data:
        line = [key]
        for value in range((len(data[key]))):
            line.append(data[key][value])
        m.writerow(line)

def defineGender(data):
    gender = {}
    for key in data:
        F = []
        M = []
        for value in range((len(data[key]))):
            if data[key][value] == 'F':
                F.append(data[key][value])
            else:
                M.append(data[key][value])
        if len(F) >= len(M):
            gender[key] = ['F']
            gender[key].append(float(len(F))/(float(len(F)+len(M))))
        else:
            gender[key] = ['M']
            gender[key].append(float(len(M))/(float(len(F)+len(M))))
    return gender

       
    
x = open('data2','r')
lines = [re.sub("[\[\{\]]*","",one_object.rstrip()) for one_object in x.readlines()]
values = returnGender(lines)
saveTrainedData(values,"product2.csv")
gender = defineGender(values)
saveTrainedData(gender,"gender.csv")
