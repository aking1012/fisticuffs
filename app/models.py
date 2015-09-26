from collections import Counter
from .AI import AI

class PlayerData():
  def __init__(self, color):
    self.color = color
    self.stack = Stacks(color)
    self.deck = Deck(color)
    self.seen_cards = Stacks(color)
    self.ai = AI(color)
    self.last_move = []*5

class Stacks:
  '''
  For seen cards map
  unseen = -1

  For stack arrangement
  unassigned = -1
  '''
  def __init__(self, color):
    self.cards = [[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    self.color = color

  def validate_assignment(self, cards_list):
    #TODO 
    return True

  def assign_stacks(self, cards_list):
    if self.validate_assignment(cards_list):
      pass
    pass

  def assign(self, deck):
    pass

  def is_avail(self, stack, distance_from_bottom):
    #Not used, but could be if instead of sequentially ordering stacks, x,y coords are used to assign
    if self.cards[stack][distance_from_bottom] == -1:
      return True

  def get_first_avail(self):
    i=0
    for stack in self.cards:
      try:
        j = stack.index(-1)
        return i, j
      except ValueError as e:
        i+=1
    return i, j

  def valid(self, selection):
    '''
    strip -1
    '''
    try:
      if selection == 'derp':
        return False
      stack = self.cards[:]
      test = stack[selection]
      test = list(filter((-1).__gt__, test))
      print(test)
      if test:
        return True
      else:
        return False
    except:
      return False

  def push_first(self, card):
    xy = self.get_first_avail()
    self.cards[xy[0]][xy[1]] = card

  def __repr__(self):
    #Build item strings
    card_strings = [['' for i in range(5)] for j in range(5)]
    x=0
    for stack in self.cards:
      y=0
      for card in stack:
        if type(card) == int:
          card_strings[x][y] = ' ' * 13
        else:
          card_strings[x][y] = card.name + ' ' * card.padding
          if card.power == 0:
            card_strings[x][y] += ' '
          else:
            card_strings[x][y] += str(card.power)
        y += 1
      while y < 5:
        print('adding a string...')
        card_strings[x][y] = ' ' * 13
        y+=1

      y = 0
      x += 1
    #Build rows
    x = 4
    card_string = ''
    while x >= 0:
      y = 0
      while y < 5:
        card_string += card_strings[y][x]
        card_string += ' '
        y += 1
      x -= 1
      card_string += '\n'
    return card_string

'''
class Stack:
  pass
'''

class Deck:
  def __init__(self, color):
    self.color = color
    self.card_num_index = []
    self.cards = [
    Dagger(),
    Dagger(),
    Dagger(),
    Dagger(),
    Dagger(),
    Sword(),
    Sword(),
    Sword(),
    Sword(),
    Sword(),
    MorningStar(),
    MorningStar(),
    MorningStar(),
    Halberd(),
    Halberd(),
    Halberd(),
    Axe(),
    Axe(),
    Longsword(),
    Longsword(),
    Archer(),
    Archer(),
    Shield(),
    Shield(),
    Crown()
    ]

  def remaining(self):
    temp = []
    for card in self.cards:
      temp.append(card.name)
    remaining = Counter(temp)
    remaining_list = [
      ['Daggers', remaining['Dagger']],
      ['Swords', remaining['Sword']],
      ['Morningstars', remaining['Morningstar']],
      ['Halberds', remaining['Halberd']],
      ['Axes', remaining['Axe']],
      ['Longswords', remaining['Longsword']],
      ['Archers', remaining['Archer']],
      ['Shields', remaining['Shield']],
      ['Crowns', remaining['Crown']]
      ]
    return remaining_list

  def show_remaining(self):
    print('Cards remaining:')
    i = 0
    for item in self.remaining():
      print(str(i) + ') ' + item[0] + ': ' + str(item[1]))
      i += 1

  def valid_selection(self, selection):
    try:
      if not selection:
        return False
      if self.remaining()[int(selection)][1] > 0:
        return True
      else:
        return False
    except IndexError:
      return False

  def int_to_card_name(self, card_num):
    #TODO shouldn't have to cast to an int here, it should take an int
    return self.remaining()[int(card_num)][0].rstrip('s')

  def find_first(self, card_num):
    name = self.int_to_card_name(card_num)
    i=0
    for card in self.cards:
      if card.name == name:
        return i
      i += 1
    return False

  def pop_first(self, card_num):
    return self.cards.pop(self.find_first(card_num))
    
  def __len__(self):
    return self.cards.__len__()

class Card:
  def __init__(self, special, power, name):
    card_number = ['Dagger', 
                   'Sword', 
                   'Morningstar', 
                   'Halberd', 
                   'Axe', 
                   'Longsword', 
                   'Archer', 
                   'Shield', 
                   'Crown']
    self.special = special
    self.power = power
    self.name = name
    self.padding = 12 - len(name)
    self.number = card_number.index(name)

class Dagger(Card):
  def __init__(self):
    super().__init__(special=0, power=1, name='Dagger')

class Sword(Card):
  def __init__(self):
    super().__init__(special=0, power=2, name='Sword')

class MorningStar(Card):
  def __init__(self):
    super().__init__(special=0, power=3, name='Morningstar')

class Halberd(Card):
  def __init__(self):
    super().__init__(special=0, power=4, name='Halberd')

class Axe(Card):
  def __init__(self):
    super().__init__(special=0, power=5, name='Axe')

class Longsword(Card):
  def __init__(self):
    super().__init__(special=0, power=6, name='Longsword')

class Archer(Card):
  def __init__(self):
    super().__init__(special=1, power=0, name='Archer')

class Shield(Card):
  def __init__(self):
    super().__init__(special=1, power=0, name='Shield')

class Crown(Card):
  def __init__(self):
    super().__init__(special=1, power=0, name='Crown')