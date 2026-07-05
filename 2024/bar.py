import printers
import requests
from rich import print, traceback
traceback.install()

data = requests.get("https://bar.emf.camp/api/on-tap.json").json()

with printers.get_printer(printers.REMOTE) as p:

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
        p.textln(drink["stocktype"]["tasting_notes"])
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