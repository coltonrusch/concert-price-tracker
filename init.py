import json
import csv
import os
import requests
from secret import API_KEY      # string - SeatGeek API key is hidden
from secret import data_dir     # string - unique to the user, format: 'D:\\Users\\myName\\pricetracker\\data\\'


def currently_tracking():
    """
    iterates through the user-generated list of event IDs and prints their title and ID via get_event
    :return: n/a
    """
    print("Currently tracking the following events...")
    with open(data_dir + "user_input.txt", mode='r') as user_input:
        for line in enumerate(user_input):
            get_event(int(line[1]))


def get_event(event_id):
    """
    calls the SeatGeek API to retrieve the title for an event ID, then prints the formatted title and event ID
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

    # event title extracted from the json file and printed with the event ID
    title = json_data['title']
    print("          " + title + ", SeatGeek event ID: " + str(event_id))


def new_or_old(user_response):
    """
    helper function to determine if the user is generating a new or old event list and handle input errors
    :param user_response: string generated from user input (only '1' or '2' are valid inputs)
    :return: boolean to be fed into user_id_input
    """
    while True:
        if user_response == '1':
            return False
        if user_response == '2':
            return True
        print("Invalid response. Please type '1' for the former, and '2' for the latter.")
        break


def user_id_input(new):
    """
    takes user input of SeatGeek event ID(s) and either:
        (1) creates a new file to store the ID(s)
        (2) truncates an existing file to store the ID(s)
        (3) appends an existing file to store the ID(s)
    :param new: boolean representing if the user is generating a new event list or appending an existing event list
    :return: n/a
    """
    print("What is the numerical SeatGeek ID for the event(s) you would like to track? "
          "(type DONE when finished entering events)")

    # creates / truncates 'user_input.txt' and stores user inputted event ID(s)
    if new:
        with open(data_dir + "user_input.txt", mode='w') as user_input:
            user_input.write(input() + "\n")

        current_input = input()
        with open(data_dir + "user_input.txt", mode='a+') as user_input:
            while current_input != "DONE":
                user_input.write(current_input + "\n")
                current_input = input()
    # appends 'user_input.txt' and stores user inputted event ID(s)
    else:
        with open(data_dir + "user_input.txt", mode='a+') as user_input:
            user_input.write(input() + "\n")

        current_input = input()
        with open(data_dir + "user_input.txt", mode='a+') as user_input:
            while current_input != "DONE":
                user_input.write(current_input + "\n")
                current_input = input()


def create_data_dir():
    """
    creates a directory in the script's path to store data (CSVs, json, txt)
    :return: n/a
    """
    # create directory called 'data/' (handles FileExistsError if data directory already exists)
    try:
        os.mkdir('data/')
        print("Data will be stored in a folder named 'data'")
    except FileExistsError:
        print("Data will be stored in the existing folder named 'data'")


def csv_init(event_id):
    """
    initializes a CSV with a descriptive title and column headers, making use of a json request to the SeatGeek API
    :param event_id: SeatGeek ID for the given event
    :return: n/a
    """
    params = (
        ('client_id', API_KEY),
    )

    # SeatGeek API call to obtain and cache event's json data
    response = requests.get('https://api.seatgeek.com/2/events/' + str(event_id), params=params)
    json_data = response.json()
    with open(data_dir + 'json_data.json', 'w', newline='') as outfile:
        json.dump(json_data, outfile)

    # event title extracted from the json file
    title = json_data['title']

    # checks if the CSV already exists; if not, creates CSV and adds column headers
    if os.path.exists(data_dir + title + " " + str(event_id) + ".csv"):
        print("'" + title + " " + str(event_id) + ".csv' has already been initialized.")
    else:
        print("Initializing '" + title + " " + str(event_id) + ".csv'...")
        with open(data_dir + title + " " + str(event_id) + ".csv", mode='a+', newline='') as concert_file:
            concert_writer = csv.writer(concert_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            concert_writer.writerow(
                ['Access Date', 'Announce Date', 'Event Date', 'Event ID', 'Listing Count', 'Lowest Price',
                 'Median Price',
                 'Average Price', 'Highest Price', 'Title'])


def main():
    """
    initializes CSV(s) based on user input
    :return: n/a
    """

    # if 'user_input.txt' exists, display what events are already initialized and ready to update via pricetracker.py
    if os.path.exists(data_dir + "user_input.txt"):
        currently_tracking()

    print("Would you like to add another event to the list, or are you removing all events and starting fresh with a "
          "new set of events? (type '1' for the former, and '2' for the latter.)")

    # take user input for the above usage prompt
    answer = new_or_old(input())
    while answer is not True and answer is not False:
        answer = new_or_old(input())

    # generates a list of event IDs based on user input and stores it in a data directory
    user_id_input(answer)
    create_data_dir()

    # initializes each of the event IDs present on 'user_input.txt'
    with open(data_dir + "user_input.txt", mode='r') as user_input:
        for line in enumerate(user_input):
            csv_init(int(line[1]))

    print("CSV(s) initialized. To update with current ticket data, run 'pricetracker.py'.")


if __name__ == "__main__":
    main()
