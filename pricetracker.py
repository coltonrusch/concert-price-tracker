import requests
import json
import datetime
import csv
from secret import API_KEY


def update_csv(event_id):
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

    print("Updating '" + title + " " + str(event_id) + ".csv'...")

    with open(title + " " + str(event_id) + ".csv", mode='a+', newline='') as concert_file:
        concert_writer = csv.writer(concert_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        concert_writer.writerow(
            [current_time, announce_date, event_time, event_id, listing_count, lowest_price, median_price,
             average_price, highest_price, title])


def main():
    with open("user_input.txt", mode='r') as user_input:
        for line in enumerate(user_input):
            update_csv(int(line[1]))

    print("CSV(s) updated.")


if __name__ == "__main__":
    main()
