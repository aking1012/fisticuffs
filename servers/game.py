from .models import Stacks, Deck, PlayerData
import os, sys

#Got to work this in somehow uuddlrlrba

class Game():
  '''
  Game modes inclulde visible, inivisible, with_depth, and memory
  visible - all cards are visible - debug mode
  inivisible - only your cards are visible
  with_depth - invisible with opponent stack depth available
  memory - the way the game was meant to be played/highest difficulty
  '''
  def __init__(self, players):
    turn_list = ['blue', 'red', 'green', 'purple', 'black', 'white']
    self.turn = 0
    self.turn_list = turn_list[:(players)]
    print(self.turn_list)
    self.initialized = []
    self.players = {}
    self.game_mode = 'visible'
    self.dead_list = []
    self.last_move = [-1]*5
    self.player_count = 0

  def assign_cards(self, current_player):
    while len(current_player.deck)>0:
      selection = False
      #Is card available?
      while not current_player.deck.valid_selection(selection):
        self.clear()
        print("Player " + str(self.turn_list[self.turn]) + " please complete your stack layout.")
        print('Deck assignment starts at stack 0 at the bottom and progresses up, then across')
        stack, depth = divmod(abs(25 - len(current_player.deck)), 5)
        print('Currently stack number:' + str(stack) + ' Distance from bottom ' + str(depth))
        print('------------------------------------------------------------------------------')
        print(current_player.stack)
        current_player.deck.show_remaining()
        selection = input("Select card:")
        #TODO add preconfigured deck layouts for "play the pawn trade layout" etc

      #Remove card from deck and place in stacks
      current_player.stack.push_first(current_player.deck.pop_first(selection))
    self.clear()
    print(current_player.stack)
    do_over = input("Make a mistake? (y/n)")
    if do_over == 'y':
      current_player.deck = Deck(current_player.color)
      current_player.stack = Stacks(current_player.color)
      self.assign_cards(current_player)

  def init(self, player_count):
    self.turn = 0
    self.initialized = []
    self.player_count = player_count
    while len(self.initialized) < player_count:
      self.turn = len(self.initialized)
      current_player = PlayerData(self.turn_list[self.turn])
      self.players[self.turn_list[self.turn]] = current_player
      self.assign_cards(current_player)
      self.initialized.append(self.turn_list[len(self.initialized)])
    self.turn = 0

  def clear(self):
    #Not going to make this cross-platform - since the CLI is just an iteration.
    #It's a function just in case though.
    os.system('clear')

  def check_victory(self):
    print(len(self.dead_list))
    print(len(self.players))
    if len(self.dead_list)+1 == len(self.players):
      for player in self.players:
        if self.players[player].color not in self.dead_list:
          print(self.players[player].color + " wins")
          sys.exit()


  def valid_opponent(self, opponent):
    try:
      if self.turn_list[opponent] not in self.dead_list \
        and self.turn_list[opponent] != self.current_player.color:
        return opponent
      else:
        return 'derp'
    except:
      return 'derp'

  def opponents(self):
    #Used derp instead of false or True to work around magic casting of ints and Booleans
    select_opponent = 'derp'
    while select_opponent == 'derp':
      for player in self.players:
        if self.players[player].color not in self.dead_list \
            and self.players[player].color != self.current_player.color:
          lens = []
          exists = ['']*5
          for stack in self.players[player].stack.cards:
            lens.append(len(stack))
            exists[len(lens)-1] = 'X'
          print(self.players[player].color + ' ' + \
            str(self.turn_list.index(self.players[player].color)))
          print()
          #TODO and last move indicator
          print([str(item) for item in lens])
          print(exists)
      select_opponent = int(input("Select opponent by number:"))
      select_opponent = self.valid_opponent(select_opponent)
    self.opponent = int(select_opponent)

  def attacker_selection(self):
    selection = 'derp'
    while not self.current_player.stack.valid(selection):
      self.clear()
      print(self.current_player.stack)
      selection = int(input("Select stack to use:"))
    self.attacker = selection

  def valid_opponent_stack(self, stack):
    player = self.players[self.turn_list[self.opponent]]
    if len(player.stack.cards[stack]) > 0:
      return stack
    else:
      return 'derp'

  def target_selection(self):
    '''
    a lot duplicated between here and select opponent.
    should probably be broken out into a separate function used twice

    display opponent stacks
    select stack
    '''
    select_opponent_stack = 'derp'
    while select_opponent_stack == 'derp':
      #TODO you are here...
      player = self.players[self.turn_list[self.opponent]]
      lens = []
      exists = ['']*5
      for stack in player.stack.cards:
        lens.append(len(stack))
        exists[len(lens)-1] = 'X'
      #TODO last move indicator
      print([str(item) for item in lens])
      print(exists)
      select_opponent_stack = int(input("Select opponent's stack by number:"))
      select_opponent_stack = self.valid_opponent_stack(select_opponent_stack)
    self.opponent_stack = select_opponent_stack

  def combat_mechanic(self):
    '''
    by the original rules, some of these scenarios shouldn't happen...
    '''
    attacker = self.current_player.stack.cards[self.attacker].pop()
    defender = self.players[self.turn_list[self.opponent]].stack.cards[self.opponent_stack].pop()

    if defender.special:
      if defender.name == 'Crown':
        print("Attacker wins")
        self.current_player.stack.cards[self.attacker].append(attacker)
        self.dead_list.append(self.current_player.color)
      elif defender.name == 'Archer':
        print("Attacker wins")
        self.current_player.stack.cards[self.attacker].append(attacker)
      elif defender.name == 'Shield' and attacker.name == 'Archer':
        print("Defender wins")
        self.players[self.turn_list[self.opponent]].stack.cards[self.opponent_stack].append(defender)
      elif defender.name == 'Shield':
        print("Draw")
        pass
    elif attacker.special:
      if attacker.name == 'Crown':
        print("Defender wins")
        self.players[self.turn_list[self.opponent]].stack.cards[self.opponent_stack].append(defender)
      elif attacker.name == 'Archer':
        print("Attacker wins")
        self.current_player.stack.cards[self.attacker].append(attacker)
      elif attacker.name == 'Shield':
        print("Defender wins")
        self.players[self.turn_list[self.opponent]].stack.cards[self.opponent_stack].append(defender)
    elif attacker.power > defender.power:
      print("Attacker wins")
      self.current_player.stack.cards[self.attacker].append(attacker)
    elif defender.power > attacker.power:
      print("Defender wins")
      self.players[self.turn_list[self.opponent]].stack.cards[self.opponent_stack].append(defender)
    else:
      print("Draw")
      pass

  def next_player(self):
    if self.turn < self.player_count - 1:
      self.turn += 1
    else:
      self.turn = 0
    #TODO check for dead player in 3+player games ?? thought I did that, but I really can't remember

  def pause_for_hotseat(self, reason):
    if reason == 'complete':
      input('Turn complete.  Press return/enter to clear the screen')
    elif reason == '':
      input('Opponent turn complete.  Press return/enter to start your turn')

  def run(self):
    self.turn = 0
    while(True):
      #Game loop
      #TODO pull the raw_input's out to here, so the same methods can be
      #used as validators in a client server model
      self.current_player = self.players[self.turn_list[self.turn]]
      self.clear()
      print(self.current_player.color + ' turn')

      #untested victory condition
      self.check_victory()
      self.opponents()
      #TODO here
      self.attacker_selection()
      self.target_selection()
      self.combat_mechanic()
      #untested victory condition
      self.check_victory()
      self.pause_for_hotseat('complete')
      #TODO next player should fire a client server json conversation
      #TODO UE4 GUI that talks to a local server
      #TODO UE4 GUI that talks to a remote server
      #TODO all game logic should be a simple python server.  The client is the hard part.
      #TODO multiple games, multiple users, player affinity, game affinity
      self.next_player()
      self.clear()
      self.pause_for_hotseat('next')

  def run_server(self):
    #TODO
    #split up client and server
    #jsonsocket for "server"
    #https://github.com/mdebbar/jsonsocket
    #flask app for web ui or REST server
    #some of the comments are braindumps and bookmarks
    pass

  class Games:
    #a class to do Game() aggregation and sorting of game IDs
    def __init__(self):
      pass
