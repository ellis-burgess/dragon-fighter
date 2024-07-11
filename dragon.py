import random

class Dragon:
  STAT_PER_LEVEL = 2
  HP_MULTIPLIER = 3
  DRAGON_NAME_STARTS = ['Azur', 'Bal', 'Chion', 'Drak', 'El', 'Faelen',
                        'Graan', 'Hioch', 'Ionar', 'Jaarkan', 'Kalion',
                        'Liomar', 'Maakaan', 'Nirak', 'Obdir', 'Panak',
                        'Quetz', 'Rochar', 'Stakar', 'Tiam', 'Unaark',
                        'Viirnok', 'Wadion', 'Xarak', 'Yiich', 'Zorak']
  DRAGON_NAME_ENDS = ['aan', 'boch', 'chin', 'dan', 'emak', 'fael',
                      'gorak', 'haaken', 'ioch', 'jurdir', 'kamak',
                      'liir', 'morn', 'nak', 'oran', 'piiran', 'quital',
                      'raedan', 'stork', 'tamat', 'uhumat', 'varan',
                      'wiikaren', 'xiaan', 'yran', 'zakaan']

  def __init__(self, level, dtype):
    if isinstance(dtype, list):
      self.dtype = random.choice(dtype)
    else:
      self.dtype = dtype

    self.level = level
    if self.level > 5:
      self.name = f"{random.choice(self.DRAGON_NAME_STARTS)}{random.choice(self.DRAGON_NAME_ENDS)}, the "
    else:
      self.name = ''
    if self.level > 10:
      self.name += 'Great '
    self.name += f"{self.dtype} dragon".title()

    stat_count = self.STAT_PER_LEVEL * level
    self.stats = {'Strength': 1, 'Dexterity': 1, 'Wisdom': 1, 'Constitution': 1}
    for i in range(stat_count):
      self.stats[random.choice(('Strength', 'Wisdom', 'Dexterity', 'Constitution'))] += 1
    
    self.max_hp = self.HP_MULTIPLIER * self.stats['Constitution']
    self.hp = self.max_hp
    self.breath_weapon = True

  def print_dragon(self):
    dragon_info = [f"{self.name}"]
    dragon_info.append(f"Level: {self.level}")
    for stat in self.stats.keys():
      dragon_info.append(f"{stat}: {self.stats[stat]}")
    dragon_info.append(f"Type: {self.dtype}")
    dragon_info.append(f"HP: {self.hp}/{self.max_hp}")
    return "\n".join(dragon_info)