from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random
import numpy as np
from utilities import *
import math

class RegionAgent(GeoAgent):
    def __init__(self, unique_id, model, shape):
        super().__init__(unique_id, model, shape)
        self.wealth = None
        self.cooperativeness = None
        self.strategy = None
        self.efficiency = None
        self.has_traded = False
        self.tax_payed = 0
    


    def CC(self, neighbor):
        self.wealth += math.log((self.wealth + neighbor.wealth) / 2) * self.model.member_trade_multiplier
        neighbor.wealth += math.log((self.wealth + neighbor.wealth) / 2) * self.model.member_trade_multiplier
        self.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)
        neighbor.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)
        


    def CD(self, neighbor):
        self.wealth += math.log((self.wealth + neighbor.wealth) / 2)
        neighbor.wealth += math.log((self.wealth + neighbor.wealth) / 2)
        self.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)
        neighbor.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)
        


    def DC(self, neighbor):
        self.wealth += math.log((self.wealth + neighbor.wealth) / 2)
        neighbor.wealth += math.log((self.wealth + neighbor.wealth) / 2)
        self.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)
        neighbor.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)
        


    def DD(self, neighbor):
        self.wealth += math.log((self.wealth + neighbor.wealth) / 2)
        neighbor.wealth += math.log((self.wealth + neighbor.wealth) / 2)
        self.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)
        neighbor.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)



    def trade(self, neighbor):
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
        step_efficiency = abs(self.efficiency + random.gauss(mu=0, sigma=self.model.efficiency_stdev/4))
        self.wealth += math.log(self.wealth) * step_efficiency



    def choose_strategy(self):
        decision = self.cooperativeness + random.uniform(-self.model.randomness, self.model.randomness)
        if decision > 0: 
            self.strategy = 1
        else:
            self.strategy = 2



    def get_trade_partner(self):
        if self.model.international_trade:
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