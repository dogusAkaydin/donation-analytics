"""Compute running percentile of repeat donors in a list streaming line-by-line."""

import sys
import csv
from collections import Counter

def main(inFilePath,outFilePath):
    
    inFile  =open(inFilePath, 'r')
    records =csv.reader(inFile,delimiter="|")
   
    headerFilePath ="indiv_header_file.csv" #Downloaded from FEC website.    
    with open(headerFilePath) as headerFile:
        allColumns=next(csv.reader(headerFile,delimiter=","))
    
    columnNamesOfInterest=['CMTE_ID','NAME','ZIP_CODE',
                           'TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID']
    columnNumbersOfInterest = [allColumns.index(aName) 
                               for aName in columnNamesOfInterest]
    
    colID = dict(zip(columnNamesOfInterest,columnNumbersOfInterest))
   
    donorCounter=Counter()
    for rec in records:
        if valid(rec):
            donorID=rec[colID['NAME']]+'|'+rec[colID['ZIP_CODE']][0:5]
            donorCounter[donorID]+=1
        else:
            continue
        
    print(donorCounter)


def valid(record):
    return True

if __name__ == "__main__":
    inFilePath  = sys.argv[1]
    outFilePath = sys.argv[2]
    main(inFilePath,outFilePath)



