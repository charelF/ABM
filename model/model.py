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
    def __init__(self, basic_trade_reward, member_trade_reward,
                international_trade, max_eff, eutax, neighbor_influence, tax_influence):

        # set up parameters
        self.basic_trade_reward = basic_trade_reward
        self.member_trade_reward = member_trade_reward
        self.international_trade = international_trade
        self.max_eff = max_eff
        self.eutax = eutax
        self.neighbor_influence = neighbor_influence
        self.tax_influence = tax_influence

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
            agent.wealth = 1
            agent.efficiency = max(random.random() * self.max_eff, 0.0000001)
            # agent.efficiency = agent.SHAPE_AREA * max_eff
            agent.tax = 0
            agent.eu_bonus = 0
            agent.fictional_bonus = 0
        
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
            tax = agent.wealth * self.eutax
            agent.tax_payed = tax
            agent.wealth -= tax
            self.treasury += tax



    def distribute_benefits(self):
        members = [agent for agent in self.agents if agent.strategy == 1]
        if not members:
            self.running = False
            return

        benefit = self.treasury / len(members)
        for agent in members:
            agent.wealth += benefit
            if benefit + agent.eu_bonus > agent.tax_payed:
                agent.cooperativeness = min(agent.cooperativeness + self.tax_influence, 1)
            elif benefit  + agent.eu_bonus < agent.tax_payed:
                agent.cooperativeness = max(agent.cooperativeness - self.tax_influence, -1)
                
        self.treasury = 0



    def compute_virtual_benefits(self):
        others = [agent for agent in self.agents if agent.strategy == 2]
        members = [agent for agent in self.agents if agent.strategy == 1]
        if not members or not others:
            self.running = False
            return
        for agent in others:
            virtual_tax_payed = agent.wealth * self.eutax
            virtual_treasury = self.treasury + virtual_tax_payed
            virtual_benefit = virtual_treasury / (len(members) + 1)
            if virtual_benefit + agent.fictional_bonus > virtual_tax_payed:
                agent.cooperativeness = min(agent.cooperativeness + self.tax_influence, 1)
            elif virtual_benefit + agent.fictional_bonus < virtual_tax_payed:
                agent.cooperativeness = max(agent.cooperativeness - self.tax_influence, -1)



    def step(self):
        for agent in self.agents: agent.has_traded = False
        self.round += 1

        self.schedule.step()
        
        self.compute_statistics()

        self.collect_taxes()
        self.compute_virtual_benefits()
        self.distribute_benefits()

        self.datacollector.collect(self)

            























    # def distribute_taxes(self):

        # # Hardship
        # self.total_hardship = 0.000000001
        # traded_agents = [agent for agent in self.agents if agent.strategy == 1]
        # for agent in traded_agents:
        #     self.total_hardship += 1 - agent.cooperativeness
        #     # hardship is opposite to cooperativeness
        #     # lots of cooperativeness --> total hardship small
        
        # for agent in traded_agents:
        #     distributed_wealth =  (1 - agent.cooperativeness)/ self.total_hardship * self.treasury
        #     agent.wealth += distributed_wealth
        #     self.treasury -= distributed_wealth
        #     if distributed_wealth + agent.eu_bonus < agent.tax:
        #         agent.cooperativeness -= self.tax_influence
        #     else:
        #         agent.cooperativeness += self.tax_influence

        #     if agent.cooperativeness > 1:
        #         agent.cooperativeness = 1
        #     elif agent.cooperativeness < -1:
        #         agent.cooperativeness = -1
        # traded_agents = [agent for agent in self.agents if agent.strategy == 1]
        # for agent in traded_agents:
        #     # distribution = self.treasury / self.count_collaborators()
        #     # distribution = agent.tax 
        #     # agent.wealth += distribution
        #     # if distribution + agent.eu_bonus < agent.tax:
        #     # if distribution + agent.eu_bonus < agent.tax:
        #     if agent.eu_bonus < 0:
        #         agent.cooperativeness = max(agent.cooperativeness - self.tax_influence, -1)
        #     elif agent.eu_bonus > 0:
        #         agent.cooperativeness = min(agent.cooperativeness + self.tax_influence, 1)

        # self.treasury = 0


    # def calculate_benefit(self):
    #     traded_agents = [agent for agent in self.agents if agent.strategy == 2]
    #     for agent in traded_agents:
    #         # distribution = (self.treasury + agent.wealth * self.eutax) / (self.count_collaborators() + 1)
    #         # distribution = agent.wealth * self.eutax
    #         # agent.wealth += distribution
    #         # if distribution + agent.fictional_bonus < distribution:
    #         if agent.fictional_bonus < 0:
    #             agent.cooperativeness = max(agent.cooperativeness - self.tax_influence, -1)
    #         elif agent.fictional_bonus > 0:
    #             agent.cooperativeness = min(agent.cooperativeness + self.tax_influence, 1)


    #     # for agent in self.agents:
    #     #     #print(agent.NUTS_ID, agent.wealth)
    #     #     if agent.strategy == 2:
    #     #         tax_payment = agent.wealth * self.eutax
    #     #         fictional_total_hardship = self.total_hardship + (1 - agent.cooperativeness)
    #     #         try:
    #     #             tax_distribution = (1 - agent.cooperativeness)/ fictional_total_hardship * self.treasury
    #     #         except:
    #     #             tax_distribution = 0

    #     #         if tax_payment < tax_distribution + agent.fictional_bonus:
    #     #             agent.cooperativeness += self.tax_influence
    #     #         else:
    #     #             agent.cooperativeness -= self.tax_influence

    #     #         if agent.cooperativeness > 1:
    #     #             agent.cooperativeness = 1
    #     #         elif agent.cooperativeness < -1:
    #     #             agent.cooperativeness = -1                                
    #             #print(agent.NUTS_ID , tax_payment, agent.fictional_bonus, tax_distribution)



    
