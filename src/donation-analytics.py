"""Compute running percentile of repeat donors in a list streaming line-by-line."""

import sys
import csv
from collections import Counter, defaultdict

def main(inFilePath,outFilePath):
    
    inFile  =open(inFilePath, 'r')
    records =csv.reader(inFile,delimiter='|')
   
    headerFilePath ='indiv_header_file.csv' #Downloaded from FEC website.    
    with open(headerFilePath) as headerFile:
        allColumns=next(csv.reader(headerFile,delimiter=','))
    
    columnNamesOfInterest=['CMTE_ID','NAME','ZIP_CODE',
                           'TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID']
    columnNumbersOfInterest = [allColumns.index(aName) 
                               for aName in columnNamesOfInterest]
    
    colID = dict(zip(columnNamesOfInterest,columnNumbersOfInterest))
  
    donors = {} #For Method 1 and Method 3
    #donors = defaultdict(set) #For Method 2
    donorCounter=Counter() 
    repeatDonations=defaultdict(list)
    for rec in records:
        if isValid(rec):
            name     =rec[colID['NAME']]
            zipCode  =rec[colID['ZIP_CODE']][0:5]
            year     =rec[colID['TRANSACTION_DT']][4:]
            receipent=rec[colID['CMTE_ID']]
            amt      =rec[colID['TRANSACTION_AMT']]
            #donorIDperYear=name+'|'+zipCode
            donorID=name+'|'+zipCode
            groupID=receipent+'|'+zipCode+'|'+year
            #Method 1: setdefault
            #donors.setdefault(donorID,[]).append(year)
            #Method 2: defaultdict
            #donors[donorID].add(year)
            #Method 3: Build dict for donations while identifying repeat donors
            #donors[donorID].append(year)
            try: 
               donors[donorID].append(year)
               repeatDonations[groupID].append(int(amt))
               updatePercentiles(repeatDonations)
            except KeyError:
               donors[donorID] = []
               donors[donorID].append(year)
        else:
            continue

def isValid(record):
    return True

def pctl(sortedList, percentile):
    return percentile

def updatePercentiles(donations):
    for groupID, amounts in donations.items():
        #This list is sorted except for the last appended item.
        donations[groupID].sort()
        sl=donations[groupID]
        #I coud have used Insertion Sort but I'll let
        #timsort do it -- because it can automatically 
        #sense the sortedness of the list and choose the
        #most efficient algorithm (Merge Sort or Insertion Sort)
        print('{}|{}|{}|{}'.format(groupID,pctl(sl,pc),sum(sl),len(sl)))
    return True

if __name__ == '__main__':
    inFilePath  = sys.argv[1]
    outFilePath = sys.argv[2]
    main(inFilePath,outFilePath)



