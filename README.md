# Insight Data Engineering Coding Challenge: Donation Analytics

## Table of Contents
1. [Summary of the Challenge](README.md#summary-of-the-challenge)
2. [Summary of the Algorithm](README.md#summary-of-the-algorithm)
3. [Summary of the Implementation](README.md#summary-of-the-implemention)
4. [Tests](README.md#tests)
5. [Scalability](README.md#scalability)
6. [Summary](README.md#summary)

## Summary of the Challenge:
A series of donation records stream in from a file, line-by-line. 
Each record lists some information about the donor, the recipient and the donation. 
As each record comes in, emit the following as a new line in a file if the donor is a repeat donor: 

    Recipient|Zip|Year|Repeat Donation x-Percentile Amt.|Repeat Donation Total Amt.|# Rep. Donations 

The percentile value used when finding `x-Percentile Amt.` will be read from a file. 
Assume that the records can have missing or malformed data so do some validity checks to skip such 
records.

See [the full description of the challenge](https://github.com/InsightDataScience/donation-analytics/blob/master/README.md).

[Back to Table of contents](README.md#table-of-contents)


## Summary of the Algorithm:

1. Read the next available record and check if it is valid.
  1. If the record is valid mold it to a data structure and return that data structure.
     In this data structure, define each donor with a key (i.e. `donorID`) which is composed of 
     the donor's name and zip code.
     In addition, define a donation group with a key (i.e. `groupID`) which is composed of the 
     recipient, donor's zip code and the donation year.
  2. If the record is not valid return None.
2. If a valid record is returned proceed to the next step. Otherwise loop back to Step 1.
3. Check if the donor is a repeat donor 
   1. If the donor is a repeat donor,
      1. Append the donation amount to a list hash-mapped to this `groupID`.
      2. Increment a running sum, which is hash-mapped to this `groupID`, by this donation amount.
      3. Compute the desired percentile value and emit the updated values in the format requested.
   2. If the donor is not a repeat donor, add that donor to the `donors` hash-map.
5. Add the donation year of that donor to its corresponding set of donation years.
6. Loop back to Step 1.

@if it is a key in a `donors` hash-map that maps each `donorID` 
         to a set of years that the donor donated within.

[Back to Table of contents](README.md#table-of-contents)


## Summary of the Implementation:


[Back to Table of contents](README.md#table-of-contents)


## Tests:


[Back to Table of contents](README.md#table-of-contents)


## Scalability:


[Back to Table of contents](README.md#table-of-contents)


## Summary:


[Back to Table of contents](README.md#table-of-contents)


