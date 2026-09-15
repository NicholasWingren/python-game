import game_save as g
import random as r
class Armor:
    def __init__ (self, protection, material, price, full_protection):
        self.protection = protection
        self.material = material
        self.price = price
        self.repair_cost = price
        self.full_protection = full_protection

    

class Card:
    def __init__(self, name, multiplier, extra_turns, units):
        self.name = name
        self.multiplier = multiplier
        self.extra_turns = extra_turns
        self.units = units
        self.price = 30
        
    def __str__ (self):
        return f"{self.name}: You have {self.units} card(s) with a {self.multiplier} damage multiplier and {self.extra_turns} extra turn(s)"
        

class Player:
    def __init__ (self, name, weapon, armor, money):
        self.name = name
        self.health = 100
        self.weapon=weapon
        self.armor=armor
        self.money=money
        self.inventory = []
        self.selected_card = no_card
        
    def load_data(self, data):
        self.name = data.name
        self.health = data.health
        self.weapon = Weapon(data.weapon.name, data.weapon.price, data.weapon.damage, data.weapon.ammo, data.weapon.full_ammo, data.weapon.ammo_price)
        self.armor = Armor(data.armor.protection, data.armor.material, data.armor.price, data.armor.full_protection)
        self.money = data.money
        self.inventory = data.inventory
        
    
    def add_money(self, value):
        self.money += value
    
    def buy_weapon(self,new_weapon):
        if self.money >= new_weapon.price:
            self.weapon = new_weapon
            self.money -= new_weapon.price
            print(f"You equipped the {self.weapon.name}. You have {self.money} money left")
        else:
            print("You do not have enough money")
        
   
    def attack(self,player):
        if self.weapon.ammo > 0:
            damage = self.weapon.damage
            if self.selected_card.multiplier > 0:
                damage *= (1+self.selected_card.multiplier)
                self.selected_card = no_card  
                
            player.take_damage(damage)
            self.weapon.ammo -= 1
            print(f"You dealt {damage} damage")
        else:
            print("You do not have enough ammo to attack. Buy more ammo")
   
    def buy_armor(self, new_armor):
        if self.money >= new_armor.price:
            self.armor = new_armor
            self.money -= new_armor.price               
            print(f"You equipped {self.armor.material} armor")
        else:
            print("You do not have enough money")

    def use_card(self):
        card = input("Choose the card you want to use: ")
        if card == card0.name:
            self.selected_card = card0
        elif card == card1.name:
            self.selected_card = card1
        elif card == card2.name:
            self.selected_card = card2        
        print(f"You equipped the card: {self.selected_card.name}")    
        
            

    def buy_card(self):
        card = deck[r.randint(0,len(deck)-1)]
        if self.money >= card.price:
            found = False
            for i in range(0,len(self.inventory)):
                if (self.inventory[i].name == card.name):
                    self.inventory[i].units += 1
                    found = True
            if (found == False):                
                self.inventory.append(card)
                
            self.money -= card.price
            print(f"You received 1 card with a {card.multiplier} damage multiplier and {card.extra_turns} extra turn(s)")
            
  
        else:
            print("You do not have enough money")
            
        
    
    def take_damage(self, weapon_damage):
        self.armor.protection -= weapon_damage
        if (self.armor.protection <= 0):          
            self.health += self.armor.protection 
            self.armor.protection = 0
   
    def buy_ammo(self, player):        
        self.money -= player.weapon.ammo_price
        player.weapon.ammo += (player.weapon.full_ammo-player.weapon.ammo)
        print(f"Your {player.weapon.name} is refilled to {player.weapon.full_ammo} ammo")
 
    def repair_armor(self, player):
        self.money -= player.armor.repair_cost
        player.armor.protection += (player.armor.full_protection-player.armor.protection)
    
    def __str__(self):
        return f" {self.name} te equipada la/el {self.weapon.name} i l'armor de {self.armor.material}.\n Te {self.health} de health y {self.armor.protection} de protection de l'escut. \n Disposa de {self.money} de money "


class Weapon:
    def __init__ (self, name, price, damage, ammo, full_ammo, ammo_price):
        self.name = name
        self.price = price
        self.damage = damage
        self.ammo = ammo
        self.full_ammo = full_ammo        
        self.ammo_price = ammo_price
        
    def __str__(self):
        return f"The {self.name} deals {self.damage} damage and has {self.ammo} ammo" 

    







no_card = Card("noCard",0,0,1)
card0 = Card("multiplier de damage",1,0,1)
card1 = Card("turn extra", 0,1,1)
card2 = Card("mixed", 1,1,1)

deck=[card0,card1,card2]   
   

# PLAYER 1 WEAPONS
pistol1=Weapon("Pistol", 5, 5, 5, 5, 5 )
smg1=Weapon("SMG", 10, 10, 20, 20, 5)
shotgun1=Weapon("Shotgun", 10, 20, 7, 7, 5)
sniper1=Weapon("Sniper", 20, 40, 5, 5, 10)
rifle1=Weapon("Rifle", 30, 30, 15, 15, 15)

# PLAYER 2 WEAPONS
pistol2=Weapon("Pistol", 5, 5, 5, 5, 5 )
smg2=Weapon("SMG", 10, 10, 20, 20, 5)
shotgun2=Weapon("Shotgun", 10, 20, 7, 7, 5)
sniper2=Weapon("Sniper", 20, 40, 5, 5, 10)
rifle2=Weapon("Rifle", 30, 30, 15, 15, 15)



# PLAYER 1 ARMOR
no_armor1=Armor(0,"none",0, 0)
wood1=Armor(20,"wood",20, 20)
stone1=Armor(40,"stone",50, 50)
metal1=Armor(80,"metal",100, 50)

# PLAYER 1 ARMOR
no_armor2=Armor(0,"none",0, 0)
wood2=Armor(20,"wood",20,20)
stone2=Armor(50,"stone",50 ,50)
metal2=Armor(100,"metal",100, 100)


option = input("Do you want to start a new game? ") 

if option == "yes":         
    player1 = Player(input("Enter player 1 name: "), pistol1, no_armor1, 90)
    player2 = Player(input("Enter player 2 name: "), pistol2, no_armor2, 90)      
    round_counter=1
    turn=0
    data=[player1,player2, round_counter, turn]

if option == "no":
    game = g.GameSave()
    data=game.load_game()
    player1 = Player("","","","")
    player1.load_data(data[0])
    player2 = Player("","","","")
    player2.load_data(data[1])
    round_counter = data[2]
    turn = data[3]
    
    
while player1.health > 0 and player2.health > 0:
    if option == "0":
        break
    player1.add_money(10)
    player2.add_money(10)
    print()
    print(f'ROUND {round_counter}')
    round_counter+=1
    while turn%2 == 0:
        
        game=g.GameSave()
        game.save_game(data)
        print()
        print(f"Turn: {player1.name}")
        print()
        print(f"Money: {player1.money}")
        print(f"Health: {player1.health}")
        print()
        option = input("0- Exit the program. \n1- Attack. \n2- Buy armor. \n3- Buy weapon. \n4- Buy ammo. \n5- Repair armor. \n6- Buy card. \n7- Use card. \n8- View player stats. \n9- View weapon stats. \nChoose an option: ")
        print()
       
        if option == "0":
            print("The program has stopped")
            break
            
       
        if option == "1":
           player1.attack(player2)
           turn+=1
           if player1.selected_card.extra_turns > 0:
               turn-=1
               player1.selected_card = no_card  
    
        elif option == "2":
            purchased = False
            while purchased == False:
                armor=input("Prices -> wood: 20 / stone: 40 / metal: 80: ")
                if armor=="wood":
                    player1.buy_armor(wood1)
                    turn+=1
                    purchased = True
                elif armor=="stone":
                    player1.buy_armor(stone1)
                    turn+=1
                    purchased = True
                elif armor=="metal":
                    player1.buy_armor(metal1)
                    turn+=1
                    purchased = True
                else: 
                    print()
                    print("Invalid entry. Please type the option exactly as shown")
            if player1.selected_card.extra_turns > 0:
                    turn-=1
                    player1.selected_card = no_card  
                       
        
        elif option == "3":              
            purchased = False
            while purchased == False:            
                weapon=input("Prices -> pistol: 5 / shotgun: 10 / smg: 10 / sniper: 20 / rifle: 30: ")
                if weapon=="smg":
                    player1.buy_weapon(smg1)
                    turn+=1
                    purchased = True
                elif weapon=="pistol":
                    player1.buy_weapon(pistol1)
                    turn+=1
                    purchased = True
                elif weapon=="shotgun":
                    player1.buy_weapon(shotgun1)
                    turn+=1
                    purchased = True
                elif weapon=="sniper":
                    player1.buy_weapon(sniper1)
                    turn+=1
                    purchased = True
                elif weapon=="rifle":
                    player1.buy_weapon(rifle1)
                    turn+=1
                    purchased = True
                else: 
                    print()
                    print("Invalid entry. Please type the option exactly as shown")
                if player1.selected_card.extra_turns > 0:
                        turn-=1
                        player1.selected_card = no_card 
        
        elif option == "4":
            player1.buy_ammo(player1)
            turn+=1
            if player1.selected_card.extra_turns > 0:
                    turn-=1
                    player1.selected_card = no_card 
        
        elif option == "5":
            player1.repair_armor(player1)
            turn+=1
            if player1.selected_card.extra_turns > 0:
                    turn-=1
                    player1.selected_card = no_card            

        elif option == "6":
            player1.buy_card()                    

            
        elif option == "7":
            for card in player1.inventory:
                print(card)  
            player1.use_card()
            turn+=1
            if player1.selected_card.extra_turns > 0:
                    turn-=1
                    player1.selected_card = no_card
            
        elif option == "8":
               print(player1)
               
        elif option == "9":
               print(player1.weapon)
            
            
        else:
            print()
            print("The option you entered is not valid. Please choose another one")
            
        


    while turn%2!=0:
        if (player2.health < 0):
            print(f"{player1.name} has won")
            break
        if option == "0":
            break
        
        game = g.GameSave()
        data = [player1, player2, round_counter, turn]
        game.save_game(data)
        
        print()
        print(f"Turn: {player2.name}")
        print()
        print(f"Money: {player2.money}")
        print(f"Health: {player2.health}")
        print()
        option = input("0- Exit the program. \n1- Attack. \n2- Buy armor. \n3- Buy weapon. \n4- Buy ammo. \n5- Repair armor. \n6- Buy card. \n7- Use card. \n8- View player stats. \n9- View weapon stats. \nChoose an option: ")
        print()
        if option == "0":
            print("The program has stopped")
            break
        
        if option == "1":   
            player2.attack(player1)
            turn+=1
            if player2.selected_card.extra_turns > 0:
                    turn-=1
                    player2.selected_card = no_card 
        
        elif option == "2":
            purchased = False
            while purchased == False:
                armor=input("Prices -> wood: 20 / stone: 40 / metal: 80: ")
                if armor=="wood":
                    player2.buy_armor(wood2)
                    turn+=1
                    purchased = True
                elif armor=="stone":
                    player2.buy_armor(stone2)
                    turn+=1
                    purchased = True
                elif armor=="metal":
                    player2.buy_armor(metal2)
                    turn+=1
                    purchased = True
                else: 
                    print()
                    print("Invalid entry. Please type the option exactly as shown")
            if player2.selected_card.extra_turns > 0:
                    turn-=1
                    player2.selected_card = no_card 

        elif option == "3":
            purchased = False
            while purchased == False:
                weapon=input("Prices -> pistol: 5 / shotgun: 10 / smg: 10 / sniper: 20 / rifle: 30: ")
                if weapon=="smg":
                    player2.buy_weapon(smg2)
                    turn+=1
                    purchased = True
                elif weapon=="pistol":
                    player2.buy_weapon(pistol2)
                    turn+=1
                    purchased = True
                elif weapon=="shotgun":
                    player2.buy_weapon(shotgun2)
                    turn+=1
                    purchased = True
                elif weapon=="sniper":
                    player2.buy_weapon(sniper2)
                    turn+=1
                    purchased = True
                elif weapon=="rifle":
                    player2.buy_weapon(rifle2)
                    turn+=1
                    purchased = True
                else: 
                    print()
                    print("Invalid entry. Please type the option exactly as shown")
            if player2.selected_card.extra_turns > 0:
                    turn-=1
                    player2.selected_card = no_card       
        elif option == "4":
            player2.buy_ammo(player2)
            turn+=1
            if player2.selected_card.extra_turns > 0:
                    turn-=1
                    player2.selected_card = no_card 
        
        elif option == "5":
            player2.repair_armor(player2)
            turn+=1
            if player2.selected_card.extra_turns > 0:
                    turn-=1
                    player2.selected_card = no_card            

        elif option == "6":
            player2.buy_card()                    

            
        elif option == "7":
            for card in player2.inventory:
                print(card)  
            player2.use_card()
            turn+=1
            if player2.selected_card.extra_turns > 0:
                    turn-=1
                    player2.selected_card = no_card
          

        elif option == "8":
               print(player2)
               
        elif option == "9":
               print(player2.weapon)

            
        else:
            print()
            print("The option you entered is not valid. Please choose another one")

               
        if player1.health < 0:
            print(f"{player2.name} has won")
            break