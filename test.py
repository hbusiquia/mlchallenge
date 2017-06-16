import json
import random
import ast
import re
import csv


def returnProductId(lines):
    json_as_list = "".join(lines).split('}')
    values = {}
    for elem in json_as_list:
         if len(elem) > 0:
             t = json.loads(json.dumps("{" + elem[::1]+"}"))
             t = eval(t)
             uid = t['uid']
             page_type = t['page_type']
             if page_type == 'product':
                if len(values)==0:
                    values[uid] = [t['productId']]
                elif uid in values:
                    if t['productId'] not in values[uid]:
                        values[uid].append(t['productId'])
                else:
                    values[uid] = [t['productId']]
    return values

def saveTrainedData(data):
    c = csv.writer(open("uid.csv","wb"))
    for uid in range(len(data)):
        line = data[uid]
        c.writerow(line)

def returnGender(filename):
    m = csv.reader(open(filename,"r"))
    gender = {}
    for row in m:
        gender[row[0]] = [row[1]]
        if len(row) > 2:
            gender[row[0]].append(row[2])
    return gender

def testGender(values,gender):
    result = {}
    for key in values:
        for product in values[key]:
            gen = [gender[product][0],gender[product][1]]
            if len(result) == 0:
                result[key] = []
                result[key].append(gen)
            elif key in result:
                result[key].append(gen)
            else:
                result[key] = []
                result[key].append(gen)
        
    return result

def defineGender(data):
    gender = {}
    for key in data:
        F = []
        M = []
        for value in range((len(data[key]))):
            if data[key][value][0] == 'F':
                F.append(data[key][value][0])
            else:
                M.append(data[key][value][0])
        if len(F) >= len(M):
            gender[key] = ['F']
        else:
            gender[key] = ['M']
    return gender

def saveResult(data,namefile):
    m=csv.writer(open(namefile,"wb"))
    for key in data:
        line = [key]
        for value in range((len(data[key]))):
            line.append(data[key][value])
        m.writerow(line)
   
x = open('target2','r')
lines = [re.sub("[\[\{\]]*","",one_object.rstrip()) for one_object in x.readlines()]    
values = returnProductId(lines)
genderProduct = returnGender("gender.csv")
databaseGender = returnGender("result2.csv")
uidgender = testGender(values,genderProduct)
uidgender2 = defineGender(uidgender)
saveResult(uidgender2,"result12.csv")
