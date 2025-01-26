# DataCite Bulk DOI Creator

Use in conjunction with the the [csv-merger-1](https://github.com/VIULibrary/csv-merger-1) and [csv-merger-2](https://github.com/VIULibrary/csv-merger-2) to map a dspace export .csv to a datacite import .csv, generate DOIs, and finally merge your DOIs in your dspace export/import .csv for importing into dspace


**[csv-merger-1](https://github.com/VIULibrary/csv-merger-) &rarr; DATACITE BULK DOI CREATOR &rarr; [csv-merger-csv-2](https://github.com/VIULibrary/csv-merger-2)**



## Description
A python script that bulk creates DataCite DOIs from a provided CSV file. DOIs are created in the findable state. If you are looking for the PHP version of this script see [DataCite Bulk DOI Creator WebApp](https://github.com/gsu-library/datacite-bulk-doi-creator-webapp).

For more information about DOIs please see DataCite's [support page](https://support.datacite.org/) and/or resources from their [homepage](https://doi.datacite.org/). Information on their [metadata schemas](https://schema.datacite.org/) is also available.

## Installation
1. [Install Python 3](https://www.python.org/about/gettingstarted/)
2. [Install Requests library](https://requests.readthedocs.io/en/latest/user/install/)
3. [Install json, datetime, and csv modules](https://docs.python.org/3/installing/index.html)

## Usage
Rename the config.sample.py file to config.py and fill in your DOI prefix, username (repository ID), and password. If wanting to test the script out with the test DataCite API replace the URL with the API test URL (https://api.test.datacite.org/dois) and credentials.

The headers.csv file provides an example of all valid headers this script accepts (also see CSV Fields below). Only one set of creator fields are required per record.

Run the python script upload-csv.py/auto-prefix.py When starting, it will ask you to provide a file name to process. The file path will be relative to the folder the python script is run from (unless a leading slash is used). When finished an upload report/.csv output will be generated.

## CSV Fields
**title** - title of publication  
**year** - publication year  
**type** - [Datacite resource type](https://support.datacite.org/docs/what-are-the-resource-types-for-datacite-dois)  
**description** - abstract description  
**creator{n}** - full name (header example: creator1, creator2, etc.)  
**creator{n}_type** - *Personal* or *Organizational* (If *Organizational*, set related creator fields blank) <br>
**creator{n}_given** - given name  
**creator{n}_family** - family name  
**publisher** - publisher  
**source** - URL reference to resource  
**context_key** - DOI suffix (remove from .csv and run 'auto-prefx.py to have Datacite autogenerate DOIs)


## UPDATES (VIU)
- use auto-prefix.py and a corresponding.csv (without a **context_key** header) to have Datacite generate DOI suffixes for you
- console gives a count of DOIs generated
- log output goes to named .csv with **title**, **source**, and **doi** headers/data
- Use this output file to merge the DOIs into your dspace metadata export/import file with [csv-merger](https://github.com/VIULibrary/csv-merger-1)


## Errors
If an error occurs a verbose message will be logged in the upload report/.csv. For more information on error codes please see DataCite's [API error code page](https://support.datacite.org/docs/api-error-codes).

If using auto-prefix.py, the error is written to the output.csv

## Attribution
The original code was created by Scotty Carlson and adapted by Kelsey George for UNLV Library.

## Dependencies
- [Requests library](https://requests.readthedocs.io/)
- [json module](https://docs.python.org/3/library/json.html)
- [datetime module](https://docs.python.org/3/library/datetime.html)
- [csv module](https://docs.python.org/3/library/csv.html)


## Attribution
Code Repository: https://github.com/gsu-library/datacite-bulk-doi-creator  
Forked From: https://github.com/UNLV-Libraries/metadata-workflows  
Author: Matt Brooks <mbrooks34@gsu.edu>  
Date Created: 2022-03-28  
License: [MIT](https://mit-license.org/)  
Version: 1.1.0