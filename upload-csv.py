#!/usr/bin/env python

import requests
import json
from datetime import datetime
import csv
import config


'''Reads in the metadata from your export CSV and readies it for import.'''
def process_csv(file):
    header = [h.strip().lower() for h in file.readline().split(',')]
    reader = csv.DictReader(file, fieldnames=header)
    processed_csv = []
    prefix = config.doiPrefix

    try:
        for row in reader:
            i = 1
            creator = 'creator' + str(i)
            creators = []

            while creator in row:
               # Only append if there is data present.
               if row[creator]:
                  creators.append({
                     'name': row['creator' + str(i)],
                     'nameType': row['creator' + str(i) + '_type'],
                     'givenName': row['creator' + str(i) + '_given'],
                     'familyName': row['creator' + str(i) + '_family']
                  })
               else:
                  break

               i += 1
               creator = 'creator' + str(i)

            processed_csv.append({
                'id': row['context_key'],
                'creators': creators,
                'year': row['year'],
                'url': row['source'],
                'title': row['title'],
                'type': row['type'],
                'descriptions': [{
                    'description': row['description'],
                    'descriptionType': 'Abstract'
                }],
                'publisher': row['publisher'],
                'doi': '{0}/{1}'.format(prefix, row['context_key'])
            })
    except Exception as e:
        print(e)
        file.close()
        exit()

    return processed_csv


'''Process and submit DOIs to DataCite.'''


def submit_dois(dois):
    export = []

    for doi in dois:
        data = {
            'data': {
                'id': doi['doi'],
                'type': 'dois',
                'attributes': {
                    'event': 'publish',
                    'doi': doi['doi'],
                    'creators': doi['creators'] if doi['creators'] else [{'name': 'Anonymous'}],
                    'titles': [{'title': doi['title'].strip()}],
                    'publisher': doi['publisher'].strip(),
                    'publicationYear': doi['year'].strip(),
                    'descriptions': doi['descriptions'] if doi['descriptions'][0]['description'].strip() else [],
                    'types': {
                        'resourceTypeGeneral': 'Text',
                        'resourceType': doi['type'].strip()
                    },
                    'schemaVersion': 'http://datacite.org/schema/kernel-4',
                    'url': doi['url'].strip()
                }
            }
        }

        print("Submitting data to DataCite:")
        print(json.dumps(data, indent=4))

        json_data = json.dumps(data, ensure_ascii=False)
        response = requests.post(
            config.url,
            headers={'Content-Type': 'application/vnd.api+json'},
            data=json_data.encode('utf-8'),
            auth=(config.username, config.password)
        )

        response_text = json.loads(response.text)
        print(f"{doi['doi']} processed, response: {response.status_code}")
        print(response_text)  # Print full response for debugging

        export_row = {
            'id': doi['id'],
            'doi': f"https://doi.org/{doi['doi']}",
            'status': response.status_code,
            'error_message': response_text['errors'][0]['title'] if 'errors' in response_text else ''
        }
        export.append(export_row)

    return export



'''Saves a CSV file of the results.'''
def save_results(results):
    try:
        file = open('upload-report-{0}.csv'.format(datetime.now().strftime('%Y%m%d-%H%M%S')), 'w', newline='')
        fields = [
            'id',
            'doi',
            'status',
            'error_message'
        ]
        writer = csv.DictWriter(file, fieldnames=fields)

        writer.writeheader()
        writer.writerows(results)
    except:
        print('Error saving report CSV.')
        exit()
    finally:
        file.close()



file_name = input('Please enter the name of your CSV file.\n')
try:
    file = open(file_name, newline='', errors='ignore')
except:
    print('Error reading file.')
    exit()

dois = process_csv(file)
file.close()
results = submit_dois(dois)
save_results(results)