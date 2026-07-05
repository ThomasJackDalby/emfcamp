import sys
import printers
import random

PRINTER_TYPE = printers.CONSOLE

class Item:
    def __init__(self, barcode, name):
        self.name = name
        self.barcode = barcode

ITEMS = [
    Item("74837465937","Bread"),
    Item("11773366448", "Egg"),
    Item("23523565435", "Bacon")
]

def print_menu():
    with printers.get_printer(PRINTER_TYPE) as p:
        p.set(double_height=True, double_width=True, bold=True, align="center")
        p.textln("BREAKFAST MENU")
        p.textln()
        for item in ITEMS:
            p.set(bold=True)
            p.textln(item.name)
            p.set(bold=False)
            p.barcode(item.barcode, "UPC-A")
            p.textln("-"*42)
        p.textln("Complete")
        p.barcode("00000000000", "UPC-A")
        p.cut()

def create_order():
    with printers.get_printer(PRINTER_TYPE) as p:
        order_id = random.randint(0, 100)
        order = {}
        while True:
            barcode = input("SCAN > ")[:-1]
            if int(barcode) == 0:
                p.set(double_height=True, double_width=True, bold=True, align="center", underline=True)
                p.textln(f"ORDER #{order_id}")
                p.textln()
                p.set(double_height=True, double_width=True, align="left")
                for item in order:
                    p.textln(f"{item.name} x {order[item]}")
                p.cut()
                p.set(double_height=True, double_width=True, bold=True, align="center", underline=True)
                p.textln(f"ORDER #{order_id}")
                p.textln()
                p.set(double_height=True, double_width=True, align="left")
                p.textln("Please retain for collection.")
                p.cut()
                return
            item = next((item for item in ITEMS if item.barcode == barcode), None)
            if item is not None:
                if not item in order:
                    order[item] = 0
                order[item] += 1
                print(f"Added 1 {item.name}")

if __name__ == "__main__":

    if len(sys.argv) < 2: raise Exception("No mode provided.")
    mode = sys.argv[1]

    if mode == "order": create_order()
    elif mode == "menu": print_menu()
    else: raise Exception(f"Unknown mode [{mode}] provided.")