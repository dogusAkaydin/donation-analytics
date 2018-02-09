"""Compute running percentile of repeat donors in a list streaming line-by-line."""
import sys
import csv
from collections import defaultdict
import math

def main(recFilePath,pctFilePath,outFilePath):
   
    with open(pctFilePath) as pctFile:
        percentile=int(pctFile.readline().rstrip())
   
    outFile = open(outFilePath, 'w')
      
    with open(recFilePath) as recFile:
        records =csv.reader(recFile,delimiter='|')
        receipentCol='CMTE_ID'
        donorNameCol='NAME'
        zipCodeCol  ='ZIP_CODE'
        donDateCol  ='TRANSACTION_DT'
        donAmtCol   ='TRANSACTION_AMT'
        otherIDcol  ='OTHER_ID'
        selectedColumns=[receipentCol,donorNameCol,zipCodeCol,donDateCol,donAmtCol,otherIDcol]  
        colID = getColumnIDs(selectedColumns)
 
        donors={}
        repeatDonations={}
        #repeatDonations=defaultdict(list)
        for rec in records:
            if isValid(rec):
                name     =rec[colID[donorNameCol]]
                zipCode  =rec[colID[zipCodeCol]][0:5]
                year     =rec[colID[donDateCol]][4:]
                receipent=rec[colID[receipentCol]]
                amt      =rec[colID[donAmtCol]]
                donorID  =name+'|'+zipCode
                groupID  =receipent+'|'+zipCode+'|'+year
                if donorID in donors:
                    repeatDonations.setdefault(groupID,[]).append(int(amt))
                    #repeatDonations[groupID].append(int(amt))
                    emitStats(repeatDonations,percentile,outFile)
                else:
                    donors[donorID] = set()
                donors[donorID].add(year)
                '''
                try: 
                   donors[donorID].append(year)
                   repeatDonations[groupID].append(int(amt))
                   updatePercentiles(repeatDonations,percentile)
                except KeyError:
                   donors[donorID]=[]
                   donors[donorID].append(year)
                '''
            else:
                continue

def getColumnIDs(selectedColumns):
    headerFilePath ='indiv_header_file.csv' #Downloaded from FEC website.    
    with open(headerFilePath) as headerFile:
        allColumns=next(csv.reader(headerFile,delimiter=','))
      
    selectedNumbers=[allColumns.index(aColumn) 
                     for aColumn in selectedColumns]
    return dict(zip(selectedColumns,selectedNumbers))

def findPercentileValue(sortedList,percentile,n):
    idx=math.ceil((percentile/100.0)*n)-1 #-1 since the list is 0-based.
    return sortedList[idx]

def emitStats(donations,percentile,outFile):
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
        outFile.write('{}|{}|{}|{}\n'.format(groupID,
                                      findPercentileValue(sl,percentile,n),
                                      suml,n))
    return True

def isValid(record):
    return True

if __name__ == '__main__':
    recFilePath=sys.argv[1]
    pctFilePath=sys.argv[2]
    outFilePath=sys.argv[3]
    main(recFilePath,pctFilePath,outFilePath)
