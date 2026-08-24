# TI-Nspire CX II Python game skeleton.
# Keep the first version intentionally simple while validating the toolchain.

from random import randint
from time import sleep
from ti_draw import *
from ti_system import get_key

SCREEN_W = 318
SCREEN_H = 212
START_CASH = 2000
START_DEBT = 5500
MAX_DAYS = 30

DRUGS = [
    ["Acid", 1000],
    ["Cocaine", 15000],
    ["Heroin", 8000],
    ["Weed", 400],
]

state = {
    "cash": START_CASH,
    "debt": START_DEBT,
    "day": 1,
    "location": "Bronx",
}


def draw_header():
    set_color(0, 0, 0)
    fill_rect(0, 0, SCREEN_W, 24)
    set_color(255, 255, 255)
    draw_text(8, 17, "DRUG WARS")


def draw_status():
    set_color(0, 0, 0)
    draw_text(10, 48, "Cash: $" + str(state["cash"]))
    draw_text(10, 68, "Debt: $" + str(state["debt"]))
    draw_text(10, 88, "Day: " + str(state["day"]) + "/" + str(MAX_DAYS))
    draw_text(10, 108, "Location: " + state["location"])


def draw_menu():
    draw_text(10, 140, "1 Buy / prices")
    draw_text(10, 160, "2 Travel / next day")
    draw_text(10, 180, "Esc Quit")


def draw_screen():
    clear()
    draw_header()
    draw_status()
    draw_menu()
    paint_buffer()


def random_price(base):
    # Simple +/- 30% variation for the starter build.
    pct = randint(70, 130)
    return (base * pct) // 100


def show_prices():
    clear()
    set_color(0, 0, 0)
    draw_text(8, 18, "MARKET")
    y = 45
    for item in DRUGS:
        name = item[0]
        base = item[1]
        draw_text(10, y, name + ": $" + str(random_price(base)))
        y += 25
    draw_text(10, 190, "Press any key")
    paint_buffer()

    while get_key() == "":
        sleep(0.05)


def next_day():
    if state["day"] < MAX_DAYS:
        state["day"] += 1


def main():
    draw_screen()

    while True:
        key = get_key()

        if key == "esc":
            break
        elif key == "1":
            show_prices()
            draw_screen()
        elif key == "2":
            next_day()
            draw_screen()

        sleep(0.05)


main()
