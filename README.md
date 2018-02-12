# Insight Data Engineering Coding Challenge: Donation Analytics

## Table of Contents
1. [Summary of the Challenge](README.md#summary-of-the-challenge)
2. [Summary of the Algorithm](README.md#summary-of-the-algorithm)
3. [Summary of the Implementation](README.md#summary-of-the-implemention)
4. [Tests](README.md#tests)
5. [Scalability](README.md#scalability)
6. [Summary](README.md#summary)

## Summary of the Challenge:
A series of donation records stream in from a file, line-by-line. Each record lists some information about the donor, the recipient and the donation. 
As each record comes in, emit the following as a new line in a file if the donor is a repeat donor: 

    Recipient|Zip|Year|Repeat Donation x-Percentile Amt.|Repeat Donation Total Amt.|# Rep. Donations 

The percentile value used when finding `x-Percentile Amt.` will be read in from a file. 

Assume that the records can have missing or malformed data and do validity checks.

See [the full desription of the challenge](https://github.com/InsightDataScience/donation-analytics/blob/master/README.md).

[Back to Table of contents](README.md#table-of-contents)


## Summary of the Algorithm:

1. If the current record is valid, proceed to the next step. Otherwise, skip to the next record.
2. If the donor is a repeat donor, append the donation amount to list hash-mapped to donation key. 
The key is composed of the recipient name, donor zip code and the donation year.  
3. If the donor is not a repeat donor, add that donor to a hash-map which maps each donor to a set of years she/he donated.
4. Add the donation year of that donor to its corresponding set of donation years.




[Back to Table of contents](README.md#table-of-contents)


## Summary of the Implementation:


[Back to Table of contents](README.md#table-of-contents)


## Tests:


[Back to Table of contents](README.md#table-of-contents)


## Scalability:


[Back to Table of contents](README.md#table-of-contents)


## Summary:


[Back to Table of contents](README.md#table-of-contents)


