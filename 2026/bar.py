import printers
import argparse
import requests
import json
import re
from rich import print, traceback
traceback.install()

PROD_URL = "https://bar.emf.camp/api/on-tap.json"
DEV_URL = "https://emftill.assorted.org.uk/api/on-tap.json"

REGEX_CLEAN_HTML = re.compile('<.*?>') 

def clean_html(raw_html):
  return re.sub(REGEX_CLEAN_HTML, '', raw_html)

def main(printer_type: int, dev: bool):

    url = DEV_URL if dev else PROD_URL
    data = requests.get(url).json()
    with open("debug.json", "w") as file:
        json.dump(data, file, indent=4)

    with printers.get_printer(printer_type) as p:

        def print_heading(heading: str):
            p.set(align="center", bold=True, underline=True, double_height=True, double_width=True)
            p.textln(f"{heading.upper()}")
            p.set()
            p.textln("----------------")
            p.textln()

        def print_drink(drink):
            p.set(bold=True, underline=True)
            p.textln(f"{drink['stocktype']['fullname']} £{drink['stocktype']['price']}")
            if drink["description"] is not None: p.textln(drink["description"])
            if drink["stocktype"]["tasting_notes"] is not None: p.textln(clean_html(drink["stocktype"]["tasting_notes"]))
            p.set(align="center")
            p.textln(f"{drink['stocktype']['base_units_remaining']}/{drink['stocktype']['base_units_bought']} ({drink['remaining']}%) ")
            p.set(align="center")
            p.textln("--------")

        def print_section(key):
            print_heading(key)
            for drink in data[key]: print_drink(drink)

        print_section("ales")
        print_section("ciders")
        print_section("kegs")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--printer", type=int, default=printers.REMOTE)
    parser.add_argument("-d", "--dev", action="store_true")
    args = parser.parse_args()

    main(printer_type=args.printer, dev=args.dev)
