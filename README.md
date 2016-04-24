# PROJECT NAME

## Context

The Consumer Financial Protection Bureau (CFPB) publishes a public [consumer complaint database](http://www.consumerfinance.gov/data-research/consumer-complaints/ CFPB Consumer Complaint Database) consisting of complaints relating to financial services products and companies. Unscrupulous companies sometimes take advantage of consumers through predatory or discriminatory product offerings and targeting, leading to the consumers lodging complaints against these products and companies to the CFPB. <p>

By enriching the consumer complaint dataset with population demographic statistics sourced from the [American Community Survey](https://www.census.gov/programs-surveys/acs/ American Community Survey), our research shows that there exist notable relationships between companies that have received complaints from those geographical regions with the largest minority populations (on the 5-digit ZIP code granulatity) and the companies that are eventually charged with discriminatory product offerings. <p>

Most notably, we show that our analysis can help identify companies that possibly offer predatorial, fraudulent, and racially discriminatory financial products. This can help influence policy and investigation decisions by financial regulatory bodies, and help consumers get better access to data about the suspiciousness of a financial vendor.<p>

## Description=

## Installation

### Software Dependencies
* Python version >2.7
* [Pandas](http://pandas.pydata.org/ Pandas) (Python Data Analysis Library)

### Dataset Dependencies
* CFPB [Consumer Complaint Database](https://data.consumerfinance.gov/views/s6ew-h6mp/rows.csv) in CSV format
     * You can also manually select download options from the [main CFPB data page](http://www.consumerfinance.gov/data-research/consumer-complaints/#download-the-data)
* Census data by zipcode in CSV format
    1. Manually download the required datasets for the [datasources](zipcodes/datasources.py). These datasets and more are available from [American Fact Finder Download Center](http://factfinder.census.gov/faces/nav/jsf/pages/download_center.xhtml)
    2. Extract the csv data files into the [data](zipcodes/data) folder.
    3. Execute `$ python runner.py` to generate a single csv file with demographic information for each zipcode. (Example outputs are available already in the [output](zipcodes/output) directory

## Usage

