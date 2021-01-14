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
        self.wealth += self.model.member_trade_reward
        self.wealth += self.model.union_payoff
        neighbor.wealth += self.model.member_trade_reward
        neighbor.wealth += self.model.union_payoff

    def CD(self, neighbor):
        self.wealth += self.model.basic_trade_reward
        self.wealth += self.model.union_payoff
        neighbor.wealth += self.model.basic_trade_reward
        
    def DC(self, neighbor):
        self.wealth += self.model.basic_trade_reward
        neighbor.wealth += self.model.basic_trade_reward
        neighbor.wealth += self.model.union_payoff

    def DD(self, neighbor):
        self.wealth += self.model.basic_trade_reward
        neighbor.wealth += self.model.basic_trade_reward

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
        decision = (
            self.cooperativeness
            + self.model.union_payoff
            + self.model.member_trade_reward
            - self.model.basic_trade_reward
            # + random.uniform(-0.1, 0.1)
        )
        if decision > 0:
            self.strategy = 1
        elif decision < 0:
            self.strategy = 2
        else:
            self.strategy = random.choice([1,2])

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
        self.update_cooperativeness(neighbor)

    def __repr__(self):
        return "Agent " + str(self.unique_id)