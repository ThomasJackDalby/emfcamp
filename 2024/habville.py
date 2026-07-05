import os
import random
import json
import logging
from printers import Printer

logger = logging.getLogger(__name__)

FILE_PATH = ".cache/people.json"
if not os.path.exists(FILE_PATH):
    DATA = {}
else:
    with open(FILE_PATH, "r") as file:
        DATA = json.load(file)

class Person:
    def __init__(self, name, code) -> None:
        self.name = name
        self.code = code

def scan_person():
    while True:
        barcode = input("SCAN > ")
        person = get_person(barcode)
        if person is not None:
            return person

def get_person(barcode: str):
    barcode = barcode[:11] if len(barcode) > 11 else barcode
    person = next((person for person in DATA if person["barcode"] == barcode), None)

    if person is not None: 
        return Person(person["name"], person["barcode"])
    
    logger.warn(f"No person found with barcode {barcode}")
    return None

def register(name: str):
    barcode = _get_random_barcode()
    DATA.append({
        "barcode" : barcode,
        "name" : name
    })
    with open(FILE_PATH, "w") as file:
        json.dump(DATA, file, indent=4)

def print_people(p: Printer):
    p.set(double_height=True, double_width=True, bold=True, align="center")
    p.textln()
    for person in DATA:
        p.set(double_height=True, double_width=True, bold=True, align="center")
        p.textln(person["name"])
        p.barcode(person["barcode"], "UPC-A")
        p.set()
        p.textln("-"*42)
    p.cut()

def _get_random_barcode():
    return "".join(str(random.randint(0, 9)) for i in range(11))

if __name__ == "__main__":
    print_people()
    exit()
 
    import sys
    name = sys.argv[1]
    register(name)