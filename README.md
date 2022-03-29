# DataCite Bulk DOI Creator
Code Repository: https://github.com/gsu-library/datacite-bulk-doi-creator  
Author: Matt Brooks <mbrooks34@gsu.edu>  
Date Created: 2022-03-28  
License: [MIT](https://mit-license.org/)  
Forked From: https://github.com/UNLV-Libraries/metadata-workflows  
Version: 0.1.0  

## Description
A python script that creates DataCite DOIs from a provided CSV file. DOIs are created in the findable state.

## Usage
Rename the config.sample.py file to config.py and fill in your entire DOI prefix, username, and password. If wanting to test the script out with the test DataCite API replace the URL with the API test URL (https://api.test.datacite.org/dois).

## Attribution
The original code was created by Scotty Carlson and adapted by Kelsey George for UNLV Library.

## Dependencies
- [Python Requests](https://docs.python-requests.org/)
- [Python JSON](https://docs.python.org/3/library/json.html)
- [Python Chardet](https://chardet.github.io/)
- [Python pandas](https://pandas.pydata.org/)
