from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random
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
        """
            computes wealth and trade_bonus resulting from the (C,C) strategy profile
        """
        self.wealth += math.log((self.wealth + neighbor.wealth) / 2) * self.model.member_trade_multiplier
        neighbor.wealth += math.log((self.wealth + neighbor.wealth) / 2) * self.model.member_trade_multiplier
        self.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)
        neighbor.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)
        


    def CD(self, neighbor):
        """
            computes wealth and trade_bonus resulting from the (C,D) strategy profile
        """
        self.wealth += math.log((self.wealth + neighbor.wealth) / 2)
        neighbor.wealth += math.log((self.wealth + neighbor.wealth) / 2)
        self.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)
        neighbor.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)
        


    def DC(self, neighbor):
        """
            computes wealth and trade_bonus resulting from the (D, C) strategy profile
        """
        self.wealth += math.log((self.wealth + neighbor.wealth) / 2)
        neighbor.wealth += math.log((self.wealth + neighbor.wealth) / 2)
        self.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)
        neighbor.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)
        


    def DD(self, neighbor):
        """
            computes wealth and trade_bonus resulting from the (D, D) strategy profile
        """
        self.wealth += math.log((self.wealth + neighbor.wealth) / 2)
        neighbor.wealth += math.log((self.wealth + neighbor.wealth) / 2)
        self.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)
        neighbor.trade_bonus = math.log((self.wealth + neighbor.wealth) / 2) * (self.model.member_trade_multiplier - 1)



    def trade(self, neighbor):
        """
            Computes the resulting strategy profile of a game where self and neighbour meet
            Both agents can play any of the 2 available strategies
        """
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
            Adjusts cooperativness based on the cooperativeness of the neighbors
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
        """
            Computes wealth growth of an agent which represents its GDP growth in real life
            Each agent has an efficiency parameter which is initialised randomly
            To add more randomness to this growth and make it less predictable, we compute
            a step_efficiency which slightly deviates the efficiency of an agent.
        """
        step_efficiency = abs(self.efficiency + random.gauss(mu=0, sigma=self.model.efficiency_stdev/4))
        self.wealth += math.log(self.wealth) * step_efficiency



    def choose_strategy(self):
        """
            Agents chose a strategy based on their cooperativeness
        """
        decision = self.cooperativeness  # + random.uniform(-self.model.randomness, self.model.randomness)
        if decision > 0: 
            self.strategy = 1
        else:
            self.strategy = 2



    def get_trade_partner(self):
        """
            Depending on whether international trade is enabled or not, this finds a trading partner
            for an agent among the neighbouring regions or on an international scale
            Returns a trade_partner of type RegionAgent.
        """
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
            # each agent only trades once per step, which works since we have exactly 320 agents,
            # so the first 160 agents pick a trading partner among the remaining 160.
            trade_partner = self.get_trade_partner()
            self.trade(trade_partner)
            trade_partner.has_traded = True
        


    def __repr__(self):
        return "Agent " + str(self.unique_id)