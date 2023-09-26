#https://xerini.atlassian.net/jira/core/projects/VER/board

import requests
import json
import csv

api_label = 'xerini_reporter'
api_token = 'ATATT3xFfGF0LBjrA4_OoQEJ2JbIsM-5sqtZ3IVWC1cgSf4EkSaMWBrGSvwc6ZIwxxxkcpW5evxZ6obIsS7i1dAW5TtIAjcYxLeLnOtfID9Zo6PUsAr94oX5R78pJlrPLLpsuuBVJsk7ATdnf8Px_nD2IQRSzgYLfjYSk_JhEWkPDfwb3BLqJMw=C7D0EEC2'
USERNAME='jason.braid@xerini.co.uk'

project = 'VER'
status = 'In Progress'
csv_filename = f"{project}__{status}_issues.csv"

# Jira API URL and authentication credentials
JIRA_API_URL = 'https://xerini.atlassian.net/rest/api/2/'

# Label to search for
label_to_search = 'useability'

query_results = []

# Create a session with basic authentication
session = requests.Session()
session.auth = (USERNAME, api_token)

# Define JQL (Jira Query Language) to search for issues with a specific label
jql_query = f'status = "{status}" and project = "{project}"'

# Define the fields you want to retrieve (customize as needed)
fields = 'key,summary,issuetype,created,updated,assignee,description,status,comment'

# Build the Jira REST API request URL
url = f'{JIRA_API_URL}search'
params = {
    'jql': jql_query,
    'fields': fields,
}

try:
    # Send a GET request to Jira API
    response = session.get(url, params=params)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        data = response.json()
        issues = data.get('issues', [])

        # Print information about the issues
        for issue in issues:

            

            query_results.append(
                {"Key": issue["key"], 
                 "Summary": issue["fields"]["summary"], 
                 "Description": issue["fields"]["description"],
                 "Status": issue["fields"]["status"]["name"],
                 }
                 )
    else:
        print(f'Failed to retrieve data. Status code: {response.status_code}')
except requests.exceptions.RequestException as e:
    print(f'Error: {e}')

# Open the CSV file for writing
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Key", "Summary", "Description", "Status"])

    # Write the CSV header
    writer.writeheader()

    # Write the query results as rows
    for issue in query_results:
        writer.writerow(issue)

print(f'Data has been written to {csv_filename}.')

# Close the session
session.close()
