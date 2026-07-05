import sys
import printers
from rich import traceback
traceback.install()

PRINTER_TYPE = printers.REMOTE

def print_message(message):
    with printers.get_printer(PRINTER_TYPE) as p:
        p.set(double_height=True, double_width=True, bold=True, underline=True, align="centre")
        p.textln("Incoming MESSAGE!!!!")
        p.set()
        p.textln("--------------------")
        p.textln(message)
        p.textln("--------------------")
        p.cut()

if __name__ == "__main__":
    if len(sys.argv) < 2: raise Exception("No message provided.")
    message = sys.argv[1]