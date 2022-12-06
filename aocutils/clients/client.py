import requests
import datetime
import os
from bs4 import BeautifulSoup
from termcolor import colored
import json


def read_credentials():
    try:
        credentials = json.loads(open("user_info.json").read())
    except FileNotFoundError:
        print("Error: Specify your cookie & user agent in a file with name user_info.json")
        exit(0)

    return credentials

def get_current_day():
    dt = datetime.datetime.now(tz=datetime.timezone.utc)
    if 0 < dt.hour < 5:
        day = dt.day-1
    else:
        day = dt.day
    return dt.year, day

def fetch(year=None, day=None):
    if not year or not day:
        year, day = get_current_day()
    credentials = read_credentials()
    url = f'https://adventofcode.com/{year}/day/{day}/input'

    input_path = f"{os.getcwd()}/day{day}/input.txt"
    if os.path.exists(input_path):
        print(f"{input_path} exists. Exiting.")
        return

    resp = requests.get(url, **credentials)
    with open(input_path, 'w') as f:
        f.write(resp.text)


def find_main_info(text):
    try:
        soup = BeautifulSoup(text, 'html.parser')
        for data in (soup(['style', 'script'])):
            data.decompose()
        return soup.get_text()
    except Exception:
        print(colored("Could not parse answer. Go to www.adventofcode.com to check if you got it right.", "red"))
        print(text)
        return
    return soup.get_text()

def submit(answer, year=None, day=None, level=1):
    if not year or not day:
        year, day = get_current_day()
    credentials = read_credentials()
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    data = {'level': level, "answer": answer}
    resp = requests.post(url, data=data, **credentials)
    response = find_main_info(resp.text)
    if "That's the right answer" in response:
        message = colored(response, "green")
    else:
        message = colored(response, "red")
    print(message)
    return response
