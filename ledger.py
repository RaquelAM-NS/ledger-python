import sys
from importlib import import_module
import re

arg = sys.argv
strData = ''
la = 3

def readFile(file):
    strDataFiles = ''
    try:
        reader = open(file, 'r')
        strReader = reader.read()
        if(strReader.find('!include') != -1):
            filesArray = strReader.replace('!include ', '').split('\n')
            for nameFile in filesArray:
                if(nameFile != ''):
                    try:
                        with open(nameFile, 'r') as readerFile:
                            strDataFiles = strDataFiles + readerFile.read()
                    finally:
                        readerFile.close()   
            return strDataFiles           
        else:
            strDataFiles = strReader
            return strDataFiles
    finally:
        reader.close()

def getAmount(amountString):
    amount = re.findall(r"[-+]?\d*\.\d+|\d+", amountString)[0] if len(re.findall(r"[-+]?\d*\.\d+|\d+", amountString)) != 0 else ''
    sign = '-' if amountString.find('-') != -1 else ''
    return sign + amount

def createDataStructure(strData):
    arrayLines = strData.replace('\t','').split('\n')
    arrayData = []
    movement = {}
    for i in arrayLines:
        if(i.find(';') != 0):
            match = re.search(r'(\d+/\d+/\d+)', i)
            if(match):
                if len(movement) != 0:
                    arrayData.append(movement.copy())
                    movement = {}
                if len(movement) == 0:
                    movement['date'] = i.split(' ')[0]
                    s = ' '
                    movement['description'] = s.join(i.split(' ')[1:])
            else:
                movement['account'+str(len(movement))] = {'accountName': i, 'amount': getAmount(i)}
    return arrayData

for i in range(len(arg)):
    if (arg[i].find('f')!= -1):
        strData = readFile(arg[i+1])
    if (arg[i].find('bal')!= -1):
        print(createDataStructure(strData))
    if (arg[i].find('reg')!= -1):
        print('call function register')
    if (arg[i].find('print')!= -1):
        print(strData)

