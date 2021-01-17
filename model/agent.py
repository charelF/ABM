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
        self.has_traded = False
        self.tax_payed = 0
    

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


    def trade(self, neighbor):
        print(self.wealth)
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
        print(self.wealth)


    def compute_neighbor_influence(self):
        """
        adjusts cooperativness based on the cooperativeness of the neighbors
        if average cooperativeness of all neighbors bigger (smaller) than 0:
            adds (removes) 'neighbor_influence' from cooperativeness
        """
        neighbors = self.model.grid.get_neighbors(self)
        if neighbors:  # only if neighbors exist
            neighbor_cooperativeness = [neighbor.cooperativeness for neighbor in neighbors]
            average_neighbor_cooperativeness = sum(neighbor_cooperativeness) / len(neighbor_cooperativeness)
            if average_neighbor_cooperativeness > 0:
                self.cooperativeness = min(self.cooperativeness + self.model.neighbor_influence, 1)
            elif average_neighbor_cooperativeness < 0:
                self.cooperativeness = max(self.cooperativeness - self.model.neighbor_influence, -1)
            

    def natural_growth(self):
        self.wealth += self.wealth * self.efficiency


    def choose_strategy(self):
        if self.cooperativeness > 0: 
            self.strategy = 1
        else:
            self.strategy = 2


    def get_trade_partner(self):
        # there is a 1/(len(agents)) chance we trade with ourself lol
        if random.random() < self.model.vision:
            trade_partner = random.choice([agent for agent in self.model.agents if agent.has_traded == False])
        else:
            try:
                trade_partner = random.choice([agent for agent in self.model.grid.get_neighbors(self) if agent.has_traded == False])
            except:
                trade_partner = random.choice([agent for agent in self.model.agents if agent.has_traded == False])
    
        return trade_partner
        
    def step(self):
        self.choose_strategy()
        self.compute_neighbor_influence()
        self.natural_growth()
        if not self.has_traded:
            trade_partner = self.get_trade_partner()
            self.trade(trade_partner)
            trade_partner.has_traded = True
        

    def __repr__(self):
        return "Agent " + str(self.unique_id)