import json
import random


geoip = []

with open('geoip.json', 'r') as f:
    geoip = json.load(f)


final_data = []


def add_location(records):
    #  rad from eth json array file
    with open('logs.json', 'r') as f:
        records = json.load(f)
        # read each records and print
        for record in records:
            del record['_id']
            del record['_timestamp']
            del record['ip']
            del record['date']
            del record['newfeild']
            # print(record)

            # get a  random record from geoip
            random_record = random.choice(geoip)
            # add the random record to the record
            record['continent'] = random_record['continent']
            record['lat'] = random_record['lat']
            record['lon'] = random_record['lon']
            record['city'] = random_record['city']
            record['country'] = random_record['country']
            record['region'] = random_record['region']
            record['postal'] = random_record['postal']

            # print(record)

            # add the record to the final data
            final_data.append(record)


#  write main function
if __name__ == "__main__":
    for i in range(25):
        add_location(final_data)
    #  write the final data to a file
    with open('logs_with_geoip.json', 'w', encoding="utf-8") as f:
        # Use json.dump to write the dictionary to the file
        json.dump(final_data, f)
