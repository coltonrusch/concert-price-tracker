import requests
import json
import datetime
import csv
import os
from secret import API_KEY
from secret import data_dir


def update_csv(event_id):
    """
    updates an already initialized CSV for a specific SeatGeek event with ticket pricing data
    :param event_id: SeatGeek ID for the given event
    :return: n/a
    """
    params = (
        ('client_id', API_KEY),
    )

    # SeatGeek API call to obtain and cache event's json data
    response = requests.get('https://api.seatgeek.com/2/events/' + str(event_id), params=params)
    json_data = response.json()
    with open(data_dir + 'json_data.json', 'w') as outfile:
        json.dump(json_data, outfile)

    # relevant data extracted from the json file
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

    # updates an event's CSV with the relevant data, given that the event's CSV has been initialized by init.py
    if os.path.exists(data_dir + title + " " + str(event_id) + ".csv"):
        print("Updating '" + title + " " + str(event_id) + ".csv'...")
        with open(data_dir + title + " " + str(event_id) + ".csv", mode='a+', newline='') as concert_file:
            concert_writer = csv.writer(concert_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            concert_writer.writerow(
                [current_time, announce_date, event_time, event_id, listing_count, lowest_price, median_price,
                 average_price, highest_price, title])
    else:
        print("File '" + title + " " + str(event_id) + ".csv' has not been initialized, and will not be updated.")


def main():
    """
    iterates through the user inputted event IDs generated by init.py and updates each of their CSV files
    :return: n/a
    """
    with open(data_dir + "user_input.txt", mode='r') as user_input:
        for line in enumerate(user_input):
            update_csv(int(line[1]))

    print("CSV(s) updated.")


if __name__ == "__main__":
    main()
