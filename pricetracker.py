import requests
import json
import datetime
import csv
import time

API_KEY = 'MTM2OTUwOTZ8MTU1OTE0NjkwMi4xMg'
event_id = 4924572

params = (
    ('client_id', API_KEY),
)

response = requests.get('https://api.seatgeek.com/2/events/' + str(event_id), params=params)
json_data = response.json()
with open('json_data.txt', 'w') as outfile:
    json.dump(json_data, outfile)

stats = json_data['stats']

title = json_data['title']
listing_count = stats['listing_count']
lowest_price = stats['lowest_price']
median_price = json_data['stats']['median_price']
average_price = stats['average_price']
highest_price = stats['highest_price']
announce_date = json_data['announce_date']
event_time = json_data['datetime_local']
current_time = datetime.datetime.utcnow().isoformat()[:-4]


def print_info():
    print("Event:")
    print(title)
    print("Listing count: ")
    print(listing_count)
    print("Lowest price: ")
    print(lowest_price)
    print("Median price: ")
    print(median_price)
    print("Average price: ")
    print(average_price)
    print("Highest price: ")
    print(highest_price)
    print("Announce date (UTC): ")
    print(announce_date)
    print("Event date/local time (UTC): ")
    print(event_time)
    print("Current date/time (UTC): ")
    print(current_time)


print_info()


with open(title + " " + str(event_id), mode='w') as concert_file:
    concert_writer = csv.writer(concert_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    concert_writer.writerow(['Access Date', 'Announce Date', 'Event Date', 'Event ID', 'Listing Count', 'Lowest Price', 'Median Price', 'Average Price', 'Highest Price', 'Title'])
    concert_writer.writerow([current_time, announce_date, event_time, event_id, listing_count, lowest_price, median_price, average_price, highest_price, title])


# def csv_update(writer):
#     with open(title + " " + str(event_id), mode='w'):
#         writer.writerow([current_time, announce_date, event_time, event_id, listing_count, lowest_price, median_price, average_price, highest_price, title])
#
# time.sleep(10)
# csv_update(concert_writer)
