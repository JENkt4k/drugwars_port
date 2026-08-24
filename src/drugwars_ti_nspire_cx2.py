# Drug Wars - TI-Nspire CX II Python
# Faithful reimplementation of the classic TI-82/83 Drugwars mechanics.
# The original TI-BASIC source has a variable collision: N is used both
# for heroin inventory and location. This version fixes that bug.
#
# Create a new Python program on the TI-Nspire CX II, choose
# "Random Simulations" (or otherwise ensure random is available),
# paste this code, and run with Ctrl+R.

from random import randint

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

def pause():
    input("ENTER...")

def ask_int(prompt, default=None):
    while True:
        try:
            s = input(prompt)
            if s == "" and default is not None:
                return default
            return int(s)
        except:
            print("Enter a number.")

def yes_no(prompt):
    while True:
        v = ask_int(prompt + " (1=YES,2=NO): ")
        if v == 1:
            return True
        if v == 2:
            return False

def money(n):
    return "$" + str(int(n))

class Game:
    def __init__(self):
        self.cash = 2000
        self.debt = 5000
        self.bank = 0

        self.day = 1
        self.location = 0       # Bronx
        self.guns = 0
        self.damage = 0

        self.capacity = 100
        self.inv = [0, 0, 0, 0, 0, 0]
        self.prices = [0, 0, 0, 0, 0, 0]

        self.dead = False
        self.finished = False

    def used_space(self):
        # Guns consume five coat slots in the original game.
        return sum(self.inv) + self.guns * 5

    def free_space(self):
        return self.capacity - self.used_space()

    def show_title(self):
        print("")
        print("==============================")
        print("       J.M.'S DRUGWAR")
        print("        SIMULATION 2.00")
        print("==============================")
        print("Original IBM game: John E. Dell")
        print("TI version: Jonathan Maier")
        print("")

    def instructions(self):
        print("Buy low and sell high.")
        print("You begin with $2000 and $5000 debt.")
        print("You have 30 days to pay the debt")
        print("and make as much money as possible.")
        print("")
        print("Normal price ranges:")
        print("Cocaine : $16000-$28000")
        print("Heroin  :  $5000-$12000")
        print("Acid    :  $1000-$4400")
        print("Weed    :    $330-$750")
        print("Speed   :     $70-$220")
        print("Ludes   :     $10-$50")
        print("")
        print("Police become a danger when you")
        print("carry a large inventory.")
        pause()

    def roll_prices(self):
        # These reproduce the TI-BASIC formulas closely.
        self.prices[COKE]   = randint(16000, 28000)
        self.prices[HEROIN] = randint(5000, 12000)
        self.prices[ACID]   = randint(10, 44) * 100
        self.prices[WEED]   = randint(33, 75) * 10
        self.prices[SPEED]  = randint(7, 22) * 10
        self.prices[LUDES]  = randint(1, 5) * 10

        # Original effectively rounds rand*20, producing roughly 0..20.
        event = randint(0, 20)
        self.random_event(event)

    def random_event(self, event):
        if event == 1:
            print("")
            print("RIVAL DEALERS ARE SELLING")
            print("CHEAP LUDES!")
            self.prices[LUDES] = 2
            pause()

        elif event == 2:
            print("")
            print("WEED PRICES HAVE BOTTOMED OUT!")
            self.prices[WEED] = 122
            pause()

        elif event == 3:
            print("")
            print("POLICE ARE SELLING CHEAP HEROIN")
            print("FROM LAST WEEK'S RAID!")
            self.prices[HEROIN] = randint(850, 2000)
            pause()

        elif event == 4 or event == 5:
            print("")
            print("ADDICTS ARE BUYING HEROIN")
            print("AT OUTRAGEOUS PRICES!")
            self.prices[HEROIN] = randint(18000, 43000)
            pause()

        elif event == 6 or event == 7:
            print("")
            print("POLICE MADE A BIG COKE BUST!")
            print("PRICES ARE OUTRAGEOUS!")
            self.prices[COKE] = randint(80000, 140000)
            pause()

        elif event == 8:
            print("")
            print("YOU WERE MUGGED IN THE SUBWAY!")
            # Original keeps approximately two thirds of wallet.
            self.cash = (self.cash // 3) * 2
            print("You have", money(self.cash), "left.")
            pause()

        elif event == 12 or event == 13:
            self.gun_offer()

        elif event == 14:
            print("")
            print("THERE'S SOME WEED HERE THAT")
            print("SMELLS LIKE GOOD STUFF.")
            if yes_no("SMOKE IT?"):
                print("")
                print("YOU HALLUCINATE, STUMBLE")
                print("ONTO THE SUBWAY TRACKS,")
                print("AND GET HIT BY A TRAIN.")
                print("")
                print("JUST SAY NO TO DRUGS.")
                pause()
                self.dead = True
                self.finished = True

        elif event == 15:
            if self.cash >= 300:
                print("")
                print("BUY A NEW TRENCHCOAT WITH")
                print("MORE POCKETS FOR $200?")
                if yes_no("BUY COAT?"):
                    self.capacity += 10
                    self.cash -= 200
                    print("Capacity is now", self.capacity)
                    pause()

        elif event == 16:
            if self.free_space() >= 8:
                amount = randint(1, 7)
                which = randint(0, 5)
                self.inv[which] += amount
                print("")
                print("YOU FOUND", amount, "UNITS OF")
                print(DRUGS[which].upper())
                print("ON A DEAD DUDE IN THE SUBWAY!")
                pause()

        elif event == 17:
            print("")
            print("THE MARKET HAS BEEN FLOODED")
            print("WITH CHEAP HOMEMADE ACID!")
            self.prices[ACID] = randint(250, 799)
            pause()

        elif event == 9 or event == 10 or event == 11:
            if sum(self.inv) >= 50:
                # Original maps these event values to 1, 3, or 4 deputies
                # plus Officer Hardass.
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

        guns = ["BERETTA", "SATURDAY NIGHT SPECIAL", ".44 MAGNUM"]
        gun_name = guns[randint(0, 2)]

        print("")
        print("WILL YOU BUY A")
        print(gun_name)
        print("FOR $400?")

        if yes_no("BUY GUN?"):
            self.guns += 1
            self.cash -= 400
            print("Guns:", self.guns)
            pause()

    def police_chase(self, deputies):
        # The BASIC stores deputies separately and treats Officer Hardass
        # as one additional pursuer.
        enemies = deputies + 1

        print("")
        print("OFFICER HARDASS AND", deputies)
        print("OF HIS DEPUTIES ARE AFTER YOU!")
        pause()

        while enemies > 0 and not self.finished:
            print("")
            print("===== BEING CHASED =====")
            print("1. View guns")
            print("2. View damage")
            print("3. Number of police")
            print("4. Run")
            print("5. Fight")
            c = ask_int("> ")

            if c == 1:
                print("You have", self.guns, "gun(s).")
                pause()

            elif c == 2:
                print("Damage:", self.damage)
                print("50 damage = death.")
                pause()

            elif c == 3:
                print(enemies, "police still chasing you.")
                pause()

            elif c == 4:
                if randint(0, 1) == 0:
                    print("YOU LOST THEM IN AN ALLEY!")
                    pause()
                    return
                else:
                    print("YOU CAN'T SHAKE THEM!")
                    pause()
                    if self.police_fire():
                        return

            elif c == 5:
                if self.guns == 0:
                    print("YOU DON'T HAVE ANY GUNS!")
                    print("YOU HAVE TO RUN!")
                    pause()
                    continue

                if randint(0, 1) == 0:
                    print("YOU MISSED!")
                    pause()
                else:
                    enemies -= 1
                    print("YOU KILLED ONE!")
                    pause()

                    if enemies <= 0:
                        self.police_victory()
                        return

                if self.police_fire():
                    return

    def police_fire(self):
        print("")
        print("THEY'RE FIRING AT YOU!")

        if randint(0, 1) == 0:
            print("THEY MISSED!")
            pause()
            return False

        print("YOU'VE BEEN HIT!")
        self.damage += 3
        print("Damage:", self.damage)
        pause()

        if self.damage >= 50:
            print("YOU'VE BEEN KILLED!")
            pause()
            self.dead = True
            self.finished = True
            return True

        return False

    def police_victory(self):
        print("")
        print("YOU KILLED ALL OF THEM!")
        loot = randint(750, 1999)
        self.cash += loot
        print("You found", money(loot),
              "on Officer Hardass.")
        pause()

        if self.cash >= 1200:
            print("")
            if yes_no("PAY $1000 FOR A DOCTOR?"):
                self.cash -= 1000
                self.damage = 0
                print("Damage reset to 0.")
                pause()

    def show_prices(self):
        print("")
        print("DAY", self.day, "-", LOCATIONS[self.location])
        print("------------------------------")
        for i in range(6):
            print(str(i + 1) + ".", DRUGS[i],
                  money(self.prices[i]))
        print("------------------------------")
        print("Wallet:", money(self.cash))
        print("Debt  :", money(self.debt))
        print("Bank  :", money(self.bank))

    def show_coat(self):
        print("")
        print("===== TRENCHCOAT =====")
        for i in range(6):
            print(str(i + 1) + ".", DRUGS[i], self.inv[i])
        print("Guns:", self.guns, "(5 spaces each)")
        print("Capacity:", self.capacity)
        print("Free space:", self.free_space())
        print("Damage:", self.damage)
        pause()

    def choose_drug(self, prompt):
        while True:
            self.show_prices()
            print("0. Cancel")
            choice = ask_int(prompt)
            if choice == 0:
                return -1
            if 1 <= choice <= 6:
                return choice - 1
            print("Invalid choice.")

    def buy(self):
        d = self.choose_drug("Buy which #? ")
        if d < 0:
            return

        price = self.prices[d]
        max_cash = self.cash // price
        max_hold = self.free_space()
        max_qty = min(max_cash, max_hold)

        print("You can afford:", max_cash)
        print("You can hold  :", max_hold)

        qty = ask_int("How many? ")
        if qty < 0 or qty > max_qty:
            print("Can't do that.")
            pause()
            return

        self.inv[d] += qty
        self.cash -= qty * price

    def sell(self):
        d = self.choose_drug("Sell which #? ")
        if d < 0:
            return

        print("You have:", self.inv[d])
        qty = ask_int("How many? ")

        if qty < 0 or qty > self.inv[d]:
            print("Can't do that.")
            pause()
            return

        self.inv[d] -= qty
        self.cash += qty * self.prices[d]

    def travel(self):
        print("")
        print("===== WHERE TO, DUDE? =====")
        for i in range(len(LOCATIONS)):
            print(str(i + 1) + ".", LOCATIONS[i])
        print("0. Stay here")

        choice = ask_int("> ")
        if choice == 0:
            return False
        if choice < 1 or choice > len(LOCATIONS):
            return False

        dest = choice - 1
        if dest == self.location:
            print("You're already there.")
            pause()
            return False

        self.location = dest

        print("")
        print("          SUBWAY")
        print("")

        self.day += 1

        # Original: debt grows 10% every travel day.
        self.debt = int(self.debt * 1.10)

        # Original bank earns 6% every travel day.
        self.bank = int(self.bank * 1.06)

        if self.day >= 31:
            self.finished = True
            return True

        self.roll_prices()
        return True

    def loan_shark(self):
        if self.location != 0:
            print("THE LOAN SHARK ONLY DEALS")
            print("IN THE BRONX.")
            pause()
            return

        while True:
            print("")
            print("===== LOAN SHARK =====")
            print("Debt:", money(self.debt))
            print("Cash:", money(self.cash))
            print("1. Repay")
            print("2. Borrow")
            print("0. Goodbye")
            c = ask_int("> ")

            if c == 0:
                return

            elif c == 1:
                amt = ask_int("Repay how much? ")
                if 0 <= amt <= self.cash and amt <= self.debt:
                    self.cash -= amt
                    self.debt -= amt
                    return
                print("Invalid amount.")

            elif c == 2:
                amt = ask_int("Borrow how much more? ")
                if 0 <= amt <= 5000:
                    self.cash += amt
                    self.debt += amt
                    return
                print("Maximum additional loan is $5000.")

    def bank_menu(self):
        if self.location != 0:
            print("THE BANK IS IN THE BRONX.")
            pause()
            return

        while True:
            print("")
            print("===== BANK =====")
            print("Account:", money(self.bank))
            print("Wallet :", money(self.cash))
            print("1. View account")
            print("2. Deposit")
            print("3. Withdraw")
            print("0. Goodbye")
            c = ask_int("> ")

            if c == 0:
                return

            elif c == 1:
                print("Your account =", money(self.bank))
                pause()

            elif c == 2:
                amt = ask_int("Deposit how much? ")
                if 0 <= amt <= self.cash:
                    self.cash -= amt
                    self.bank += amt
                else:
                    print("Invalid amount.")

            elif c == 3:
                amt = ask_int("Withdraw how much? ")
                if 0 <= amt <= self.bank:
                    self.bank -= amt
                    self.cash += amt
                else:
                    print("Invalid amount.")

    def score(self):
        net = self.bank + self.cash - self.debt

        if net < 0:
            score = 0
        else:
            # Original BASIC formula:
            # sqrt(netWorth / 31.5), capped at 100.
            score = int(round((net / 31.5) ** 0.5))
            if score > 100:
                score = 100

        print("")
        print("==============================")
        print("          GAME OVER")
        print("==============================")
        print("Cash :", money(self.cash))
        print("Bank :", money(self.bank))
        print("Debt :", money(self.debt))
        print("Net  :", money(net))
        print("")
        print("YOUR SCORE (0-100):", score)
        print("")

        return score

    def main_menu(self):
        while not self.finished:
            print("")
            print("==============================")
            print("DRUGWAR!  DAY", self.day, "/ 30")
            print(LOCATIONS[self.location])
            print("==============================")
            print("1. See prices")
            print("2. Trenchcoat")
            print("3. Buy")
            print("4. Sell")
            print("5. Jet")
            print("6. See loan shark")
            print("7. Visit bank")
            print("0. Status")

            c = ask_int("> ")

            if c == 1:
                self.show_prices()
                pause()
            elif c == 2:
                self.show_coat()
            elif c == 3:
                self.buy()
            elif c == 4:
                self.sell()
            elif c == 5:
                self.travel()
            elif c == 6:
                self.loan_shark()
            elif c == 7:
                self.bank_menu()
            elif c == 0:
                self.show_prices()
                print("Free space:", self.free_space())
                print("Guns:", self.guns)
                print("Damage:", self.damage)
                pause()

    def run(self):
        self.show_title()
        if yes_no("INSTRUCTIONS?"):
            self.instructions()

        self.roll_prices()

        if not self.finished:
            self.main_menu()

        self.score()

def play():
    while True:
        g = Game()
        g.run()
        if not yes_no("PLAY AGAIN?"):
            print("")
            print("THANKS FOR PLAYING!")
            print("REMEMBER: WATCH YOUR BACK.")
            break

play()
