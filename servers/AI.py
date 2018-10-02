class AI():
  def __init__(self, player_data):
    self.player_data = player_data
  def random_stack(self):
    from random import shuffle
    shuffle(self.player_data.deck)
  def defend_row(self, row, power_bias=0, depth_bias=2):
    #Don't use cards from this stack to attack.
    #Bias is how much pain to take in exchange for not using a card in that stack.
    #  If a 3 just attacked you and you have a 4 only on your king stack, but you have a 5 on
    #  a different stack - a bias of 1 would let you not use the 5.
    #Depth bias is how much taller your king stack is allowed to be than the average size of your
    #  other stacks before power bias is ignored.
    #  (Only tip your hand so far on stacks where you don't want to make them shorter)
    #  Bug, king stack must be taller than the other stacks for this calculation to work without a filter.
    pass
  def undefend_row(self, row, power_bias=0, depth_bias=2):
    #Use exclusively cards from this stack to attack to rebalance the stack deviation.
    #Bias is how much pain to take in exchange for not using a card in that stack.
    #  If a 3 just attacked you and you have a 4 only on your king stack, but you have a 5 on
    #  a different stack - a bias of 1 would let you not use the 5.
    #Depth bias is how much taller your king stack is allowed to be than the average size of your
    #  other stacks before power bias is ignored.
    #  (Only tip your hand so far on stacks where you don't want to make them shorter)
    #  Bug, king stack must be taller than the other stacks for this calculation to work without a filter.
    pass
  def ignore_opposing_row(self, row, turns_to_ignore):
    #Ignore an opponent's stack for a given number of turns.
    #If using the same depth_bias logic as before from the other side
    #(a given stack should be no further from the rest, or it is being intentionally not used to attack)
    pass
  def hammer_row(self, row, turns_to_hammer):
    #If the engine determines a row is important, treat it with maximum prejudice for this many turns.
    #Hard to implement, because if you are already working on another stack intentionally - this might fire
    #  and screw it up.
    pass
  def overmatch_lowest_known(self, row):
    pass
  def use_dagger(self):
    pass
  def use_sword(self):
    pass
  def use_morningstar(self):
    pass
  def use_halberd(self):
    pass
  def use_axe(self):
    pass
  def use_longsword(self):
    pass
  def use_archer(self):
    pass
