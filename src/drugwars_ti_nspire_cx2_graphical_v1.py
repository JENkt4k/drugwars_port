# Drug Wars - TI-Nspire CX II Graphical Edition
# ------------------------------------------------------------
# Full-screen ti_draw UI: no Python Shell scrolling.
#
# Controls:
#   Up/Down      move through menus
#   Left/Right   adjust numeric values by 1
#   0-9          type numeric values
#   Enter        select / confirm
#   Esc          back / cancel
#
# TI-Nspire CX II modules used:
#   ti_draw      full-screen graphics
#   ti_system    get_key()
#   random       game randomness
#
# Create a new Python program on the handheld and paste this file.
# The program uses the default 318x212 graphics coordinate system,
# where (0,0) is the upper-left corner.

from ti_draw import *
from ti_system import *
from random import randint

# ----------------------------
# Screen / palette
# ----------------------------

W = 318
H = 212

BLACK = (0, 0, 0)
WHITE = (235, 235, 235)
GRAY = (150, 150, 150)
DARK = (25, 25, 25)
CYAN = (0, 220, 235)
GREEN = (80, 255, 90)
YELLOW = (255, 230, 40)
RED = (255, 75, 50)
ORANGE = (255, 145, 40)
BLUE = (70, 140, 255)

# ----------------------------
# Game constants
# ----------------------------

DRUGS = ["Cocaine", "Heroin", "Acid", "Weed", "Speed", "Ludes"]
COKE, HEROIN, ACID, WEED, SPEED, LUDES = range(6)

LOCATIONS = [
    "Bronx",
    "Ghetto",
    "Central Park",
    "Manhattan",
    "Coney Island",
    "Brooklyn"
]

# ----------------------------
# Graphics helpers
# ----------------------------

def color(c):
    set_color(c[0], c[1], c[2])

def rect(x, y, w, h, c):
    color(c)
    fill_rect(x, y, w, h)

def line(x1, y1, x2, y2, c=GRAY):
    color(c)
    draw_line(x1, y1, x2, y2)

def text(x, y, s, c=WHITE):
    color(c)
    draw_text(x, y, str(s))

def begin_screen():
    # Draw entirely into the off-screen buffer.
    rect(0, 0, W, H, BLACK)

def end_screen():
    paint_buffer()

def header(title, right=""):
    rect(0, 0, W, 23, DARK)
    text(6, 17, title, CYAN)
    if right:
        # simple right-ish placement; titles are short
        x = W - 7 - len(str(right)) * 8
        if x < 170:
            x = 170
        text(x, 17, right, CYAN)
    line(0, 24, W, 24, GRAY)

def footer(left="", right=""):
    line(0, 190, W, 190, GRAY)
    if left:
        text(5, 207, left, YELLOW)
    if right:
        x = W - 5 - len(str(right)) * 8
        if x < 155:
            x = 155
        text(x, 207, right, WHITE)

def wait_key():
    return get_key(1)

def wait_enter_or_esc():
    while True:
        k = wait_key()
        if k == "enter":
            return True
        if k == "esc":
            return False

def message(title_text, lines, accent=YELLOW, footer_text="ENTER: Continue"):
    begin_screen()
    header(title_text)
    y = 48
    for i, s in enumerate(lines):
        c = accent if i == 0 else WHITE
        text(12, y, s, c)
        y += 22
    footer(footer_text)
    end_screen()
    return wait_enter_or_esc()

def confirm(title_text, question):
    selected = 0
    while True:
        begin_screen()
        header(title_text)
        text(16, 62, question, WHITE)

        opts = ["YES", "NO"]
        for i in range(2):
            y = 105 + i * 32
            if i == selected:
                rect(25, y - 18, 110, 25, DARK)
                text(32, y, "> " + opts[i], YELLOW)
            else:
                text(32, y, "  " + opts[i], WHITE)

        footer("UP/DOWN: Move", "ENTER: Select")
        end_screen()

        k = wait_key()
        if k == "up" or k == "down":
            selected = 1 - selected
        elif k == "enter":
            return selected == 0
        elif k == "esc":
            return False

def menu_screen(title_text, subtitle, items, selected, status1="", status2=""):
    begin_screen()
    header(title_text, subtitle)

    if status1:
        text(7, 42, status1, GREEN)
    if status2:
        text(167, 42, status2, RED)

    y0 = 67
    row_h = 24
    for i, item in enumerate(items):
        y = y0 + i * row_h
        if i == selected:
            rect(7, y - 17, 304, 22, DARK)
            text(13, y, "> " + item, YELLOW)
        else:
            text(13, y, "  " + item, WHITE)

    footer("UP/DOWN: Move", "ENTER: Select")
    end_screen()

def choose_menu(title_text, subtitle, items, status1="", status2="", allow_esc=True):
    sel = 0
    while True:
        menu_screen(title_text, subtitle, items, sel, status1, status2)
        k = wait_key()

        if k == "up":
            sel = (sel - 1) % len(items)
        elif k == "down":
            sel = (sel + 1) % len(items)
        elif k == "enter":
            return sel
        elif k == "esc" and allow_esc:
            return -1

def number_entry(title_text, prompt, value=0, min_value=0, max_value=999999):
    # Fully graphical numeric input; never falls back to input().
    # Digits replace an initial zero, then append.
    typed = str(value)
    if typed == "":
        typed = "0"

    while True:
        try:
            n = int(typed)
        except:
            n = 0

        if n < min_value:
            n = min_value
        if n > max_value:
            n = max_value

        begin_screen()
        header(title_text)
        text(14, 60, prompt, WHITE)
        text(14, 93, "Min: " + str(min_value), GRAY)
        text(160, 93, "Max: " + str(max_value), GRAY)

        rect(55, 118, 205, 38, DARK)
        text(70, 146, str(n), CYAN)

        footer("DIGITS/LEFT/RIGHT", "ENTER: OK  ESC: Back")
        end_screen()

        k = wait_key()

        if k in ("0","1","2","3","4","5","6","7","8","9"):
            if typed == "0":
                typed = k
            else:
                candidate = typed + k
                try:
                    cv = int(candidate)
                except:
                    cv = n
                if cv <= max_value:
                    typed = candidate

        elif k == "left":
            n -= 1
            if n < min_value:
                n = min_value
            typed = str(n)

        elif k == "right":
            n += 1
            if n > max_value:
                n = max_value
            typed = str(n)

        elif k == "del" or k == "backspace":
            if len(typed) > 1:
                typed = typed[:-1]
            else:
                typed = "0"

        elif k == "enter":
            if n < min_value:
                n = min_value
            if n > max_value:
                n = max_value
            return n

        elif k == "esc":
            return None

def drug_table(title_text, game, mode="prices", selected=-1):
    begin_screen()
    header(title_text, game.location_name() + " D" + str(game.day))

    y = 48
    for i in range(6):
        if i == selected:
            rect(4, y - 15, 309, 20, DARK)

        num = str(i + 1) + "."
        name = DRUGS[i]
        price = "$" + str(game.prices[i])

        if selected == i:
            c = YELLOW
        else:
            c = WHITE

        text(8, y, num, c)
        text(33, y, name, c)
        text(169, y, price, GREEN)

        if mode == "sell" or mode == "coat":
            text(268, y, "x" + str(game.inv[i]), CYAN)

        y += 21

    line(0, 176, W, 176, GRAY)
    text(7, 188, "Cash $" + str(game.cash), GREEN)
    text(119, 188, "Debt $" + str(game.debt), RED)
    text(235, 188, "Free " + str(game.free_space()), WHITE)

    end_screen()

def choose_drug_graphical(title_text, game, mode):
    sel = 0
    while True:
        drug_table(title_text, game, mode, sel)
        # Overlay footer-like hints inside last pixels if possible.
        k = wait_key()

        if k == "up":
            sel = (sel - 1) % 6
        elif k == "down":
            sel = (sel + 1) % 6
        elif k in ("1","2","3","4","5","6"):
            return int(k) - 1
        elif k == "enter":
            return sel
        elif k == "esc" or k == "0":
            return -1

# ----------------------------
# Game
# ----------------------------

class Game:
    def __init__(self):
        self.cash = 2000
        self.debt = 5000
        self.bank = 0

        self.day = 1
        self.location = 0

        self.guns = 0
        self.damage = 0

        self.capacity = 100
        self.inv = [0, 0, 0, 0, 0, 0]
        self.prices = [0, 0, 0, 0, 0, 0]

        self.dead = False
        self.finished = False
        self.quit_early = False

    def location_name(self):
        return LOCATIONS[self.location]

    def used_space(self):
        return sum(self.inv) + self.guns * 5

    def free_space(self):
        return self.capacity - self.used_space()

    # ------------------------
    # Title / instructions
    # ------------------------

    def title_screen(self):
        while True:
            begin_screen()

            # skyline-ish decoration
            rect(0, 0, W, H, BLACK)
            rect(0, 145, W, 45, (7, 18, 35))
            for x, h in [(10,24),(32,39),(58,29),(83,47),(112,32),
                         (139,55),(171,35),(196,49),(224,28),(252,42),(281,33)]:
                rect(x, 145-h, 19, h, (8, 28, 55))

            text(42, 48, "DRUG WARS", WHITE)
            text(234, 67, "2.00", WHITE)
            text(34, 105, "TI-Nspire CX II Edition", CYAN)
            text(33, 128, "Based on J.M. TI version", CYAN)

            text(66, 180, "ENTER: START", YELLOW)
            text(190, 180, "ESC: QUIT", GRAY)
            end_screen()

            k = wait_key()
            if k == "enter":
                return True
            if k == "esc":
                return False

    def instructions(self):
        pages = [
            [
                "Buy low and sell high.",
                "Start cash: $2000",
                "Start debt: $5000",
                "You have 30 days.",
                "Pay off the debt and",
                "make as much as possible."
            ],
            [
                "NORMAL PRICE RANGES",
                "Cocaine  $16000-$28000",
                "Heroin    $5000-$12000",
                "Acid      $1000-$4400",
                "Weed        $330-$750",
                "Speed        $70-$220",
                "Ludes         $10-$50"
            ],
            [
                "Coat holds 100 units.",
                "Guns use 5 spaces.",
                "Police may chase you",
                "when carrying a lot.",
                "Debt grows 10% / trip.",
                "Bank grows 6% / trip."
            ]
        ]

        p = 0
        while True:
            begin_screen()
            header("HOW TO PLAY", str(p + 1) + "/3")
            y = 49
            for i, s in enumerate(pages[p]):
                c = CYAN if (p == 1 and i == 0) else WHITE
                text(14, y, s, c)
                y += 22
            footer("LEFT/RIGHT: Page", "ENTER: Game")
            end_screen()

            k = wait_key()
            if k == "left":
                p = (p - 1) % 3
            elif k == "right":
                p = (p + 1) % 3
            elif k == "enter":
                if p < 2:
                    p += 1
                else:
                    return
            elif k == "esc":
                return

    # ------------------------
    # Economy
    # ------------------------

    def roll_prices(self):
        self.prices[COKE]   = randint(16000, 28000)
        self.prices[HEROIN] = randint(5000, 12000)
        self.prices[ACID]   = randint(10, 44) * 100
        self.prices[WEED]   = randint(33, 75) * 10
        self.prices[SPEED]  = randint(7, 22) * 10
        self.prices[LUDES]  = randint(1, 5) * 10

        event = randint(0, 20)
        self.random_event(event)

    def buy(self):
        while True:
            d = choose_drug_graphical("BUY", self, "buy")
            if d < 0:
                return

            price = self.prices[d]
            max_cash = self.cash // price
            max_qty = min(max_cash, self.free_space())

            if max_qty <= 0:
                message("CAN'T BUY",
                        ["Not enough cash or", "no free coat space."],
                        RED)
                continue

            qty = number_entry(
                "BUY " + DRUGS[d].upper(),
                "$" + str(price) + " each. How many?",
                0, 0, max_qty
            )

            if qty is None:
                continue

            self.inv[d] += qty
            self.cash -= qty * price
            return

    def sell(self):
        while True:
            d = choose_drug_graphical("SELL", self, "sell")
            if d < 0:
                return

            if self.inv[d] <= 0:
                message("CAN'T SELL",
                        ["You don't have any", DRUGS[d] + "."],
                        RED)
                continue

            qty = number_entry(
                "SELL " + DRUGS[d].upper(),
                "$" + str(self.prices[d]) + " each. How many?",
                0, 0, self.inv[d]
            )

            if qty is None:
                continue

            self.inv[d] -= qty
            self.cash += qty * self.prices[d]
            return

    def prices_screen(self):
        drug_table("PRICES", self, "prices", -1)
        wait_enter_or_esc()

    def coat_screen(self):
        begin_screen()
        header("TRENCHCOAT", self.location_name())

        y = 47
        for i in range(6):
            text(9, y, DRUGS[i], WHITE)
            text(190, y, str(self.inv[i]), CYAN)
            y += 20

        line(0, 169, W, 169, GRAY)
        text(8, 184, "Used " + str(self.used_space()) + "/" + str(self.capacity), WHITE)
        text(142, 184, "Free " + str(self.free_space()), GREEN)
        text(230, 184, "Guns " + str(self.guns), YELLOW)

        footer("ESC/ENTER: Back")
        end_screen()
        wait_enter_or_esc()

    # ------------------------
    # Bank / debt
    # ------------------------

    def bank_menu(self):
        if self.location != 0:
            message("BANK",
                    ["The bank is in", "the Bronx."],
                    ORANGE)
            return

        while True:
            items = ["View account", "Deposit", "Withdraw", "Back"]
            c = choose_menu(
                "BANK", "BRONX", items,
                "Cash $" + str(self.cash),
                "Bank $" + str(self.bank)
            )

            if c == -1 or c == 3:
                return

            if c == 0:
                message("BANK ACCOUNT",
                        ["Balance: $" + str(self.bank),
                         "Interest: 6% per trip."],
                        GREEN)

            elif c == 1:
                amt = number_entry("BANK - DEPOSIT",
                                   "Deposit how much?",
                                   0, 0, self.cash)
                if amt is not None:
                    self.cash -= amt
                    self.bank += amt

            elif c == 2:
                amt = number_entry("BANK - WITHDRAW",
                                   "Withdraw how much?",
                                   0, 0, self.bank)
                if amt is not None:
                    self.bank -= amt
                    self.cash += amt

    def loan_menu(self):
        if self.location != 0:
            message("LOAN SHARK",
                    ["The loan shark is in", "the Bronx."],
                    ORANGE)
            return

        while True:
            items = ["Repay debt", "Borrow more", "Back"]
            c = choose_menu(
                "LOAN SHARK", "BRONX", items,
                "Cash $" + str(self.cash),
                "Debt $" + str(self.debt)
            )

            if c == -1 or c == 2:
                return

            if c == 0:
                max_pay = min(self.cash, self.debt)
                amt = number_entry("REPAY DEBT",
                                   "Repay how much?",
                                   0, 0, max_pay)
                if amt is not None:
                    self.cash -= amt
                    self.debt -= amt

            elif c == 1:
                amt = number_entry("BORROW",
                                   "Borrow how much?",
                                   0, 0, 5000)
                if amt is not None:
                    self.cash += amt
                    self.debt += amt

    # ------------------------
    # Travel
    # ------------------------

    def travel(self):
        while True:
            sel = 0
            while True:
                begin_screen()
                header("TRAVEL", "Day " + str(self.day))

                y = 46
                for i, loc in enumerate(LOCATIONS):
                    if i == sel:
                        rect(6, y - 15, 306, 20, DARK)
                        text(12, y, "> " + loc, YELLOW)
                    else:
                        text(12, y, "  " + loc, WHITE)

                    if i == self.location:
                        text(232, y, "(HERE)", CYAN)

                    y += 23

                footer("UP/DOWN: Move", "ENTER: Travel ESC:Back")
                end_screen()

                k = wait_key()
                if k == "up":
                    sel = (sel - 1) % len(LOCATIONS)
                elif k == "down":
                    sel = (sel + 1) % len(LOCATIONS)
                elif k == "enter":
                    break
                elif k == "esc":
                    return False

            if sel == self.location:
                message("TRAVEL",
                        ["You're already in", self.location_name() + "."],
                        ORANGE)
                continue

            self.location = sel
            self.day += 1

            # Original mechanics:
            self.debt = int(self.debt * 1.10)
            self.bank = int(self.bank * 1.06)

            if self.day >= 31:
                self.finished = True
                return True

            # Simple subway transition.
            begin_screen()
            header("SUBWAY")
            text(72, 93, "Traveling to", WHITE)
            text(81, 125, self.location_name(), CYAN)
            footer("ENTER: Arrive")
            end_screen()
            wait_enter_or_esc()

            self.roll_prices()
            return True

    # ------------------------
    # Random events
    # ------------------------

    def random_event(self, event):
        if self.finished:
            return

        if event == 1:
            self.prices[LUDES] = 2
            message("MARKET EVENT",
                    ["CHEAP LUDES!", "Rival dealers flooded", "the market."],
                    YELLOW)

        elif event == 2:
            self.prices[WEED] = 122
            message("MARKET EVENT",
                    ["WEED PRICES CRASH!", "The market bottomed out."],
                    YELLOW)

        elif event == 3:
            self.prices[HEROIN] = randint(850, 2000)
            message("MARKET EVENT",
                    ["CHEAP HEROIN!", "Police are unloading", "last week's seizure."],
                    YELLOW)

        elif event == 4 or event == 5:
            self.prices[HEROIN] = randint(18000, 43000)
            message("MARKET EVENT",
                    ["HEROIN SHORTAGE!", "Addicts are paying", "outrageous prices."],
                    ORANGE)

        elif event == 6 or event == 7:
            self.prices[COKE] = randint(80000, 140000)
            message("MARKET EVENT",
                    ["BIG COKE BUST!", "Prices are outrageous."],
                    ORANGE)

        elif event == 8:
            lost_before = self.cash
            self.cash = (self.cash // 3) * 2
            lost = lost_before - self.cash
            message("SUBWAY EVENT",
                    ["YOU WERE MUGGED!", "Lost $" + str(lost),
                     "Cash left $" + str(self.cash)],
                    RED)

        elif event == 12 or event == 13:
            self.gun_offer()

        elif event == 14:
            if confirm("STRANGE WEED",
                       "Smoke the stuff you found?"):
                message("BAD IDEA",
                        ["YOU HALLUCINATE...", "stumble onto the tracks,",
                         "and get hit by a train."],
                        RED)
                self.dead = True
                self.finished = True

        elif event == 15:
            if self.cash >= 300:
                if confirm("TRENCHCOAT",
                           "Bigger coat for $200?"):
                    self.capacity += 10
                    self.cash -= 200
                    message("TRENCHCOAT",
                            ["Capacity increased!", "New capacity: " +
                             str(self.capacity)],
                            GREEN)

        elif event == 16:
            if self.free_space() >= 8:
                amount = randint(1, 7)
                which = randint(0, 5)
                self.inv[which] += amount
                message("SUBWAY FIND",
                        ["YOU FOUND DRUGS!", str(amount) + " " + DRUGS[which],
                         "on a dead guy."],
                        YELLOW)

        elif event == 17:
            self.prices[ACID] = randint(250, 799)
            message("MARKET EVENT",
                    ["CHEAP ACID!", "Homemade acid flooded", "the market."],
                    YELLOW)

        elif event in (9, 10, 11):
            if sum(self.inv) >= 50:
                if event == 9:
                    deputies = 1
                elif event == 10:
                    deputies = 3
                else:
                    deputies = 4
                self.police_chase(deputies)

    def gun_offer(self):
        if self.cash < 500 or self.free_space() < 5:
            return

        names = ["BERETTA", "SAT. NIGHT SPECIAL", ".44 MAGNUM"]
        gun = names[randint(0, 2)]

        if confirm("GUN OFFER", gun + " for $400?"):
            self.guns += 1
            self.cash -= 400
            message("GUN PURCHASED",
                    ["Guns: " + str(self.guns),
                     "Free coat space: " + str(self.free_space())],
                    GREEN)

    # ------------------------
    # Police chase / combat
    # ------------------------

    def police_chase(self, deputies):
        enemies = deputies + 1

        message("POLICE!",
                ["OFFICER HARDASS", "+ " + str(deputies) + " deputies",
                 "are after you!"],
                RED)

        while enemies > 0 and not self.finished:
            items = ["Run", "Fight", "View guns", "View damage"]
            c = choose_menu(
                "BEING CHASED",
                str(enemies) + " cops",
                items,
                "Guns " + str(self.guns),
                "Damage " + str(self.damage) + "/50"
            )

            if c == -1:
                c = 0

            if c == 0:
                if randint(0, 1) == 0:
                    message("ESCAPED!",
                            ["You lost them", "in an alley."],
                            GREEN)
                    return
                else:
                    message("NO ESCAPE",
                            ["You can't shake them!"],
                            RED)
                    if self.police_fire():
                        return

            elif c == 1:
                if self.guns <= 0:
                    message("NO GUNS",
                            ["You have to run!"],
                            RED)
                    continue

                if randint(0, 1) == 0:
                    message("YOU FIRED",
                            ["You missed!"],
                            ORANGE)
                else:
                    enemies -= 1
                    if enemies <= 0:
                        self.police_victory()
                        return
                    message("YOU FIRED",
                            ["You hit one!", str(enemies) + " left."],
                            GREEN)

                if self.police_fire():
                    return

            elif c == 2:
                message("GUNS",
                        ["You have " + str(self.guns),
                         "gun(s).",
                         "Each uses 5 coat slots."],
                        YELLOW)

            elif c == 3:
                message("DAMAGE",
                        ["Damage: " + str(self.damage) + "/50",
                         "50 damage = death."],
                        RED)

    def police_fire(self):
        if randint(0, 1) == 0:
            message("POLICE FIRE",
                    ["They fired...", "and MISSED!"],
                    GREEN)
            return False

        self.damage += 3
        message("POLICE FIRE",
                ["YOU'VE BEEN HIT!", "Damage: " +
                 str(self.damage) + "/50"],
                RED)

        if self.damage >= 50:
            message("GAME OVER",
                    ["YOU'VE BEEN KILLED!"],
                    RED)
            self.dead = True
            self.finished = True
            return True

        return False

    def police_victory(self):
        loot = randint(750, 1999)
        self.cash += loot

        message("CHASE OVER",
                ["You got them all!", "Found $" + str(loot),
                 "on Officer Hardass."],
                GREEN)

        if self.cash >= 1200 and self.damage > 0:
            if confirm("DOCTOR", "Pay $1000 to heal?"):
                self.cash -= 1000
                self.damage = 0
                message("DOCTOR",
                        ["Damage reset to 0."],
                        GREEN)

    # ------------------------
    # Status / score
    # ------------------------

    def status_screen(self):
        begin_screen()
        header("STATUS", "Day " + str(self.day) + "/30")

        text(12, 51, "Location", GRAY)
        text(120, 51, self.location_name(), CYAN)

        text(12, 78, "Cash", GRAY)
        text(120, 78, "$" + str(self.cash), GREEN)

        text(12, 105, "Debt", GRAY)
        text(120, 105, "$" + str(self.debt), RED)

        text(12, 132, "Bank", GRAY)
        text(120, 132, "$" + str(self.bank), GREEN)

        text(12, 159, "Coat", GRAY)
        text(120, 159,
             str(self.used_space()) + "/" + str(self.capacity),
             WHITE)

        text(205, 159, "Guns " + str(self.guns), YELLOW)

        footer("ENTER/ESC: Back")
        end_screen()
        wait_enter_or_esc()

    def score_screen(self):
        net = self.bank + self.cash - self.debt

        if net < 0:
            score = 0
        else:
            score = int(round((net / 31.5) ** 0.5))
            if score > 100:
                score = 100

        begin_screen()
        header("GAME OVER")

        text(20, 55, "Cash", GRAY)
        text(160, 55, "$" + str(self.cash), GREEN)

        text(20, 82, "Bank", GRAY)
        text(160, 82, "$" + str(self.bank), GREEN)

        text(20, 109, "Debt", GRAY)
        text(160, 109, "$" + str(self.debt), RED)

        text(20, 136, "Net worth", GRAY)
        text(160, 136, "$" + str(net), CYAN)

        text(20, 166, "SCORE", YELLOW)
        text(160, 166, str(score) + " / 100", YELLOW)

        footer("ENTER: Continue")
        end_screen()
        wait_enter_or_esc()

    # ------------------------
    # Main menu
    # ------------------------

    def main_menu(self):
        items = [
            "Prices",
            "Trenchcoat",
            "Buy",
            "Sell",
            "Travel",
            "Loan Shark",
            "Bank",
            "Status",
            "Quit Game"
        ]

        sel = 0

        while not self.finished:
            begin_screen()
            header("DRUG WAR", "Day " + str(self.day) + "/30")

            text(7, 43, self.location_name(), CYAN)
            text(117, 43, "Cash $" + str(self.cash), GREEN)
            text(224, 43, "Debt $" + str(self.debt), RED)

            # Two-column menu fits comfortably.
            positions = [
                (10, 72), (163, 72),
                (10, 97), (163, 97),
                (10, 122), (163, 122),
                (10, 147), (163, 147),
                (10, 172)
            ]

            for i, item in enumerate(items):
                x, y = positions[i]
                if i == sel:
                    rect(x - 3, y - 17, 145, 21, DARK)
                    text(x, y, "> " + item, YELLOW)
                else:
                    text(x, y, "  " + item, WHITE)

            footer("ARROWS: Move", "ENTER: Select ESC:Quit")
            end_screen()

            k = wait_key()

            if k == "up":
                # move one logical row up
                if sel >= 2:
                    sel -= 2
            elif k == "down":
                if sel <= 6:
                    sel += 2
                elif sel == 7:
                    sel = 8
            elif k == "left":
                if sel % 2 == 1:
                    sel -= 1
            elif k == "right":
                if sel % 2 == 0 and sel < 7:
                    sel += 1
            elif k == "esc":
                if confirm("QUIT GAME", "Quit this game?"):
                    self.quit_early = True
                    self.finished = True
                    return
            elif k == "enter":
                if sel == 0:
                    self.prices_screen()
                elif sel == 1:
                    self.coat_screen()
                elif sel == 2:
                    self.buy()
                elif sel == 3:
                    self.sell()
                elif sel == 4:
                    self.travel()
                elif sel == 5:
                    self.loan_menu()
                elif sel == 6:
                    self.bank_menu()
                elif sel == 7:
                    self.status_screen()
                elif sel == 8:
                    if confirm("QUIT GAME", "Quit this game?"):
                        self.quit_early = True
                        self.finished = True
                        return

    def run(self):
        if not self.title_screen():
            self.quit_early = True
            self.finished = True
            return

        if confirm("INSTRUCTIONS", "View instructions?"):
            self.instructions()

        self.roll_prices()

        if not self.finished:
            self.main_menu()

        if not self.quit_early:
            self.score_screen()

# ----------------------------
# Program loop
# ----------------------------

def main():
    # Buffered drawing avoids flicker while each full screen is redrawn.
    use_buffer()

    try:
        clear_history()
    except:
        pass

    while True:
        g = Game()
        g.run()

        if g.quit_early:
            break

        if not confirm("PLAY AGAIN", "Start another game?"):
            break

    begin_screen()
    header("DRUG WARS")
    text(77, 96, "Thanks for playing.", CYAN)
    text(72, 132, "Press ENTER to exit.", YELLOW)
    end_screen()
    wait_enter_or_esc()

    clear()

main()
