from mesa.datacollection import DataCollector
from mesa import Model
from mesa.time import RandomActivation
from mesa_geo.geoagent import GeoAgent, AgentCreator
from mesa_geo import GeoSpace
import random
from agent import *
import numpy as np
import pprint

class RegionModel(Model):
    def __init__(self,
                # basic_trade_reward, member_trade_reward,
                international_trade, max_eff, eutax, neighbor_influence,
                tax_influence, member_trade_multiplier, randomness, eu_strategy):

        # set up parameters
        # self.basic_trade_reward = basic_trade_reward
        # self.member_trade_reward = member_trade_reward
        self.international_trade = international_trade
        self.max_eff = max_eff
        self.eutax = eutax
        self.neighbor_influence = neighbor_influence
        self.tax_influence = tax_influence
        self.member_trade_multiplier = member_trade_multiplier
        self.randomness = randomness
        self.eu_strategy = eu_strategy

        # initialise other attributes
        self.member_count = 0
        self.other_count = 0
        self.treasury = 0
        self.total_wealth = 0
        self.member_wealth = 0
        self.other_wealth = 0
        self.total_eff = 0
        self.member_eff = 0
        self.other_eff = 0
        self.round = 0
        self.schedule = RandomActivation(self)
        self.grid = GeoSpace()
        self.running = True

        # set up grid
        AC = AgentCreator(RegionAgent, {"model": self})
        self.agents = AC.from_file("nuts_rg_60M_2013_lvl_2.geojson")
        self.grid.add_agents(self.agents)

        # set up agents
        for agent in self.agents:
            self.schedule.add(agent)
            cooperativeness = random.uniform(-1, 1)
            agent.cooperativeness = cooperativeness
            agent.strategy = 1 if cooperativeness > 0 else 2
            agent.wealth = 10  # to test out log we cant have it be 1
            # agent.efficiency = max(random.random() * self.max_eff * , 0.0000001)
            agent.efficiency = random.uniform(1, ((self.max_eff - 1) * 2)+1)
            # agent.efficiency = random.uniform()
            # agent.efficiency = agent.SHAPE_AREA * max_eff
            agent.tax = 0
            agent.trade_bonus = 0
            # agent.trade_bonus = 0
        
        # set up datacollector
        self.datacollector = DataCollector({
            "member_count": "member_count",
            "other_count":"other_count",
            "average_cooperativeness":"average_cooperativeness",
            "other_wealth":"other_wealth",
            "total_wealth":"total_wealth",
            "member_wealth":"member_wealth",
            "other_eff":"other_eff",
            "total_eff":"total_eff",
            "member_eff":"member_eff"
        })
        self.datacollector.collect(self)



    def compute_statistics(self):
        # only used for datacollector

        self.member_count = 0
        self.other_count = 0

        self.member_wealth = 0
        self.other_wealth = 0
        self.total_wealth = 0

        self.member_eff = 0
        self.other_eff = 0
        self.total_eff = 0

        total_cooperativeness = 0

        for agent in self.agents:
            if agent.strategy == 1:
                self.member_wealth += agent.wealth
                self.member_eff += agent.efficiency
                self.member_count += 1
            else:
                self.other_wealth += agent.wealth
                self.other_eff += agent.efficiency
                self.other_count += 1
            total_cooperativeness += agent.cooperativeness
        
        self.average_cooperativeness = total_cooperativeness / 320

        self.total_wealth = self.member_wealth + self.other_wealth
        self.member_wealth = self.member_wealth / max(self.member_count, 1)
        self.other_wealth = self.other_wealth / max(self.other_count, 1)
        self.total_wealth = self.total_wealth / 320

        self.total_eff = self.member_eff + self.other_eff
        self.member_eff = self.member_eff / max(self.member_count, 1)
        self.other_eff = self.other_eff / max(self.other_count, 1)
        self.total_eff = self.total_eff / 320



    def collect_taxes(self):
        members = [agent for agent in self.agents if agent.strategy == 1]
        if not members:
            self.running = False
            return
        for agent in members:
            tax = math.log(agent.wealth) * self.eutax  # log test
            agent.tax_payed = tax
            agent.wealth -= tax
            self.treasury += tax



    def distribute_benefits(self):
        members = [agent for agent in self.agents if agent.strategy == 1]
        if not members:
            self.running = False
            return

        if self.eu_strategy == "default":
            benefit = self.treasury / len(members)
            for agent in members:
                agent.wealth += benefit
                if benefit + agent.trade_bonus > agent.tax_payed:
                    agent.cooperativeness = min(agent.cooperativeness + self.tax_influence, 1)
                elif benefit  + agent.trade_bonus < agent.tax_payed:
                    agent.cooperativeness = max(agent.cooperativeness - self.tax_influence, -1)

        elif self.eu_strategy == "hardship":
            total_hardship = 0
            for agent in members:
                total_hardship += 1 - agent.cooperativeness
            for agent in members:
                agent_benefit = ((1 - agent.cooperativeness) / total_hardship) * self.treasury
                agent.wealth += agent_benefit
                if agent_benefit + agent.trade_bonus > agent.tax_payed:
                    agent.cooperativeness = min(agent.cooperativeness + self.tax_influence, 1)
                elif agent_benefit  + agent.trade_bonus < agent.tax_payed:
                    agent.cooperativeness = max(agent.cooperativeness - self.tax_influence, -1)
        
        else:
            # unknown strategy
            raise NotImplementedError()

        self.treasury = 0



    def compute_virtual_benefits(self):
        others = [agent for agent in self.agents if agent.strategy == 2]
        members = [agent for agent in self.agents if agent.strategy == 1]

        if not members or not others:
            self.running = False
            return

        if self.eu_strategy == "default":
            for agent in others:
                virtual_tax_payed = math.log(agent.wealth) * self.eutax  # log edit
                virtual_treasury = self.treasury + virtual_tax_payed
                virtual_benefit = virtual_treasury / (len(members) + 1)
                if virtual_benefit + agent.trade_bonus > virtual_tax_payed:
                    agent.cooperativeness = min(agent.cooperativeness + self.tax_influence, 1)
                elif virtual_benefit + agent.trade_bonus < virtual_tax_payed:
                    agent.cooperativeness = max(agent.cooperativeness - self.tax_influence, -1)

        elif self.eu_strategy == "hardship":
            total_hardship = 0
            for agent in members:
                total_hardship += 1 - agent.cooperativeness
            for agent in others:
                virtual_tax_payed = math.log(agent.wealth) * self.eutax  # log edit
                virtual_treasury = self.treasury + virtual_tax_payed
                virtual_benefit = (1 / (total_hardship + 1)) * virtual_treasury
                # hardship of every defector is = max hardship = 1
                if virtual_benefit + agent.trade_bonus > virtual_tax_payed:
                    agent.cooperativeness = min(agent.cooperativeness + self.tax_influence, 1)
                elif virtual_benefit + agent.trade_bonus < virtual_tax_payed:
                    agent.cooperativeness = max(agent.cooperativeness - self.tax_influence, -1)
        
        else:
            # unknown strategy
            raise NotImplementedError()



    def step(self):
        for agent in self.agents: agent.has_traded = False
        self.round += 1

        self.schedule.step()
        
        self.compute_statistics()

        self.collect_taxes()
        self.compute_virtual_benefits()
        self.distribute_benefits()

        self.datacollector.collect(self)