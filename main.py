import boto3
import json
import csv

# Assuming that you have your AWS credentials set up in your environment.
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
# If not you can specify them directly in the client like
# boto3.client('dynamodb', region_name='us-west-2', aws_access_key_id="YOUR_ACCESS_KEY", aws_secret_access_key="YOUR_SECRET_KEY")

dynamodb = boto3.client('dynamodb', region_name='us-west-2')


def normalize_data_from_dynamo(table_name, file_name):
    # Get the table response
    response = dynamodb.scan(TableName=table_name)

    # Open a file for writing
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        

        # Write the headers to the file
        header = ["ip", "continent", "lat", "lon",
                  "city", "country", "region", "postal"]
        # writer.writerow(header)
        documents = []

        # Write the rest of the data
        for item in response['Items']:
            record = {}
            ip = item['ip']['S']
            location = item['location']['S']
            location = json.loads(location)
            continent = location['continent']['names']['en']
            lat = location['location']['latitude']
            lon = location['location']['longitude']
            city = location['city']['names']['en']
            country = location['country']['names']['en']
            region = None
            if 'subdivisions' in location and location['subdivisions'] is not None and len(location['subdivisions']) > 0:
                region = location['subdivisions'][0]['names']['en']
            postal = location['postal']['code']
            record['ip'] = ip
            record['continent'] = continent
            record['lat'] = lat
            record['lon'] = lon
            record['city'] = city
            record['country'] = country
            record['region'] = region
            record['postal'] = postal
            documents.append(record)
        
        #  write the documents array to a file
        with open(file_name, 'w', encoding="utf-8") as f:
          # Use json.dump to write the dictionary to the file
          json.dump(documents, f)

    print(f"Data downloaded and written to {file_name}")


# Call the function
normalize_data_from_dynamo('maxmind_cache', 'geoip.json')
