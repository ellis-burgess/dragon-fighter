from item import Item

class Shop:
  SHORTSWORD_COST = 10
  LONGSWORD_COST = 20
  POTION_COST = 5
  STAFF_COST = 30

  def __init__(self, type_dicts):
    self.inventory = []

    self.inventory.append(Item('shortsword', self.SHORTSWORD_COST, 'A simple sword'))
    self.inventory.append(Item(
      'longsword', self.LONGSWORD_COST, 'A long, sharp sword. Dragons beware!'
      ))
    self.inventory.append(Item(
      'healing potion',
      self.POTION_COST,
      'Drinking this potion will restore HP equal to your wisdom score.',
      single_use=True))
        
    for dtype in type_dicts:
      desc = f'Staff imbued with {dtype['type']} magic. Strong against {dtype['strong_against'][0]} and {dtype['strong_against'][1]} dragons.'
      self.inventory.append(
        Item(f'{dtype['type']} staff',
             self.STAFF_COST,
             desc
        )
      )
    self.inventory_names = [i.name for i in self.inventory]
  
  def sell_item(self, item):
    if item.single_use == False:
      self.inventory.remove(item)
      self.inventory_names.remove(item.name)

  def show_inventory(self):
    for item in self.inventory:
      print(f"{item.name} - cost: {item.cost} gold")
      print(item.description)
      print()