import random

from player import Player
from dragon import Dragon
from shop import Shop
from item import Item

type_dict = [
  {'type': 'electric', 'strong_against': ['grass', 'psychic']},
  {'type': 'fire', 'strong_against': ['rock', 'poison']},
  {'type': 'ghost', 'strong_against': ['fire', 'water']},
  {'type': 'grass', 'strong_against': ['rock', 'water']},
  {'type': 'poison', 'strong_against': ['ghost', 'grass']},
  {'type': 'psychic', 'strong_against': ['poison', 'ghost']},
  {'type': 'rock', 'strong_against': ['electric', 'psychic']},
  {'type': 'water', 'strong_against': ['electric', 'fire']}
  ]

stat_keys = ['strength', 'dexterity', 'wisdom', 'constitution']

game_options = {
  'fight dragon': 'Fight a random dragon',
  'view details': 'View your current stats',
  'visit shop': 'Visit the local shop',
  'equip weapon': 'Equip a weapon from your inventory',
  'rest': 'Rest to refill your health to full',
  'help': 'View available commands',
  'exit': 'End the game'
}

class Game:
  def __init__(self):
    name = input("What is your name? ")
    print(f"Welcome, {name}.")
    print("The aim of this game is to defeat a level 10 dragon.")
    print("Dragons will only face enemies the same level as themselves or higher.")
    print("You can buy equipment from the shop.")
    print("Good luck!")
    print()
    self.player = Player(name)
    self.shop = Shop(type_dict)

  def fight_dragon(self):
    print("A dragon appears!")
    if self.player.level > 10:
      level = random.randint(9, self.player.level)
    else:
      level = random.randint(0, self.player.level)
    self.dragon = Dragon(level, [t['type'] for t in type_dict])
    print(self.dragon.print_dragon())
    print()
    print(self.player.print_player())

    # local copy of player and dragon stats
    player_stats = self.player.stats
    dragon_stats = self.dragon.stats
    defending = False

    while self.player.hp > 0 and self.dragon.hp > 0:
      print(f"Your HP: {self.player.hp}/{self.player.max_hp}")
      print(f"Dragon's HP: {self.dragon.hp}/{self.dragon.max_hp}")
      player_action = input("What do you do? Attack, defend, change weapon, heal, or run away: ").lower()
      print()
      if defending == True:
        player_stats['Dexterity'] -= 2
        defending = False

      if player_action == 'attack':
        score_to_hit = (player_stats['Dexterity'] / dragon_stats['Dexterity'])
        if random.randint(0, 100) / 100 > score_to_hit:
          print("The dragon dodges your attack!")
          continue
        if self.player.weapon == None:
          attack = self.player.stats['Strength']
        else:
          attack = (player_stats[self.player.weapon['stat'].title()] + self.player.weapon['bonus'])
          weapon_type = next((t for t in type_dict if t['type'] == self.player.weapon['dtype']), None)
          dragon_type = next((t for t in type_dict if t['type'] == self.dragon.dtype), None)
          if weapon_type != None and dragon_type['type'] in weapon_type['strong_against']:
            attack = int(attack * 1.5)
            print("Yes! This staff is super effective against this dragon!")

        self.dragon.hp -= attack
        print(f"You hit the dragon for {attack} points of damage!")
        
      elif player_action == 'defend':
        print("You will be slightly harder to hit this turn.")
        player_stats['Dexterity'] += 2
        defending = True
        
      elif player_action == 'change weapon':
        self.equip_weapon()

      elif player_action == 'heal':
        potion = next((i for i in self.player.inventory if i.name == 'healing potion'), None)
        if potion == None or potion.quantity == 0:
          print("You don't have any healing potions!")
          print("You missed your turn while you were rummaging in your bag.")
        else:
          self.player.hp = min(self.player.max_hp, self.player.hp + self.player.stats['Wisdom'])
          print(f"You drink a potion. You now have {self.player.hp} HP.")
          potion.quantity -= 1

        
      elif player_action == 'run away':
        score_to_escape = (player_stats['Dexterity'] / dragon_stats['Dexterity'])
        if random.randint(0, 100) / 100 <= score_to_escape:
          print("You successfully escape the dragon!")
          return
        else:
          print("The dragon blocks your path.")
        
      else:
        print("Unrecognised command. Try again.")
      
      if self.dragon.hp <= 0:
        break

      d_score_to_hit = (dragon_stats['Dexterity'] / player_stats['Dexterity'])
      if random.randint(0, 100) / 100 > d_score_to_hit:
        if self.dragon.breath_weapon == True:
          self.dragon.breath_weapon = False
          print("The dragon tried to use its breath attack, but it missed!")
        else:
          print("The dragon took a swipe at you, but it missed!")
      else:
        if self.dragon.breath_weapon == True:
          self.dragon.breath_weapon = False
          attack = int(dragon_stats['Wisdom'] * 1.5)
        else:
          attack = dragon_stats['Strength']
        print(f"The dragon hits you for {attack} points of damage!")
        self.player.hp -= attack
    
    if self.dragon.hp <= 0:
      exp_gain = max(1, 10 - (self.player.level - self.dragon.level))
      gold_gain = random.randint(1, 10) * (self.dragon.level + 1)
      print(f"You have slain the dragon! You gain {exp_gain} experience points and {gold_gain} gold coins.")
      self.player.exp += exp_gain
      self.player.gold += gold_gain
    elif self.player.hp <= 0:
      print("The dragon defeated you.")
      if self.player.level == self.dragon.level:
        print("You flee with the last inch of your strength back to the local town.")
        self.player.hp = 1
      else:
        print("Game over. You had the following stats:")
        print(self.player.print_player())
        exit()
    else:
      print("You escaped from the fight.")

  def view_details(self):
    print(self.player.print_player())

  def visit_shop(self):
    print("You're visiting the shop. It has the following items for sale:")
    self.shop.show_inventory()
    sel = input("Enter the name of an item you wish to buy, or 'exit' to leave the shop: ")
    while sel.lower() != 'exit':
      if sel.lower() not in self.shop.inventory_names:
        sel = input("Invalid selection. Please try again: ")
        continue
      sel = next((i for i in self.shop.inventory if i.name == sel), None)
      if self.player.buy_item(sel) == True:
        self.shop.sell_item(sel)
        print(f"You bought the {sel.name}. You now have {self.player.gold} gold coins.")
      sel = input("Enter the name of an item you wish to buy, or 'exit' to leave the shop: ")
    print("Come again soon!")
    return
  
  def equip_weapon(self):
    weapons = [w for w in self.player.inventory if 'sword' in w.name or 'staff' in w.name]
    if len(weapons) == 0:
      print("You don't have any weapons. Go to the shop to buy one.")
      return
    print("Please select a weapon to equip. You have the following options:")
    for w in weapons:
      print(f" - {w.name.title()}")
    weapon_choice = None
    while weapon_choice is None:
        user_input = input('').lower()
        weapon_choice = next((w for w in weapons if w.name.lower() == user_input), None)
        if weapon_choice is None:
            print("Invalid selection. Please try again.")
        self.player.equip_weapon(weapon_choice)

  def rest(self):
    self.player.hp = self.player.max_hp
    print("You spend a night at a local tavern and restore your health to full.")
  
  def help(self):
    for (op, desc) in game_options.items():
      print(f"{op}: {desc}")

  def exit(self):
    print("Thanks for playing!")
    exit()

  def print_new_level(self):
    print(f"You are now level {self.player.level}! Your stats have improved:")
    for (k, v) in self.player.stats.items():
      print(f"{k.title()}: {v}")
    print(f"Your Max HP is now {self.player.max_hp}")

  def end_game(self):
    print("You did it! You defeated a level 10 dragon!")
    print("Thank you for playing!")
    exit()

  def main(self):
    print("The following commands are available:")
    self.help()

    cmd = ''
    while cmd != 'exit':
      if self.player.exp >= 10:
        self.player.level_up(1)
        self.print_new_level()
      cmd = input("Enter a command: ")
      print()
      if cmd in game_options.keys():
        cmd = getattr(self, '_'.join(cmd.lower().split(' ')))
        cmd()
      else:
        print("Command not recognised.")


if __name__ == '__main__':
  game = Game()
  game.main()