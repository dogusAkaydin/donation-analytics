#!/usr/bin/env python3
'''
Insight Data Engineering coding challenge:

Compute running percentile of repeat donations to 
US political campaigns based on FEC data.
'''
import sys
import csv
from collections import namedtuple
import math
import time
import datetime

def main(recFilePath,pctFilePath,outFilePath,logFilePath,logVerbose,modAccount):
    t0wall = time.time()
    with open(pctFilePath, 'r') as pctFile, \
         open(recFilePath, 'r') as recFile, \
         open(outFilePath, 'w') as outFile, \
         open(logFilePath, 'w') as logFile:
         percentile = int(pctFile.readline().rstrip())
         divLine = '-'*79+'\n'
         print('Processing. See process logs in {:s}'.format(logFilePath))
         logFile.write('Opened \n' 
                    '{0:s} \n' 
                    'to output the repeat donation stats in the '
                    'following format: \n'
                    '| Receipent | Donors'' Zip Code| Donation Year' 
                    '| {1:d} Percentile Amount '
                    '| Total Repeat Donation Amount' 
                    '| Number of Repeat Donations \n'
                    'The requested percentile value is read from: \n'
                    '{2:s} \n' 
                     .format(outFilePath,percentile,pctFilePath))

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
         repeatCount = {}
         repeatSum = {}
         #repeatDonations=defaultdict(list)
         nRec = 0
         nValid = 0
         nInvalid = 0
         msg = ('Started processing records present in: \n'
                '{:s} \n'
                'See the end of this log file for a process summary. \n'
                +divLine) \
                .format(recFilePath)
         logFile.write(msg)
         if not logVerbose:
             msg = ('Use command line option -v to see verbose output here.\n')
             logFile.write(msg)
         #This loop is where the line-by-line inspection happens: 
         for rec in records:
             t0_proc0 = time.time()
             nRec += 1
             ValidRecord = getRecord(rec,nRec,selectedColumns,colID,
                                     nAllColumns,logFile,logVerbose)
             if ValidRecord:  
                 if ValidRecord.donorID in donors:
                     amt = int(ValidRecord.amount)
                     repeatDonations.setdefault(ValidRecord.groupID,[]).append(amt)
                     repeatCount[ValidRecord.groupID] = repeatCount.setdefault(ValidRecord.groupID,0) + 1
                     repeatSum[ValidRecord.groupID]   = repeatSum.setdefault(ValidRecord.groupID,0) + amt
                     #repeatDonations[ValidRecord.groupID].append(int(amt))
                     emit = True
                     nSort    = len(repeatDonations[ValidRecord.groupID])
                     t0_proc1 = time.time()
                     emitStats(ValidRecord.groupID, 
                               repeatDonations[ValidRecord.groupID],
                               repeatCount[ValidRecord.groupID],
                               repeatSum[ValidRecord.groupID],
                               percentile,outFile,logFile)
                     t1_proc1 = time.time()
                 else:
                     emit = False
                     nSort = 0
                     t0_proc1 = time.time()
                     donors[ValidRecord.donorID] = set()
                     t1_proc1 = time.time()
                 donors[ValidRecord.donorID].add(ValidRecord.year)
                 nValid += 1
             else:
                 nInvalid += 1
                 continue
             t1_proc0 = time.time()
             dt_proc1 = t1_proc1 - t0_proc1
             dt_proc0 = t1_proc0 - t0_proc0
             ratio    = 100.0*dt_proc1/dt_proc0
             msg=('{0:10d}: Emit: {1:2}, nSort = {5:7d}, dt_proc0 = {2:10f}, dt_proc1 = {3:10f}, ratio = {4:5.2f} \n' \
                 .format(nRec,emit,dt_proc0,dt_proc1,ratio,nSort))
             #logFile.write(msg)
         dtWall = time.time() - t0wall
         msg = (divLine+ 
                'Gone through a total of {0:d} records. \n' 
                'Processed {1:d} valid records. \n'
                'Skipped   {2:d} invalid records.\n'
                'DONE in {3:f} seconds of wall clock time '
                .format(nRec,nValid,nInvalid,dtWall))
         logFile.write(msg)
    return dtWall

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

def emitStats(groupID, donations,cnt,tot,percentile,outFile,logFile):
    #for groupID, amounts in donations.items():
        #This list is sorted except for the last appended item.
        #donations[groupID].sort()
        #I coud have used an Insertion Sort routine here but I'll let timsort 
        #sort this out -- because it can automatically choose between
        #Merge Sort or Insertion Sort depending on sortedness of the input.
        #sortedList = donations[groupID]
        #nL   = len(sortedList)
        #sumL = sum(sortedList)
        #outFile.write('{}|{}|{}|{}\n'.format(groupID,
        #               findPercentileValue(sortedList,percentile,nL),sumL,nL))
        #nL   = cnt[groupID]
        #sumL = tot[groupID]
        #outFile.write('{}|{}|{}|{}\n'.format(groupID,
        #               findPercentileValue(donations[groupID],percentile,nL),sumL,nL))
        donations.sort()
        outFile.write('{}|{}|{}|{}\n'.format(groupID,
                       findPercentileValue(donations,percentile,cnt),tot,cnt))

def getRecord(record,lineNumber,selectedColumns,colID,
              nAllColumns,logFile,logVerbose):
    Record = namedtuple('Record', 'lineNumber length otherID name ' 
                                  'fullZipCode date recipient amount')
    theRecord = Record(lineNumber = lineNumber,
                       length     = len(record),
                       otherID    = record[colID['OTHER_ID']],
                       name       = record[colID['NAME']],
                       fullZipCode= record[colID['ZIP_CODE']],
                       date       = record[colID['TRANSACTION_DT']],
                       recipient  = record[colID['CMTE_ID']],
                       amount     = record[colID['TRANSACTION_AMT']])
 
    if isValid(nAllColumns,theRecord,logFile,logVerbose):
        zipCode=theRecord.fullZipCode[0:5]
        year=theRecord.date[4:8]
        donorID = theRecord.name+'|'+zipCode
        groupID = theRecord.recipient+'|'+zipCode+'|'+year
        result = namedtuple('ValidRecord', 
                            ['donorID', 'groupID', 'amount', 'year'])
        return result(donorID,groupID,theRecord.amount,year)

def isValid(nAllColumns,Record,logFile,logVerbose=False):
    result = False #A record enters and remains invalid unless it passes all these tests:
    if Record.length != nAllColumns:
        #Measure how much impact logVerbose checks have on speed.
        #Is there a way to bypass the checks entirely if logVerbose is False? 
        if logVerbose:
            msg = ('Skipping record line {:d} ' 
                   'because it has some missing fields.\n') \
                  .format(Record.lineNumber)
            logFile.write(msg)
    elif Record.otherID not in (None, ''):
        if logVerbose:
            msg = ('Skipping record {:d} ' 
                   'because "OTHER_ID" field is not empty.\n') \
                  .format(Record.lineNumber)
            logFile.write(msg)
    elif (Record.name is None or Record.name.isspace()):
        #Doing only a loose check on names on purpose.
        #If an aggressive check is needed a validator package can be used.
        if logVerbose:
            msg = ('Skipping record {:d} ' 
                   'because "NAME" field is blank. \n') \
                  .format(Record.lineNumber)
            logFile.write(msg)
    elif (len(Record.fullZipCode) < 5 
          or not Record.fullZipCode[0:5].isdecimal()): 
        #This will let in an entry like "94040-FOOBAR", which I thought is OK.
        if logVerbose:
            msg = ('Skipping record {:d} ' 
                   'because "ZIP_CODE" field is malformed. \n') \
                  .format(Record.lineNumber)
            logFile.write(msg)
    elif (Record.date is None or Record.date.isspace()):
        if logVerbose:
            msg = ('Skipping record {:d} ' 
                   'because "TRANSACTION_DT" field is empty \
                                                   or it does not exist. \n') \
                  .format(Record.lineNumber)
            logFile.write(msg)
    elif (Record.amount is None 
          or Record.amount.isspace()
          or not isNumber(Record.amount)
          or int(Record.amount)<=0): # 0-contribution is no contribution.
        #Doing only a loose check on names on purpose.
        #If an aggressive check is needed a validator package can be used.
        if logVerbose:
            msg = ('Skipping record {:d} ' 
                   'because "TRANSACTION_AMT" field is malformed ' 
                                                  'or non-positive. \n') \
                  .format(Record.lineNumber)
            logFile.write(msg)
    elif Record.recipient is None or Record.recipient.isspace():
        if logVerbose:
            msg = ('Skipping record {:d} '
                   'because CMTE_ID field is missing or empty \n') \
                  .format(Record.lineNumber)
            logFile.write(msg)
    else:
        try: #One more check on date to catch it if malformed.
            date=datetime.datetime.strptime(Record.date, '%m%d%Y')
        except ValueError:
            if logVerbose:
                msg = ('Skipping record {:d} ' 
                       'because "TRANSACTION_DT" field is malformed. \n') \
                      .format(Record.lineNumber)
                logFile.write(msg)
        else:
            result=True

    return result

def isNumber(s):
    try:
        res=float(s)
        return False if res is float('NaN') else True
    except ValueError:
        return False

if __name__ == '__main__':
    '''Command-line execution for donation-analytics.py'''

    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('recFilePath', 
                        help='Path to the record file provided by FEC')
    parser.add_argument('pctFilePath', 
                        help='Path to the file that holds the desired \
                              percentile value between 0 and 100.')
    parser.add_argument('outFilePath', 
                        help='Path to the file where the repeat donation \
                              results are written to.')
    parser.add_argument('logFilePath', 
                        help='Path to the file where a log of process \
                             (stats, skipped lines, etc.) are written to.')
    parser.add_argument('-v','--v', action='store_true', 
                        help='Outputs any skipped records in the log file.')
    parser.add_argument('-m','--m', action='store_true', 
                        help='Modifies the accounting so that the donations '
                             'done within the same calendar year are counted '
                             'as repeat donation.')
    args = parser.parse_args()
    #Add some input checks here:
    logVerbose = args.v 
    modAccount = args.m 
    recFilePath = args.recFilePath
    pctFilePath = args.pctFilePath
    outFilePath = args.outFilePath
    logFilePath = args.logFilePath
    dtWall = main(recFilePath,pctFilePath,outFilePath,logFilePath,
                  logVerbose,modAccount)
    print('DONE in {0:10g} seconds of wall clock time'.format(dtWall))
