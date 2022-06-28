# DataCite Bulk DOI Creator
Code Repository: https://github.com/gsu-library/datacite-bulk-doi-creator  
Forked From: https://github.com/UNLV-Libraries/metadata-workflows  
Author: Matt Brooks <mbrooks34@gsu.edu>  
Date Created: 2022-03-28  
License: [MIT](https://mit-license.org/)  
Version: 0.2.0  

## Description
A python script that bulk creates DataCite DOIs from a provided CSV file. DOIs are created in the findable state.

For more information about DOIs please see DataCite's [support page](https://support.datacite.org/) and/or resources from their [homepage](https://doi.datacite.org/). Information on their [metadata schemas](https://schema.datacite.org/) is also available.

## Installation
1. [Install Python 3](https://www.python.org/about/gettingstarted/)
2. [Install Requests library](https://requests.readthedocs.io/en/latest/user/install/)
3. [Install json, datetime, and csv modules](https://docs.python.org/3/installing/index.html)

## Usage
Rename the config.sample.py file to config.py and fill in your DOI prefix, username, and password. If wanting to test the script out with the test DataCite API replace the URL with the API test URL (https://api.test.datacite.org/dois) and credentials.

The headers.csv file provides an example of all valid headers this script accepts (also see CSV Fields below). Only one set of creator fields are required per record.

Run the python script upload-csv.py. When starting, it will ask you to provide a file name to process. The file path will be relative to the folder the python script is run from (unless a leading slash is used). When finished an upload report will be generated.

### CSV Fields
**title** - title of publication  
**year** - publication year  
**type** - resource type  
**description** - abstract description  
**creator*{n}*** - full name (example, creator1, creator2, etc.)  
**creator*{n}*_type** - *Personal* or *Organizational*  
**creator*{n}*_given** - given name  
**creator*{n}*_family** - family name  
**publisher** - publisher  
**source** - URL reference to resource  
**context_key** - DOI suffix

### Error Codes
If an error occurs please see DataCite's [API error code page](https://support.datacite.org/docs/api-error-codes) for more information.

## Attribution
The original code was created by Scotty Carlson and adapted by Kelsey George for UNLV Library.

## Dependencies
- [Requests library](https://requests.readthedocs.io/)
- [json module](https://docs.python.org/3/library/json.html)
- [datetime module](https://docs.python.org/3/library/datetime.html)
- [csv module](https://docs.python.org/3/library/csv.html)
