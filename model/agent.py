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
        self.has_interacted = False
    
    def CC(self, neighbor):
        self.wealth += self.model.member_trade_reward * self.wealth
        neighbor.wealth += self.model.member_trade_reward * neighbor.wealth
        self.eu_bonus = (self.model.member_trade_reward - self.model.basic_trade_reward) * self.wealth
        neighbor.eu_bonus = (self.model.member_trade_reward - self.model.basic_trade_reward) * neighbor.wealth


    def CD(self, neighbor):
        self.wealth += self.model.basic_trade_reward * self.wealth
        neighbor.wealth += self.model.basic_trade_reward * neighbor.wealth
        neighbor.fictional_bonus = (self.model.member_trade_reward - self.model.basic_trade_reward) *  neighbor.wealth
        self.eu_bonus = (self.model.member_trade_reward - self.model.basic_trade_reward) *  self.wealth
        
    def DC(self, neighbor):
        self.wealth += self.model.basic_trade_reward * self.wealth
        neighbor.wealth += self.model.basic_trade_reward * neighbor.wealth
        self.fictional_bonus = (self.model.member_trade_reward - self.model.basic_trade_reward) * self.wealth
        neighbor.eu_bonus = (self.model.member_trade_reward - self.model.basic_trade_reward) * neighbor.wealth

    def DD(self, neighbor):
        self.wealth += self.model.basic_trade_reward * self.wealth
        neighbor.wealth += self.model.basic_trade_reward * neighbor.wealth
        self.fictional_bonus = (self.model.member_trade_reward - self.model.basic_trade_reward) * self.wealth
        neighbor.fictional_bonus = (self.model.member_trade_reward - self.model.basic_trade_reward) *  neighbor.wealth


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

    def compare_neighbors(self):
        neighbors = self.model.grid.get_neighbors(self)
        if not neighbors:
            return
        neighbor_cooperativeness = [neighbor.cooperativeness for neighbor in neighbors]
        average_neighbor_cooperativeness = sum(neighbor_cooperativeness) / len(neighbor_cooperativeness)
        if average_neighbor_cooperativeness > 0:
            self.cooperativeness = min(self.cooperativeness + self.model.neighbor_influence, 1)
        elif average_neighbor_cooperativeness < 0:
            self.cooperativeness = max(self.cooperativeness - self.model.neighbor_influence, -1)
            

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

    def update_wealth(self):
        if self.strategy == 1:
            # pay tax
            self.tax = self.wealth * self.model.eutax
            self.wealth = self.wealth * (1 - self.model.eutax)
            self.model.treasury += self.tax
        
        # update wealth based on efficiency
        self.wealth += self.wealth * self.efficiency



    def choose_strategy(self):
        if self.cooperativeness > 0:
            self.strategy = 1
        else:
            self.strategy = 2


    def get_neighbor(self):
        # there is a 1/(len(agents)) chance we trade with ourself lol
        if random.random() < self.model.vision:
            neighbor = random.choice([agent for agent in self.model.agents if agent.has_interacted == False])
        else:
            try:
                neighbor = random.choice([agent for agent in self.model.grid.get_neighbors(self) if agent.has_interacted == False])
            except:
                neighbor = random.choice([agent for agent in self.model.agents if agent.has_interacted == False])
    
        return neighbor
        
    def step(self):
        self.choose_strategy()
        self.update_wealth
        if not self.has_interacted:
            neighbor = self.get_neighbor()
            self.interact(neighbor)
            neighbor.has_interacted = True
            self.compare_neighbors()

        

    def __repr__(self):
        return "Agent " + str(self.unique_id)