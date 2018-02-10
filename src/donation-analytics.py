import sys
import csv
from collections import defaultdict, namedtuple
import math
import argparse

def main(recFilePath,pctFilePath,outFilePath,logFilePath,logVerbose,modAccount):
    with open(pctFilePath, 'r') as pctFile, \
         open(recFilePath, 'r') as recFile, \
         open(outFilePath, 'w') as outFile, \
         open(logFilePath, 'w') as logFile:
         percentile = int(pctFile.readline().rstrip())
         divLine = '-'*79+'\n'
         print('Processing. Logging results in {:s}'.format(logFilePath))
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
         for rec in records:
             nRec += 1
             ValidRecord = getRecord(rec,nRec,selectedColumns,colID,
                                     nAllColumns,logFile)
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
         
         logFile.write(divLine+ 
                      'Gone through a total of {0:d} records. \n' 
                      'Processed {1:d} valid records. \n'
                      'Skipped   {2:d} invalid records.\n'
                      'DONE.'.format(nRec,nValid,nInvalid))

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
        #I coud have used an Insertion Sort routine here but I'll let timsort 
        #sort this out -- because it can automatically choose between
        #Merge Sort or Insertion Sort depending on sortedness of the input.
        try:
            outFile.write('{}|{}|{}|{}\n'.format(groupID,
                           findPercentileValue(sl,percentile,n),suml,n))
        except OSError as err:
            path = os.path.realpath(outFile.name)
            msg = ('Problem with output file {0}: {1} \n'.format(path,err))
            logFile.write(msg)
            raise OSError(msg)

def getRecord(record,lineNumber,selectedColumns,colID,
              nAllColumns,logFile,logVerbose=False):
    Record = namedtuple('Record', 'lineNumber length otherID name ' 
                                  'zipCode year recipient amount')
    theRecord = Record(lineNumber = lineNumber,
                       length     = len(record),
                       otherID    = record[colID['OTHER_ID']],
                       name       = record[colID['NAME']],
                       zipCode    = record[colID['ZIP_CODE']][0:5],
                       year       = record[colID['TRANSACTION_DT']][4:],
                       recipient  = record[colID['CMTE_ID']],
                       amount     = record[colID['TRANSACTION_AMT']])
 
    if isValid(nAllColumns,theRecord,logFile,logVerbose):
        donorID = theRecord.name+'|'+theRecord.zipCode
        groupID = theRecord.recipient+'|'+theRecord.zipCode+'|'+theRecord.year
        result = namedtuple('ValidRecord', 
                            ['donorID', 'groupID', 'amount', 'year'])
        return result(donorID,groupID,theRecord.amount,theRecord.year)

def isValid(nAllColumns,Record,logFile,logVerbose=False):

    result = False
    if Record.length != nAllColumns:
        #Check how much impact logVerbose checks have on speed.
        #Is there a way to bypass the checks entirely if logVerbose is False? 
        if logVerbose:
            msg = ('Skipping line {:d}' 
                   'because it has some missing fields.\n') \
                  .format(lineNumber)
            logFile.write(msg)
    elif Record.otherID not in (None, ''):
        if logVerbose:
            msg = ('Skipping line {:d}' 
                   'because "OTHER_ID" field is not empty.\n') \
                  .format(lineNumber)
            logFile.write(msg)
    #Doing only a loose check on names on purpose.
    #If an aggressive check is needed a validator package can be used.
    elif (Record.name is None or Record.name.isspace()):
        print('in')
        if logVerbose:
            msg = ('Skipping line {:d} because "NAME" field is blank. \n') \
                  .format(lineNumber)
            logFile.write(msg)
    elif any((Record.zipCode, Record.year, 
              Record.recipient, Record.amount)) in (None, ''):
        if logVerbose:
            msg = ('Skipping line {:d}'
                    'because a requested field is empty' 
                    'or it does not exist.\n') \
                  .format(lineNumber)
            logFile.write(msg)
    else:
        result=True

    return result

if __name__ == '__main__':
    '''
    Compute runnig percentile of repeat donations to campaigns.
    '''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v','--v', action='store_true', 
                        help='Output skipped records in the log file.')
    parser.add_argument('-m','--m', action='store_true', 
                        help='Modifies the accounting so that the donations '
                             'done within the same calendar year are counted '
                             'as repeat donation.')
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()
    #Add some input checks here:
    recFilePath = args.files[0]
    pctFilePath = args.files[1]
    outFilePath = args.files[2]
    logFilePath = args.files[3]
    logVerbose = args.v 
    modAccount = args.m 
    main(recFilePath,pctFilePath,outFilePath,logFilePath,
         logVerbose,modAccount)
    print('DONE.')
