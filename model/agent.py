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

    def compare_neighs(self):

        neighs = self.model.grid.get_neighbors(self)
        if not neighs:
            return 0
        cooperating_neighs = 0
        for neigh in neighs:
            if neigh.strategy == 1:
                cooperating_neighs += 1
        return (cooperating_neighs/ len(neighs) - 1/2)


    def choose_strategy(self):
        decision = (
            # hardship
            
            # ratio of neighbours that coops
            self.model.weight * self.cooperativeness
            #+ self.model.member_trade_reward
            #- self.model.basic_trade_reward
            + self.compare_neighs()
            # + random.uniform(-0.1, 0.1)
        )
        if decision > 0:

            self.tax = self.wealth * self.model.eu_tax
            self.wealth = self.wealth * (1 - self.model.eu_tax)
            self.model.treasury += self.tax

            self.strategy = 1
        else:
            self.strategy = 2

        self.wealth = self.wealth * self.efficiency
        consumed = self.model.consumption * self.wealth
        self.wealth -= consumed



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
        neighbor = self.get_neighbor()
        self.interact(neighbor)
        #self.update_cooperativeness(neighbor)

    def __repr__(self):
        return "Agent " + str(self.unique_id)