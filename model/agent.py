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
        super().__init__(unique_id, model, shape)
        self.wealth = None
        self.cooperativeness = None  # between -1 and 1
        self.strategy = None  # 1 = cooperate, 2 = defect
        self.efficiency = None
    
    def CC(self, neighbor):
        self.wealth += self.model.member_trade_reward * self.wealth
        neighbor.wealth += self.model.member_trade_reward * neighbor.wealth
        self.eu_bonus += (self.model.member_trade_reward - self.model.basic_trade_reward) * self.wealth
        neighbor.eu_bonus += (self.model.member_trade_reward - self.model.basic_trade_reward) * neighbor.wealth


    def CD(self, neighbor):
        self.wealth += self.model.basic_trade_reward * self.wealth
        #self.wealth += self.model.union_payoff
        neighbor.wealth += self.model.basic_trade_reward * neighbor.wealth
        neighbor.fictional_bonus += (self.model.member_trade_reward - self.model.basic_trade_reward) *  neighbor.wealth
        
    def DC(self, neighbor):
        self.wealth += self.model.basic_trade_reward * self.wealth
        neighbor.wealth += self.model.basic_trade_reward * neighbor.wealth
        #neighbor.wealth += self.model.union_payoff
        self.fictional_bonus += (self.model.member_trade_reward - self.model.basic_trade_reward) * self.wealth

    def DD(self, neighbor):
        self.wealth += self.model.basic_trade_reward * self.wealth
        neighbor.wealth += self.model.basic_trade_reward * neighbor.wealth

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

    def update_cooperativeness(self, neighbor):
            if self.strategy == 1:
                # if I cooperate, my neighbors cooperativess will go up
                neighbor.cooperativeness = min(neighbor.cooperativeness + self.model.neighbor_influence, 1)
            else:
                neighbor.cooperativeness = max(neighbor.cooperativeness - self.model.neighbor_influence, -1)
            if neighbor.strategy == 1:
                self.cooperativeness = min(self.cooperativeness + self.model.neighbor_influence, 1)
            else:
                self.cooperativeness = max(self.cooperativeness - self.model.neighbor_influence, -1)
                    

    def compare_neighbors(self):
        neighbors = self.model.grid.get_neighbors(self)
        if not neighbors: return 0
        neighbor_strats = [neighbor.strategy for neighbor in neighbors]
        average_neighbor_strat = sum(neighbor_strats) / len(neighbor_strats)  # between 1 and 2
        redistributed_average = (average_neighbor_strat * 2) - 3  # now between -1 and 1
        return redistributed_average
        # if not neighbors:
        #     return 0
        # cooperating_neighbors = 0
        # for neigh in neighbors:
        #     if neigh.strategy == 1:
        #         cooperating_neighbors += 1
        # return (cooperating_neighbors/ len(neighbors) - 1/2)

    # def choose_strategy(self):
    #     decision = (
    #         self.cooperativeness
    #         + self.model.union_payoff
    #         + self.model.member_trade_reward
    #         - self.model.basic_trade_reward
    #         # + random.uniform(-0.1, 0.1)
    #     )
    #     if decision > 0:
    #         self.strategy = 1
    #     elif decision < 0:
    #         self.strategy = 2
    #     else:
    #         self.strategy = random.choice([1,2])

    def pay_tax(self):
        self.tax = self.wealth * self.model.eutax
        self.wealth = self.wealth * (1 - self.model.eutax)
        self.model.treasury += self.tax
        self.wealth = self.wealth * self.efficiency

    def choose_strategy(self):
        decision = (
            self.cooperativeness
            + self.compare_neighbors()
            + random.uniform(-self.model.weight, self.model.weight)
        )
        if decision > 0:
            self.strategy = 1
        else:
            self.strategy = 2


    def get_neighbor(self):
        # there is a 1/(len(agents)) chance we trade with ourself lol
        if random.random() < self.model.vision:
            neighbor = random.choice(self.model.agents)
        else:
            try:
                neighbor = random.choice(self.model.grid.get_neighbors(self))
            except:
                neighbor = random.choice(self.model.agents)
    
        return neighbor
        
    def step(self):
        self.choose_strategy()
        self.pay_tax()
        neighbor = self.get_neighbor()
        self.interact(neighbor)
        self.update_cooperativeness(neighbor)

    def __repr__(self):
        return "Agent " + str(self.unique_id)