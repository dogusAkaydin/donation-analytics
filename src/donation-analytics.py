"""Compute running percentile of repeat donors in a list streaming line-by-line."""
import sys
import csv
from collections import defaultdict, namedtuple
import math

def main(recFilePath,pctFilePath,outFilePath,logFilePath):
   
    with open(pctFilePath) as pctFile:
        percentile = int(pctFile.readline().rstrip())
   
    logFile = open(logFilePath, 'w')

    try:
        outFile = open(outFilePath, 'w')
    except OSError:
        logFile.write('Can not open {0:s} to write.'.format(outFilePath))
    else:
        logFile.write('Opened {0:s} to record repeat donations' 
                      'in this format: \n'
                      '| Receipent | Donors'' Zip Code| Donation Year' 
                      '| {1:d} Percentile Amount | Total Repeat Donation Amount' 
                      '| Number of Repeat Donations' 
                       .format(outFilePath,percentile))
    

    with open(recFilePath) as recFile:
        records = csv.reader(recFile,delimiter='|')
        selectedColumns = ['CMTE_ID',
                           'NAME',
                           'ZIP_CODE',
                           'TRANSACTION_DT',
                           'TRANSACTION_AMT',
                           'OTHER_ID']
        colID, nAllColumns = getColumnIDs(selectedColumns)
        donors = {}
        repeatDonations = {}
        #repeatDonations=defaultdict(list)
        nRec = 0
        nValid = 0
        nInvalid = 0
        logFile.write('Started processing records in: {:s} \n' 
                       .format(recFilePath))
        for rec in records:
            nRec += 1
            ValidRecord = getRecord(rec,nRec,selectedColumns,colID,nAllColumns,logFile)
            if ValidRecord:  
                if ValidRecord.donorID in donors:
                    repeatDonations.setdefault(ValidRecord.groupID,[]) \
                                   .append(int(ValidRecord.amount))
                    #repeatDonations[ValidRecord.groupID].append(int(amt))
                    emitStats(repeatDonations,percentile,outFile)
                else:
                    donors[ValidRecord.donorID] = set()
                donors[ValidRecord.donorID].add(ValidRecord.year)
                nValid += 1
            else:
                nInvalid += 1
                continue
    outFile.close()
    
    logFile.write('Gone through a total of {0:d} records. \n' 
                  'Processed {1:d} valid records. \n'
                  'Skipped   {2:d} invalid records.\n'
                  'DONE.'.format(nRec,nValid,nInvalid))
    logFile.close()

def getColumnIDs(selectedColumns):
    headerFilePath = 'indiv_header_file.csv' #Downloaded from FEC website.    
    with open(headerFilePath) as headerFile:
        allColumns = next(csv.reader(headerFile,delimiter=','))
    try:  
        selectedNumbers = [allColumns.index(aColumn) 
                           for aColumn in selectedColumns]
    except ValueError as err:
        msg = ('The column you requested, {0}, does not exist' 
               'in the header file: {1} \n'
               'These are column names I found in the header file: \n'
               '{2}'.format(aColumn,headerFilePath,allColumns))
        logFile.write(msg)
        raise OSError(msg)
        
    return dict(zip(selectedColumns,selectedNumbers)), len(allColumns)

def findPercentileValue(sortedList,percentile,n):
    idx = math.ceil((percentile/100.0)*n)-1 #-1 since the list is 0-based.
    return sortedList[idx]

def emitStats(donations,percentile,outFile):
    for groupID, amounts in donations.items():
        #This list is sorted except for the last appended item.
        donations[groupID].sort()
        sl = donations[groupID]
        n = len(sl)
        suml = sum(sl)
        '''
        I coud have used an Insertion Sort routine here but I'll let timsort 
        sort this out -- because it can automatically choose between
        Merge Sort or Insertion Sort depending on sortedness of the input.
        '''
        try:
            outFile.write('{}|{}|{}|{}\n'.format(groupID,
                           findPercentileValue(sl,percentile,n),suml,n))
        except OSError as err:
            path = os.path.realpath(outFile.name)
            msg = ('Problem with output file {0}: {1} \n'.format(path,err))
            logFile.write(msg)
            raise OSError(msg)

def getRecord(record,lineNumber,selectedColumns,colID,nAllColumns,logFile):
    name      = record[colID['NAME']]
    zipCode   = record[colID['ZIP_CODE']][0:5]
    year      = record[colID['TRANSACTION_DT']][4:]
    receipent = record[colID['CMTE_ID']]
    amount    = record[colID['TRANSACTION_AMT']]
    donorID   = name+'|'+zipCode
    groupID   = receipent+'|'+zipCode+'|'+year
    if record[colID['OTHER_ID']] not in (None, ''):
        logFile.write('"OTHER_ID" not empty. Skipping line:{:d} \n'.format(lineNumber))
        return None
    result=namedtuple('ValidRecord', ['donorID', 'groupID', 'amount', 'year'])
    return result(donorID,groupID,amount,year)

if __name__ == '__main__':
    recFilePath=sys.argv[1]
    pctFilePath=sys.argv[2]
    outFilePath=sys.argv[3]
    logFilePath=sys.argv[4]
    main(recFilePath,pctFilePath,outFilePath,logFilePath)
