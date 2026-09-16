import random as r
import game_save as g


class Armor:
    def __init__(self, protection, material, price, full_protection=None):
        self.protection = protection
        self.material = material
        self.price = price
        self.repair_cost = price
        self.full_protection = protection if full_protection is None else full_protection

    def __str__(self):
        return f"{self.material.title()} armor: {self.protection}/{self.full_protection} protection"


class Card:
    def __init__(self, name, multiplier, extra_turns, units=1):
        self.name = name
        self.multiplier = multiplier
        self.extra_turns = extra_turns
        self.units = units
        self.price = 30

    def __str__(self):
        return (
            f"{self.name}: {self.units} card(s), "
            f"{self.multiplier}x bonus damage, {self.extra_turns} extra turn(s)"
        )


class Weapon:
    def __init__(self, name, price, damage, ammo, full_ammo, ammo_price):
        self.name = name
        self.price = price
        self.damage = damage
        self.ammo = ammo
        self.full_ammo = full_ammo
        self.ammo_price = ammo_price

    def __str__(self):
        return (
            f"{self.name}: {self.damage} damage, "
            f"{self.ammo}/{self.full_ammo} ammo"
        )


class Player:
    def __init__(self, name, weapon, armor, money):
        self.name = name
        self.health = 100
        self.weapon = weapon
        self.armor = armor
        self.money = money
        self.inventory = []
        self.selected_card = None

    def load_data(self, data):
        self.name = data.name
        self.health = data.health
        self.weapon = Weapon(
            data.weapon.name,
            data.weapon.price,
            data.weapon.damage,
            data.weapon.ammo,
            data.weapon.full_ammo,
            data.weapon.ammo_price,
        )
        self.armor = Armor(
            data.armor.protection,
            data.armor.material,
            data.armor.price,
            data.armor.full_protection,
        )
        self.money = data.money

        self.inventory = []
        for item in getattr(data, "inventory", []):
            self.inventory.append(
                Card(
                    item.name,
                    item.multiplier,
                    item.extra_turns,
                    getattr(item, "units", 1),
                )
            )

        self.selected_card = None

    def add_money(self, value):
        self.money += value

    def buy_weapon(self, new_weapon):
        if self.money < new_weapon.price:
            print("You do not have enough money.")
            return False

        self.weapon = Weapon(
            new_weapon.name,
            new_weapon.price,
            new_weapon.damage,
            new_weapon.full_ammo,
            new_weapon.full_ammo,
            new_weapon.ammo_price,
        )
        self.money -= new_weapon.price
        print(
            f"You equipped the {self.weapon.name}. "
            f"You have {self.money} money left."
        )
        return True

    def attack(self, opponent):
        if self.weapon.ammo <= 0:
            print("You do not have enough ammo to attack. Buy more ammo.")
            return False, False

        damage = self.weapon.damage
        extra_turn = False

        if self.selected_card is not None:
            if self.selected_card.multiplier > 0:
                damage *= 1 + self.selected_card.multiplier
            extra_turn = self.selected_card.extra_turns > 0
            print(f"Card used: {self.selected_card.name}")
            self.selected_card = None

        opponent.take_damage(damage)
        self.weapon.ammo -= 1
        print(f"You dealt {damage} damage.")
        return True, extra_turn

    def buy_armor(self, new_armor):
        if self.money < new_armor.price:
            print("You do not have enough money.")
            return False

        self.armor = Armor(
            new_armor.full_protection,
            new_armor.material,
            new_armor.price,
            new_armor.full_protection,
        )
        self.money -= new_armor.price
        print(
            f"You equipped {self.armor.material} armor "
            f"with {self.armor.protection} protection."
        )
        return True

    def buy_card(self, deck):
        template = r.choice(deck)

        if self.money < template.price:
            print("You do not have enough money.")
            return False

        for card in self.inventory:
            if card.name == template.name:
                card.units += 1
                break
        else:
            self.inventory.append(
                Card(template.name, template.multiplier, template.extra_turns, 1)
            )

        self.money -= template.price
        print(
            f"You received a '{template.name}' card "
            f"({template.multiplier}x bonus damage, "
            f"{template.extra_turns} extra turn(s))."
        )
        return True

    def use_card(self):
        if not self.inventory:
            print("Your card inventory is empty.")
            return False

        print("Available cards:")
        for card in self.inventory:
            print(f"- {card}")

        choice = input("Choose a card by name: ").strip().lower()

        for card in self.inventory:
            if card.name.lower() == choice:
                self.selected_card = Card(
                    card.name, card.multiplier, card.extra_turns, 1
                )
                card.units -= 1
                if card.units == 0:
                    self.inventory.remove(card)
                print(
                    f"You equipped '{self.selected_card.name}'. "
                    "It will apply to your next successful attack."
                )
                return True

        print("That card is not in your inventory.")
        return False

    def take_damage(self, damage):
        if self.armor.protection > 0:
            absorbed = min(self.armor.protection, damage)
            self.armor.protection -= absorbed
            damage -= absorbed

        if damage > 0:
            self.health = max(0, self.health - damage)

    def buy_ammo(self):
        if self.weapon.ammo == self.weapon.full_ammo:
            print("Your weapon already has full ammo.")
            return False

        if self.money < self.weapon.ammo_price:
            print("You do not have enough money to buy ammo.")
            return False

        self.money -= self.weapon.ammo_price
        self.weapon.ammo = self.weapon.full_ammo
        print(
            f"Your {self.weapon.name} is refilled to "
            f"{self.weapon.full_ammo} ammo."
        )
        return True

    def repair_armor(self):
        if self.armor.full_protection == 0:
            print("You do not have armor to repair.")
            return False

        if self.armor.protection == self.armor.full_protection:
            print("Your armor is already fully repaired.")
            return False

        if self.money < self.armor.repair_cost:
            print("You do not have enough money to repair your armor.")
            return False

        self.money -= self.armor.repair_cost
        self.armor.protection = self.armor.full_protection
        print(
            f"Your {self.armor.material} armor is fully repaired "
            f"to {self.armor.full_protection} protection."
        )
        return True

    def __str__(self):
        armor_name = (
            "No armor"
            if self.armor.full_protection == 0
            else f"{self.armor.material.title()} armor"
        )
        return (
            f"{self.name}\n"
            f"Health: {self.health}\n"
            f"Money: {self.money}\n"
            f"Weapon: {self.weapon}\n"
            f"Armor: {armor_name} "
            f"({self.armor.protection}/{self.armor.full_protection} protection)"
        )


CARD_DECK = [
    Card("Damage Multiplier", 1, 0),
    Card("Extra Turn", 0, 1),
    Card("Mixed", 1, 1),
]

WEAPON_SPECS = {
    "pistol": ("Pistol", 5, 5, 5, 5),
    "smg": ("SMG", 10, 10, 20, 5),
    "shotgun": ("Shotgun", 10, 20, 7, 5),
    "sniper": ("Sniper", 20, 40, 5, 10),
    "rifle": ("Rifle", 30, 30, 15, 15),
}

ARMOR_SPECS = {
    "wood": ("wood", 20, 20),
    "stone": ("stone", 40, 40),
    "metal": ("metal", 80, 80),
}


def make_weapon(key):
    name, price, damage, ammo, ammo_price = WEAPON_SPECS[key]
    return Weapon(name, price, damage, ammo, ammo, ammo_price)


def make_armor(key):
    material, protection, price = ARMOR_SPECS[key]
    return Armor(protection, material, price, protection)


def save_game(player1, player2, round_counter, turn):
    game = g.GameSave()
    data = [player1, player2, round_counter, turn]
    game.save_game(data)


def load_game():
    game = g.GameSave()
    data = game.load_game()

    player1 = Player("", make_weapon("pistol"), Armor(0, "none", 0, 0), 0)
    player2 = Player("", make_weapon("pistol"), Armor(0, "none", 0, 0), 0)
    player1.load_data(data[0])
    player2.load_data(data[1])

    return player1, player2, data[2], data[3]


def choose_weapon(player):
    print("Weapon prices: pistol 5 / shotgun 10 / smg 10 / sniper 20 / rifle 30")
    choice = input("Choose a weapon: ").strip().lower()

    if choice not in WEAPON_SPECS:
        print("Invalid weapon. Please choose one of the listed options.")
        return False

    return player.buy_weapon(make_weapon(choice))


def choose_armor(player):
    print("Armor prices: wood 20 / stone 40 / metal 80")
    choice = input("Choose armor: ").strip().lower()

    if choice not in ARMOR_SPECS:
        print("Invalid armor. Please choose one of the listed options.")
        return False

    return player.buy_armor(make_armor(choice))


def show_menu():
    return input(
        "0- Exit the program.\n"
        "1- Attack.\n"
        "2- Buy armor.\n"
        "3- Buy weapon.\n"
        "4- Buy ammo.\n"
        "5- Repair armor.\n"
        "6- Buy card.\n"
        "7- Use card.\n"
        "8- View player stats.\n"
        "9- View weapon stats.\n"
        "Choose an option: "
    ).strip()


def play_turn(current_player, opponent):
    while True:
        print()
        print(f"Turn: {current_player.name}")
        print(f"Money: {current_player.money}")
        print(f"Health: {current_player.health}")
        print(
            f"Armor: {current_player.armor.protection}/"
            f"{current_player.armor.full_protection}"
        )
        print()

        option = show_menu()
        print()

        if option == "0":
            return "exit", False

        if option == "1":
            success, extra_turn = current_player.attack(opponent)
            if success:
                return "action", extra_turn

        elif option == "2":
            if choose_armor(current_player):
                return "action", False

        elif option == "3":
            if choose_weapon(current_player):
                return "action", False

        elif option == "4":
            if current_player.buy_ammo():
                return "action", False

        elif option == "5":
            if current_player.repair_armor():
                return "action", False

        elif option == "6":
            if current_player.buy_card(CARD_DECK):
                return "action", False

        elif option == "7":
            current_player.use_card()

        elif option == "8":
            print(current_player)

        elif option == "9":
            print(current_player.weapon)

        else:
            print("The option you entered is not valid. Please choose another one.")


def ask_new_or_load():
    while True:
        choice = input("Do you want to start a new game? (yes/no): ").strip().lower()

        if choice in ("yes", "y"):
            player1 = Player(
                input("Enter player 1 name: ").strip(),
                make_weapon("pistol"),
                Armor(0, "none", 0, 0),
                90,
            )
            player2 = Player(
                input("Enter player 2 name: ").strip(),
                make_weapon("pistol"),
                Armor(0, "none", 0, 0),
                90,
            )
            return player1, player2, 1, 0

        if choice in ("no", "n"):
            try:
                return load_game()
            except FileNotFoundError:
                print(
                    "No saved game was found. "
                    "Please start a new game first."
                )

        else:
            print("Please enter 'yes' or 'no'.")


def main():
    player1, player2, round_counter, turn = ask_new_or_load()

    while player1.health > 0 and player2.health > 0:
        player1.add_money(10)
        player2.add_money(10)

        print()
        print(f"ROUND {round_counter}")
        round_counter += 1

        while turn % 2 == 0 and player1.health > 0 and player2.health > 0:
            result, extra_turn = play_turn(player1, player2)

            if result == "exit":
                save_game(player1, player2, round_counter, turn)
                print("Game saved. The program has stopped.")
                return

            if player2.health <= 0:
                print(f"{player1.name} has won!")
                save_game(player1, player2, round_counter, turn)
                return

            if not extra_turn:
                turn += 1

            save_game(player1, player2, round_counter, turn)

        while turn % 2 == 1 and player1.health > 0 and player2.health > 0:
            result, extra_turn = play_turn(player2, player1)

            if result == "exit":
                save_game(player1, player2, round_counter, turn)
                print("Game saved. The program has stopped.")
                return

            if player1.health <= 0:
                print(f"{player2.name} has won!")
                save_game(player1, player2, round_counter, turn)
                return

            if not extra_turn:
                turn += 1

            save_game(player1, player2, round_counter, turn)


if __name__ == "__main__":
    main()
