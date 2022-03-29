#!/usr/bin/env python

import requests
import json
import chardet
import pandas as pd
import config
# from pprint import pprint


'''Reads in the metadata from your export CSV and readies it for import.'''
def process_csv(file):
    input = pd.read_csv(file, encoding=config.encoding)
    processed_csv = []
    # TODO: determine if set or random prefix is used here.
    prefix = config.doiPrefix

    try:
        for row in input.itertuples():
            processed_csv.append({
                'id': row.context_key,
                'creators': [{
                    'name': row.creator,
                    'nameType': 'Personal',
                    'givenName': row.author1_fname,
                    'familyName': row.author1_lname
                }],
                'year': row.date,
                'uri': row.source,
                'title': row.title,
                'type': row.type,
                'descriptions': [{
                    'description': row.description,
                    'descriptionType': 'Abstract'
                }],
                'publisher': row.publisher,
                'doi': '{0}/{1}'.format(prefix, row.context_key)
            })
    except Exception as e:
        print(e)
        exit()

    return processed_csv


'''Process and submit DOIs to Datacite.'''
def submit_dois(dois):
    export = []

    for doi in dois:
        export_row = {}
        data = {
            'data': {
                'id': doi['doi'],
                'type': 'dois',
                'attributes': {
                    'event': 'publish',
                    'doi': doi['doi'],
                    'creators': doi['creators'],
                    'titles': [{
                        'title': doi['title']
                    }],
                    'publisher': doi['publisher'],
                    'publicationYear': doi['year'],
                    'descriptions': doi['descriptions'],
                    'types': {
                        'resourceTypeGeneral': 'Text',
                        'resourceType': doi['type']
                    },
                    'schemaVersion': 'http://datacite.org/schema/kernel-4',
                    'url': doi['uri']
                }
            }
        }

        json_data = json.dumps(data, ensure_ascii=False)
        response = requests.post(
            config.url,
            headers={'Content-Type': 'application/vnd.api+json'},
            data=json_data.encode('utf-8'),
            auth=(config.username, config.password)
        )
        print('{0} processed, response: {1}\n'.format(doi['doi'], response.status_code))
        export_row['id'] = doi['id']
        export_row['doi'] = 'https://doi.org/{0}'.format(doi['doi'])
        export_row['status'] = response.status_code
        export.append(export_row)

    return export


'''Saves a CSV file of the results.'''
def save_results(results):
    try:
        output = pd.DataFrame(results)
        output = output.set_index('id')
        output.to_csv('upload_report.csv')
    except:
        print('Error saving report CSV.')
        exit()



file_name = input('Please enter the name of your CSV file. (Make sure the filename has no spaces!)\n')

try:
    fp = open(file_name, 'rb').read()
    result = chardet.detect(fp)
    print('Suspected file encoding: {}'.format(result['encoding']))
except:
    print('Error reading file.')
    exit()

dois = process_csv(file_name)
results = submit_dois(dois)
save_results(results)
