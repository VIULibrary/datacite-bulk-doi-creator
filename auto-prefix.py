#!/usr/bin/env python

import requests
import json
from datetime import datetime
import csv
import config




#'''Auto-generate a suffix'''
#def generate_suffix():
#    return str(uuid.uuid4())



'''Reads in the metadata from your export CSV and readies it for import.'''
def process_csv(file):
    header = [h.strip().lower() for h in file.readline().split(',')]
    reader = csv.DictReader(file, fieldnames=header)
    processed_csv = []

    try:
        for row in reader:
            i = 1
            creator = f'creator{i}'
            creators = []

            while creator in row:
                # Ensure the creator has at least a name
                if row[creator]:
                    name_type = row.get(f'{creator}_type', '').strip()
                    if name_type not in {'Organizational', 'Personal'}:
                        # Default to 'Personal' if nameType is invalid or missing
                        name_type = 'Personal'

                    creators.append({
                        'name': row[creator].strip(),
                        'nameType': name_type,
                        'givenName': row.get(f'{creator}_given', '').strip(),
                        'familyName': row.get(f'{creator}_family', '').strip()
                    })
                else:
                    break

                i += 1
                creator = f'creator{i}'

            # Let DataCite handle the DOI suffix auto-generation
            processed_csv.append({
                'creators': creators,
                'year': row['year'].strip(),
                'url': row['source'].strip(),
                'title': row['title'].strip(),
                'type': row['type'].strip(),
                'descriptions': [{
                    'description': row['description'].strip(),
                    'descriptionType': 'Abstract'
                }],
                'publisher': row['publisher'].strip(),
                'doi': ''  # Leave DOI blank to enable auto-generation
            })
    except Exception as e:
        print(e)
        file.close()
        exit()

    return processed_csv




'''Process and submit DOIs to DataCite.'''

def submit_dois(dois):
    export = []
    success_count = 0  # Counter for successful DOI generations

    for doi in dois:
        data = {
            'data': {
                'type': 'dois',
                'attributes': {
                    'event': 'publish',  # Create a Findable DOI
                    'prefix': config.doiPrefix,  # Include the DOI prefix to trigger auto-generation
                    'creators': doi['creators'],
                    'titles': [{'title': doi['title'].strip()}],
                    'publisher': doi['publisher'].strip(),
                    'publicationYear': doi['year'].strip(),
                    'descriptions': doi['descriptions'],
                    'types': {
                        'resourceTypeGeneral': 'Text',
                        'resourceType': doi['type'].strip()
                    },
                    'schemaVersion': 'http://datacite.org/schema/kernel-4',
                    'url': doi['url'].strip()
                }
            }
        }

        # Debugging: Print the JSON payload being sent
        print("Submitting data to DataCite:")
        print(json.dumps(data, indent=4))

        # Make the POST request to the DataCite API
        json_data = json.dumps(data, ensure_ascii=False)
        response = requests.post(
            config.url,
            headers={'Content-Type': 'application/vnd.api+json'},
            data=json_data.encode('utf-8'),
            auth=(config.username, config.password)
        )

        # Parse and log the response
        response_text = json.loads(response.text)
        print(f"Response for DOI generation: {response.status_code}")
        print(response_text)

        if response.status_code == 201:  # DOI successfully created
            success_count += 1  # Increment the success counter
            export_row = {
                'doi': f"https://doi.org/{response_text['data']['id']}",
                'status': response.status_code,
                'error_message': ''
            }
        else:
            export_row = {
                'doi': None,
                'status': response.status_code,
                'error_message': response_text['errors'][0]['title'] if 'errors' in response_text else 'Unknown error'
            }

        export.append(export_row)

    # Log the total count of successful DOIs generated
    print(f"\nTotal DOIs successfully generated: {success_count}/{len(dois)}")

    return export






'''Saves a CSV file of the results.'''
def save_results(results):
    try:
        # Open the report CSV file for writing
        file = open(f'upload-report-{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv', 'w', newline='')
        fields = ['doi', 'status', 'error_message']  # Define CSV headers
        writer = csv.DictWriter(file, fieldnames=fields)

        writer.writeheader()  # Write headers
        writer.writerows(results)  # Write all result rows

        # Count the successful entries (status code 201)
        success_count = sum(1 for result in results if result['status'] == 201)

        # Append the summary row
        file.write(f"\nTotal DOIs successfully generated: {success_count}/{len(results)}\n")
        print(f"Results saved. Total DOIs successfully generated: {success_count}/{len(results)}")
    except Exception as e:
        print('Error saving report CSV:', e)
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