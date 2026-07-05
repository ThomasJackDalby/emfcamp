import string
import random
import datetime
import json
import requests
import sys
import habville
import printers
from rich import print, traceback
traceback.install()

PRINTER_TYPE = printers.CONSOLE
USE_CACHED_DATA = False # either fetches from the API, or uses a locally stored .json file.
CACHED_SCHEDULE_FILE_PATH = ".cache/schedule.json"
URL = "https://www.emfcamp.org/schedule/2024.json"
DAYS = ["", "", "Thursday", "Friday", "Saturday", "Sunday"]

def get_data():
    if USE_CACHED_DATA:
        with open(CACHED_SCHEDULE_FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    else: 
        return requests.get(URL).json()

def get_day(date: datetime):
    return DAYS[int(date.split(" ")[0][-1])]

def parse_datetime(date: datetime):
    return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

def format_time(date: datetime):
    return datetime.datetime.strftime(date, "%H:%M")

def get_time(date):
    return date.split(" ")[1][:5]

def print_talk(p, talk, barcode=False, description=False):
    p.set(align="left", bold=True, underline=True, double_height=False, double_width=False)
    p.textln(talk["title"])
    p.set(bold=False, underline=False)

    start_date = parse_datetime(talk['start_date'])
    end_date = parse_datetime(talk['end_date'])
    day = start_date.strftime('%A')
    start = format_time(start_date)
    end = format_time(end_date)

    p.textln(f"{talk['speaker']}")
    p.textln(f"{day} | {start} - {end}")
    p.textln(f"{talk['venue']}")
    if description: p.textln(talk['description'])
    if barcode:
        barcode = "".join(random.choice(string.digits) for i in range(8)) + str(talk["id"]).zfill(3)
        p.barcode(barcode, "UPC-A")
    p.textln("-"*42)

def print_schedule(data, day):
    with printers.get_printer(PRINTER_TYPE) as p:
        data = list(filter(lambda talk: parse_datetime(talk['start_date']).day == day, data))
        p.set(double_height=True, double_width=True, bold=True, align="center")
        p.textln("EMF SCHEDULE")
        #p.textln(get_day(day))
        cut = 0
        for talk in sorted(data, key=lambda talk: parse_datetime(talk["start_date"])):
            print_talk(p, talk, True, False)
            cut += 1
            if cut >= 10:
                p.cut()
                cut = 0
        p.cut()

def print_custom(data, name):
    print("Please scan who you are?")
    if name is None:
        person = habville.scan_person()
        if person is None:
            print("Who even are you..?")
            return
        name = person.name

    p.set(double_height=True, double_width=True, bold=True, align="center")
    p.textln("EMF SCHEDULE")
    p.textln(name.upper())
    
    while True:
        barcode = input("SCAN > ")
        talk_id = int(barcode[-4:-1])
        print(barcode, talk_id)
        if talk_id == 0:
            p.cut()
            return
        talk = next((talk for talk in data if talk["id"] == talk_id), None)
        if talk is not None:
            print_talk(talk)

def print_cancel():
    with printers.get_printer(PRINTER_TYPE) as p:
        p.set(double_height=True, double_width=True, bold=True, align="center")
        p.textln("CANCEL CANCEL")
        p.barcode("00000000000", "UPC-A")
        p.textln("CANCEL CANCEL")
        p.cut()

def print_random_schedule(data):
    with printers.get_printer(PRINTER_TYPE) as p:
        p.set(double_height=True, double_width=True, bold=True, align="center")
        p.textln("EMF SCHEDULE")
        p.textln("RANDOM")

        for i in range(10):
            talk = random.choice(data)
            print_talk(p, talk)

if __name__ == "__main__":
    if len(sys.argv) == 1: raise Exception("Command needed")

    command = sys.argv[1]
    if command == "cancel": print_cancel()
    elif command == "schedule": print_schedule(get_data(), datetime.datetime.now().day)
    elif command == "random": print_random_schedule(get_data())
       
        # if len(sys.argv) == 1: print_custom(data, None)
    # else:
    #     name = sys.argv[1]
    #     print_custom(data, name)