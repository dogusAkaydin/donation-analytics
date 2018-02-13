# Insight Data Engineering Coding Challenge: Donation Analytics

## Table of Contents
1. [Summary of the Challenge](README.md#summary-of-the-challenge)
1. [Summary of the Algorithm and the Implementation](README.md#summary-of-the-algorithm-and-the-implementation)
1. [Tests](README.md#tests)
1. [Scalability](README.md#scalability)
1. [Summary](README.md#summary)

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


## Summary of the Algorithm and the Implementation:
The following algorithm is implemented using Python 3.6 came in Anaconda 3 distribution. 
Although I used an Anaconda distribution, I have only used modules that are present in standard 
Python 3.6 library.

1. Read the next available record and check if it is valid.
   1. If the record is valid mold it to `namedtuple` and return that data structure. 
      In this data structure, define each donor with a key (i.e. `donorID`) which is composed of 
      the donor's name and zip code.
      In addition, define each donation group with key (i.e. `groupID`) which is composed of the 
      recipient, donor's zip code and the donation year.
   1. If the record is not valid return null.
1. If a valid record is returned proceed to the next step. Otherwise loop back to Step 1.
1. Check if the donor is a repeat donor.
   A donor is a repeat donor if it's `donorID` is found as a key in  a `dict` called `donors` which 
   hash-maps each `donorID` to a `set` of years that the donor donated within<sup>\*</sup>.
   1. If the donor is a repeat donor, 
      1. Append the donation amount to a list hash-mapped to this `groupID` in a `dict`.
      1. Accordingly, increment a running sum which is hash-mapped to this `groupID` in another `dict`. 
      1. Compute the desired percentile value and emit the updated values in the format requested.
   1. If the donor is not a repeat donor, add that donor to the `donors` `dict`.
1. Add the donation year of that donor to its corresponding `set` of donation years.
1. Loop back to Step 1.

<sup>\*</sup>  *Dealing with ambiguity*: 
               By default, this set of years include all the years donor has made any donation to any
               recipient.
               The challenge rules, however, state that
  
               > if a donor had previously contributed to any recipient listed in the `itcont.txt` file 
                in any *prior* calendar year, that donor is considered a repeat donor.
               (*emphasis* is mine)

               This means that, if a donor has donated multiple times only within the current year, 
               those donations are NOT counted as repeat donations. 
               However, multiple donations within a prior year gets counted as repeat.
               This does not really make much sense. Nevertheless, I devised the command line 
               option `-s`, which sets `strictRepeat == True`, to allow for this type of an 
               accounting, just in case.
   
<sup>\*\*</sup> As per the challenge rules, there is no distiction made here as to which recipient 
               the donor donates to -- donations to any recipent qualifies as a repeat donation.



[Back to Table of contents](README.md#table-of-contents)


## Summary of the Implementation:


[Back to Table of contents](README.md#table-of-contents)


## Tests:


[Back to Table of contents](README.md#table-of-contents)


## Scalability:


[Back to Table of contents](README.md#table-of-contents)


## Summary:


[Back to Table of contents](README.md#table-of-contents)


