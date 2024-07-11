import math

class Player:
  STATS_PER_LEVEL = 2

  def __init__(self, name, starting_gold=10):
    self.level = 0
    self.stats = {'Strength': 1, 'Dexterity': 1, 'Wisdom': 1, 'Constitution': 1}
    self.name = name
    self.inventory = []
    self.gold = starting_gold
    self.weapon = None
    self.max_hp = 3 * self.stats['Constitution']
    self.hp = self.max_hp
    self.exp = 0
  
  def level_up(self, level_inc):
    self.level += level_inc
    points = self.STATS_PER_LEVEL * level_inc
    for i in range(points):
      stat_choice = input("Which stat do you want to level up? Strength, dexterity, wisdom or constitution? ")
      while stat_choice.title() not in self.stats.keys():
        stat_choice = input("Invalid choice. Please choose a stat from strength, dexterity, wisdom, or constitution: ")
      self.stats[stat_choice.title()] += 1
    cur_hp = self.hp/self.max_hp
    self.max_hp = 3 * self.stats['Constitution']
    self.hp = math.ceil(cur_hp * self.max_hp)
    self.exp -= 10
  
  def print_player(self):
    player_info = [f"Player name: {self.name}"]
    player_info.append(f"Level: {self.level}")
    for stat in self.stats.keys():
      player_info.append(f"{stat}: {self.stats[stat]}")
    
    player_info.append(f"Gold: {self.gold} pieces")
    if len(self.inventory) > 0:
      player_info.append("Inventory:")
    for item in self.inventory:
      player_info.append(f"{item.name.title()}: {item.quantity}")
    
    if self.weapon == None:
      player_info.append("No weapon equipped.")
    else:
      player_info.append(f"Weapon: {self.weapon['type']} equipped: +{self.weapon['bonus'] * self.stats[self.weapon['stat'].title()]} to attacks.")
    
    player_info.append(f"HP: {self.hp}/{self.max_hp}")
    player_info.append(f"EXP: {self.exp} ({10 - self.exp} to next level).")

    return '\n'.join(player_info)

  def buy_item(self, item):
    if self.gold < item.cost:
      print("You cannot afford this item.")
      return False
    else:
      self.gold -= item.cost
      if item.name in [i.name for i in self.inventory]:
        inv_entry = next((i for i in self.inventory if i.name == item.name))
        inv_entry.quantity += 1
      else:
        self.inventory.append(item)
    return True
  
  def equip_weapon(self, weapon):
    if weapon not in self.inventory:
      print("Weapon not found.")
    else:
      self.weapon = {}
      self.weapon['type'] = weapon.name
      self.weapon['bonus'] = 1
      if self.weapon['type'] == 'shortsword' or self.weapon['type'] == 'longsword':
        self.weapon['stat'] = 'strength'
        self.weapon['dtype'] = 'normal'
        if self.weapon['type'] == 'longsword':
          self.weapon['bonus'] += 1
      else:
        self.weapon['stat'] = 'wisdom'
        self.weapon['dtype'] = weapon.name.split(' ')[0]
