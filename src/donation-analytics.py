"""Compute running percentile of repeat donors in a list streaming line-by-line."""
import sys
import csv
from collections import Counter, defaultdict
import math

def main(inFilePath,pctFilePath,outFilePath):
 
    headerFilePath ='indiv_header_file.csv' #Downloaded from FEC website.    
    with open(headerFilePath) as headerFile:
        allColumns=next(csv.reader(headerFile,delimiter=','))
   
    with open(pctFilePath) as pctFile:
        percentile=int(pctFile.readline().rstrip())
 
    with  open(inFilePath) as inFile:
        records =csv.reader(inFile,delimiter='|')
         
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
                   updatePercentiles(repeatDonations,percentile)
                except KeyError:
                   donors[donorID] = []
                   donors[donorID].append(year)
            else:
                continue

def isValid(record):
    return True

def compPctl(sortedList,percentile,n):
    idx=math.ceil((percentile/100.0)*n)-1 #-1 since the list is 0-based.
    return sortedList[idx]

def updatePercentiles(donations,pc):
    for groupID, amounts in donations.items():
        #This list is sorted except for the last appended item.
        donations[groupID].sort()
        sl=donations[groupID]
        n=len(sl)
        suml=sum(sl)
        '''
        I coud have used an Insertion Sort routine here but 
        I'll let timsort do it -- because it can automatically 
        sense the sortedness of the list and choose between 
        Merge Sort or Insertion Sort.
        '''
        print('{}|{}|{}|{}'.format(groupID,compPctl(sl,pc,n),suml,n))
    return True

if __name__ == '__main__':
    inFilePath  = sys.argv[1]
    pctFilePath = sys.argv[2]
    outFilePath = sys.argv[3]
    main(inFilePath,pctFilePath,outFilePath)

