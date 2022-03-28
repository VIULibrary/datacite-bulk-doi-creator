#!/usr/bin/env python

import requests
import json
import random
import string
import chardet
import pandas as pd
import config


def pull_dois():
    '''Pulls first page of DOIs from Datacite API.'''
    response = requests.get(config.url)
    dois = json.loads(response.text)
    doi_data = dois['data']
    known_idents = []

    for doi in doi_data:
        ident = doi['id'].split('/')[1]
        known_idents.append(ident)

    return known_idents


def data_munger(file):
    '''Reads in the metadata from your export CSV and readies it for import.'''
    input_csv = pd.read_csv(file, encoding=config.encoding)
    data_package = []

    for row in input_csv.itertuples():
        data_package.append({'id': row.context_key, 'creators': [{'name': row.creator, 'nameType': 'Personal', 'givenName': row.author1_fname, 'familyName': row.author1_lname}],
                                 'year': row.date, 'uri': row.source, 'title': row.title, 'type': row.type, 'descriptions': [{'description': row.description, 'descriptionType': 'Abstract'}],
                                'publisher': row.publisher, 'doi': '10.{0}/{1}'.format(doiPrefix, row.context_key)})
        '''Be sure to enter your doi prefix above where it says 10.#####.'''

    return data_package



def doi_packager(y):
    '''Submits new DOI packages to Datacite. Be sure to add your credentials for DataCite production where it says USERNAME and PASSWORD.'''
    headers = {'Content-Type': 'application/vnd.api+json'}
    export_list = []

    for doi_data in y:
        export_dict = {}
        data_pack = {'data': {'id': doi_data['doi'], 'type': 'dois', 'attributes':
                         {'event': 'publish', 'doi': doi_data['doi'], 'creators': doi_data['creators'],
                          'titles': [{'title': doi_data['title']}], 'publisher': doi_data['publisher'],
                          'publicationYear': doi_data['year'], 'descriptions': doi_data['descriptions'],
                          'types': {'resourceTypeGeneral': 'Text', 'resourceType': doi_data['type']},
                          'url': doi_data['uri'], 'schemaVersion': 'http://datacite.org/schema/kernel-4'}}}
        jsonized = json.dumps(data_pack, ensure_ascii=False)
        response = requests.post('https://api.datacite.org/dois',
                                 headers=headers, data=jsonized.encode('utf-8'),
                                 auth=(username, password))
        print('{0} processed, response: {1}'.format(doi_data['doi'], response.status_code))
        export_dict['id'] = doi_data['id']
        export_dict['doi'] = 'https://doi.org/{0}'.format(doi_data['doi'])
        export_dict['status'] = response.status_code
        export_list.append(export_dict)

    return export_list


def csv_machine(z):
    '''Barfs out a CSV file of your results'''
    output = pd.DataFrame(z)
    output = output.set_index('id')
    output.to_csv('metadata_update.csv')


file_name = input('Please enter the name of your CSV file. (Make sure the filename has no spaces!)\n')

try:
    fp = open(file_name, 'rb').read()
    result = chardet.detect(fp)
    print(result['encoding'])
    # fp.close()
except:
    print('Error reading file')
    exit()

# new_dois = data_munger(file_name)
# results = doi_packager(new_dois)
# csv_machine(results)
