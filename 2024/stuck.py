import printers
from rich import print, traceback
traceback.install()

PRINTER_TYPE = printers.REMOTE

with printers.get_printer(PRINTER_TYPE) as p:
    p.set(double_height=True, double_width=True, bold=True, underline=True, align="right")
    p.textln("HELP!! I'm stuck in a printer :(")
    p.set(align="left")
    for i in range(20):
        p.textln("Aaaaaaaaahhhhhhhh")
    p.cut()