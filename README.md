# Financial Marketplace Referee (FMR)

## Context

The Consumer Financial Protection Bureau (CFPB) publishes a public [consumer complaint database](http://www.consumerfinance.gov/data-research/consumer-complaints/ CFPB Consumer Complaint Database) consisting of complaints relating to financial services products and companies. Unscrupulous companies sometimes take advantage of consumers through predatory or discriminatory product offerings and targeting, leading to the consumers lodging complaints against these products and companies to the CFPB. <p>

By enriching the consumer complaint dataset with population demographic statistics sourced from the [American Community Survey](https://www.census.gov/programs-surveys/acs/ American Community Survey), our research shows that there exist notable relationships between companies that have received complaints from those geographical regions with the largest minority populations (on the 5-digit zipcode granulatity) and the companies that are eventually charged with discriminatory product offerings. <p>

Most notably, we show that our analysis can help identify companies that possibly offer predatorial, fraudulent, and racially discriminatory financial products. This can help influence policy and investigation decisions by financial regulatory bodies, and help consumers get better access to data about the suspiciousness of a financial vendor.<p>

## Description

**__Financial Marketplace Referee__** is an application toolset that performs analysis on the latest CFPB consumer complaint database and ASR zipcode demographic statistics to inform the user of companies that are suspected to be involved in financial foul play.

There are two analysis modules that can be executed:
  1. Complaint Volume
    * This module analyzes the data without reference to demographics and flags company suspiciousness based on the number of complaints lodged against it.
  2. Racial Discrimination
    * This module attempts to find patterns of complaints that could indicate a company is discriminating against minority groups. Joining against the ACS database, this analysis module finds companies with abnormally high numbers of complaints from geographic regions with the largest minority populations. This module can both find potentially risky companies for a given product line, and can score a single company on all product lines which they offer.

Each of these modules allow the user to ask two questions:
  1. Is company X bad?
    * This suggests to the user if the company is suspected to be offering "bad" products across a range of product lines.
  2. For a particular product line, (e.g. Mortgage, Student Loan) which companies should I avoid?
    * This presents the user a list of companies with the anomalous complaints that could indicate foul play.

## Installation

First, clone the repository locally:
```
$ git clone https://github.com/bayeshack16-superawesometeam/bayeshack16.git
```

Next, install fmr:
```
$ python setup.py install
```

Finally, enjoy!

### Software Dependencies
* Python version > 2.6
* [Pandas](http://pandas.pydata.org/ Pandas) (Python Data Analysis Library)

### Dataset Dependencies
* CFPB [Consumer Complaint Database](https://data.consumerfinance.gov/views/s6ew-h6mp/rows.csv) in CSV format
     * You can also manually select download options from the [main CFPB data page](http://www.consumerfinance.gov/data-research/consumer-complaints/#download-the-data)
* Census data by zipcode in CSV format
    1. Manually download the required datasets for the [datasources](zipcodes/datasources.py). These datasets and more are available from [American Fact Finder Download Center](http://factfinder.census.gov/faces/nav/jsf/pages/download_center.xhtml)
    2. Extract the csv data files into the [data](zipcodes/data) folder.
    3. Execute `$ python runner.py` to generate a single csv file with demographic information for each zipcode. (Example outputs are available already in the [output](zipcodes/output) directory

## Usage
###Examples:
To find mortgage companies potentially discriminating against clients:
```bash
$ fmr \
	--complaintsfile ./Consumer_Complaints.csv \
	--demographicsfile ./zipcodes/output/zz_all_us_race.csv \
	--racial \
	--badcompanies \
	--productline 'Mortgage' \
	--pretty
```
Sample output:
```
Racial Analysis:
[
    "Common Wealth Mortgage Services",
    "First American Mitigators, PLLC.",
    "Oceanside Mortgage Company",
    ...,
    "Old National Bank"
]
```
To find out what JPMorgan Chase & Co. financial product lines are suspicious:
```bash
$ fmr \
	--complaintsfile ./Consumer_Complaints.csv \
	--volume \
	--isbad \
	--company 'JPMorgan Chase & Co.' \
	--pretty
```
Sample output: ('true' means suspicious)
```
Volume Analysis:
{
    "Debt collection": true,
    "Prepaid card": false,
    "Mortgage": true,
    "Credit reporting": false,
    "Student loan": false,
    "Money transfers": false,
    "Bank account or service": true,
    "Credit card": true,
    "Payday loan": false,
    "Consumer Loan": true,
    "Other financial service": true
}
```
For all options:
```
$ fmr -h
```
The following values are valid inputs for the "--productline" flag
```
[
    'Student loan',
    'Credit reporting',
    'Credit card',
    'Debt collection',
    'Payday loan',
    'Consumer Loan',
    'Bank account or service',
    'Mortgage',
    'Money transfers',
    'Prepaid card',
    'Other financial service'
]
```
