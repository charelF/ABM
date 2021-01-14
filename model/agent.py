from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random
import numpy as np
from utilities import *

class RegionAgent(GeoAgent):

    def __init__(self, unique_id, model, shape):
        """Create a new Schelling agent.

        Args:
            unique_id: Unique identifier for the agent.
        """
        super().__init__(unique_id, model, shape)
        self.wealth = None
        self.cooperativeness = None  # between -1 and 1
        self.strategy = None  # 1 = cooperate, 2 = defect

    def update_cooperativeness(self, neighbor):
        if self.strategy == 1:
            # if I cooperate, my neighbors cooperativess will go up
            neighbor.cooperativeness = min(neighbor.cooperativeness + 0.1, 1)
        else:
            neighbor.cooperativeness = max(neighbor.cooperativeness - 0.1, -1)
        
        if neigbor.strategy == 1:
            self.cooperativeness = min(self.cooperativeness + 0.1, 1)
        else:
            self.cooperativeness = max(self.cooperativeness - 0.1, -1)

    def CC(self, neighbor):
        self.wealth += self.model.member_trade_reward
        self.wealth += self.model.union_payoff
        neighbor.wealth += self.model.member_trade_reward
        neighbor.wealth += self.model.union_payoff

    def CD(self, neighbor):
        self.wealth += self.model.basic_trade_reward
        self.wealth += self.model.union_payoff
        self.cooperativeness = max(self.cooperativeness + 0.1, 1)
        neighbor.wealth += self.model.basic_trade_reward
        
    def DC(self, neighbor):
        self.wealth += self.model.basic_trade_reward
        neighbor.wealth += self.model.basic_trade_reward
        neighbor.wealth += self.model.union_payoff

    def DD(self, neighbor):
        self.wealth += self.model.basic_trade_reward
        neighbor.wealth += self.model.basic_trade_reward


    # def defect(self, neighbor, defect):
    #     """
    #     defect indicates who defects: 1 is neighbour
    #     -1 is self.
    #     """
    #     self.country.wealth     -= defect * self.model.defect_reward
    #     neighbor.country.wealth += defect * self.model.defect_reward                

    # def both_defect(self, neighbor):

    #     self.country.wealth     -= self.model.defect_reward
    #     neighbor.country.wealth -= self.model.defect_reward  

    def interact(self, neighbor):
        if self.strategy == 1:
            if neighbor.strategy == 1:
                self.CC(neighbor)
            else:
                self.CD(neighbor)
        else:
            if neighbor.strategy == 1:
                self.DC(neighbor)
            else:
                self.DD(neighbor)

    def choose_strategy(self):

        if (self.cooperativeness +
            self.model.union_payoff + 
            self.model.member_trade_reward -
            self.model.basic_trade_reward) > 0:
            # cooperates
            self.strat = 1
        else:
            self.strat = 2

    def get_neighbor(self):
        while True:
            neighbor = random.choice(self.model.agents)
            if neighbor != self:
                return neighbor

    def step(self):
        self.choose_strategy()
        neighbor = self.get_neighbor()
        self.interact(neighbor)









        # """Advance agent one step."""

        # # See if country has interacted
        # if self.country.interacted:
        #     return
        # # New code
        # # try:
        # # commenting out the try except becaus it catches all kinds of errors, can be reactivated later
        # # neighbor = random.choice(self.model.grid.get_neighbors(self))
        

        # neighbor.country.interacted = True
        # self.country.interacted = True
                        
        # # if neighbor.country == self.country:
        # #     self.trade(neighbor)
        # #     self.country.traded = True
        # # else:
        # self.country.traded = self.choose_interaction()
        # neighbor.country.traded = neighbor.choose_interaction()

        # # Update nation params
        # if self.country.trade:
        #     self.country.trades += 1
        # if neighbor.country.trade:
        #     neighbor.country.trades += 1
        
        # # Interaction
        # if self.country.trade and neighbor.country.trade:
        #     self.trade(neighbor)
        #     self.country.attacked = False
        #     self.neighbour.attacked = False
        # # Read doc of defect to understand 1, -1 args.
        # elif self.country.trade and not neighbor.country.trade:
        #     self.country.attacked = True
        #     self.neighbour.attacked = False
        #     self.defect(neighbor, 1)
        # elif self.country.trade and not neighbor.country.trade:
        #     self.country.attacked = False
        #     self.neighbour.attacked = True
        #     self.defect(neighbor, -1)
        # else:
        #     self.country.attacked = True
        #     self.neighbour.attacked = True
        #     self.both_defect(neighbor)
        # # except:
        # #     # When country has no neighbors
        # #     self.country.traded = False

    def __repr__(self):
        return "Agent " + str(self.unique_id)