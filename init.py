import requests
import json
import csv
from secret import API_KEY


def main():
    print("What is the numerical SeatGeek ID for the event you would like to track?")
    event_id = int(input())
    with open("user_input.txt", mode='w+') as user_input:
        user_input.write(str(event_id))

    params = (
        ('client_id', API_KEY),
    )

    response = requests.get('https://api.seatgeek.com/2/events/' + str(event_id), params=params)
    json_data = response.json()
    with open('json_data.txt', 'w', newline='') as outfile:
        json.dump(json_data, outfile)
    title = json_data['title']
    print("Initializing '" + title + " " + str(event_id) + ".csv'...")

    with open(title + " " + str(event_id) + ".csv", mode='a+', newline='') as concert_file:
        concert_writer = csv.writer(concert_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        concert_writer.writerow(
            ['Access Date', 'Announce Date', 'Event Date', 'Event ID', 'Listing Count', 'Lowest Price', 'Median Price',
             'Average Price', 'Highest Price', 'Title'])

    print("CSV initialized. To update this file with current ticket data, run 'pricetracker.py'.")


if __name__ == "__main__":
    main()
