class Item:
  def __init__(self, name, cost, description, single_use=False, quantity=1):
    self.name = name
    self.cost = cost
    self.description = description
    self.single_use = single_use
    self.quantity = quantity